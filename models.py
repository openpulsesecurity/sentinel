from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    source_ip = db.Column(db.String(45), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    protocol = db.Column(db.String(10), nullable=False)
    oid = db.Column(db.String(255), nullable=True)
    value_original_oid = db.Column(db.String(255), nullable=True)
    value = db.Column(db.String(1024), nullable=False)
    severity = db.Column(db.String(20), default="Unknown", nullable=False)

    def __repr__(self):
        return f'<Event {self.id} Type: {self.event_type} Source: {self.source_ip} Severity: {self.severity}>'