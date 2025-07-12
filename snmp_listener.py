import asyncio
import threading
from datetime import datetime
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from flask import Flask
from models import db, Event
from event_processor import process_event_for_enrichment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///siem.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def trap_callback(snmpEngine, stateReference, contextEngineId, contextName,
                  varBinds, cbCtx):
    source_ip = "unknown"
    timestamp = datetime.utcnow()

    with app.app_context():
        event_ids_to_process = []
        for name, val in varBinds:
            event = Event(
                timestamp=timestamp,
                source_ip=source_ip,
                event_type="snmp_trap",
                protocol="udp",
                oid=name.prettyPrint(),
                value=val.prettyPrint(),
                severity="Unknown"
            )
            db.session.add(event)
            db.session.flush()
            event_ids_to_process.append(event.id)
        db.session.commit()
        print(f'Received SNMP Trap (source IP: {source_ip})')

        for event_id in event_ids_to_process:
            process_event_for_enrichment(event_id)

async def run_snmp_listener(port=1162):
    snmpEngine = engine.SnmpEngine()

    config.addTransport(
        snmpEngine,
        udp.domainName,
        udp.UdpAsyncioTransport().openServerMode(('0.0.0.0', port))
    )

    config.addV1System(snmpEngine, 'my-area', 'public')
    ntfrcv.NotificationReceiver(snmpEngine, trap_callback)

    print(f'SNMP Trap listener started on 0.0.0.0:{port}')
    await asyncio.Event().wait()

def start_snmp_listener_in_thread(port=1162):
    def runner():
        asyncio.run(run_snmp_listener(port))
    thread = threading.Thread(target=runner, daemon=True)
    thread.start()