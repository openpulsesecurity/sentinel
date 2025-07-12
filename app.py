from flask import Flask, render_template
from models import db, Event
from snmp_listener import start_snmp_listener_in_thread
from syslog_listener import start_syslog_listener_in_thread

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///siem.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

initialized = False

@app.route('/')
def index():
    global initialized
    if not initialized:
        with app.app_context():
            db.create_all()
        start_snmp_listener_in_thread(port=1162)
        start_syslog_listener_in_thread(port=1514)
        initialized = True
    events = Event.query.order_by(Event.timestamp.desc()).limit(100).all()
    return render_template('index.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)