import socketserver
import threading
from datetime import datetime
from flask import Flask
from models import db, Event
from event_processor import process_event_for_enrichment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///siem.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        source_ip = self.client_address[0]
        timestamp = datetime.utcnow()

        message = data

        with app.app_context():
            event = Event(
                timestamp=timestamp,
                source_ip=source_ip,
                event_type="syslog",
                protocol="udp",
                oid=None,
                value=message[:1024],
                severity="Unknown"
            )
            db.session.add(event)
            db.session.flush()
            event_id = event.id
            db.session.commit()
            print(f"Received Syslog from {source_ip}: {message[:80]}...")

            process_event_for_enrichment(event_id)

def run_syslog_listener(port=1514):
    HOST, PORT = "0.0.0.0", port
    try:
        socketserver.UDPServer.allow_reuse_address = True
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        print(f"Syslog listener started on 0.0.0.0:{PORT}")
        server.serve_forever(poll_interval=0.5)
    except Exception as e:
        print(f"Error starting Syslog listener: {e}")

def start_syslog_listener_in_thread(port=1514):
    thread = threading.Thread(target=run_syslog_listener, args=(port,), daemon=True)
    thread.start()