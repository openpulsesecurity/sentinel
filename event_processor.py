from models import db, Event
import re

SNMP_OID_MAPPING = {
    ".1.3.6.1.6.3.1.1.5.1": "SNMP Cold Start",
    ".1.3.6.1.6.3.1.1.5.2": "SNMP Warm Start",
    ".1.3.6.1.6.3.1.1.5.3": "SNMP Link Down",
    ".1.3.6.1.6.3.1.1.5.4": "SNMP Link Up",
    ".1.3.6.1.6.3.1.1.5.5": "SNMP Authentication Failure",
    ".1.3.6.1.6.3.1.1.5.6": "SNMP EGP Neighbor Loss",
    # TODO Add FortiGate/pfSense
}

SEVERITY_RULES = {
    "snmp_trap": {
        "critical": [
            ".1.3.6.1.6.3.1.1.5.3", # Link Down
            ".1.3.6.1.6.3.1.1.5.5", # Authentication Failure
            "fail", "error", "down", "critical", "unauthorized", "deny"
        ],
        "high": [
            ".1.3.6.1.6.3.1.1.5.1", # Cold Start
            "warn", "warning", "threshold", "exceeded"
        ],
        "informational": [
            ".1.3.6.1.6.3.1.1.5.4", # Link Up
            "up", "start", "config", "change", "success", "info"
        ]
    },
    "syslog": {
        "critical": [
            r"deny\s", r"rejected\s", r"failed\slogin", r"authentication\sfailed",
            r"intrusion\sdetected", r"critical\serror"
        ],
        "high": [
            r"failed\s", r"blocked\s", r"unauthorized", r"warning", r"error"
        ],
        "informational": [
            r"login\ssuccess", r"accepted", r"connected", r"info", r"start", r"stop", r"status"
        ]
    }
}

def get_event_severity(event_type, identifier, value=""):
    """
    Determines the severity of an event based on its type, OID/keyword, and value.
    Identifier can be OID for SNMP, or a keyword for Syslog.
    """
    rules = SEVERITY_RULES.get(event_type, {})

    # Check Critical rules
    for pattern in rules.get("critical", []):
        if event_type == "snmp_trap" and identifier == pattern:
            return "Critical"
        if event_type == "syslog" and re.search(pattern, value, re.IGNORECASE):
            return "Critical"

    # Check High rules
    for pattern in rules.get("high", []):
        if event_type == "snmp_trap" and identifier == pattern:
            return "High"
        if event_type == "syslog" and re.search(pattern, value, re.IGNORECASE):
            return "High"

    # Check Informational rules
    for pattern in rules.get("informational", []):
        if event_type == "snmp_trap" and identifier == pattern:
            return "Informational"
        if event_type == "syslog" and re.search(pattern, value, re.IGNORECASE):
            return "Informational"

    return "Unknown" # Default if no rule matches

def process_event_for_enrichment(event_id):
    """
    Fetches an event by ID, enriches it, and updates it in the database.
    This function should be called within a Flask app context.
    """
    with db.session.begin_nested():
        event = db.session.get(Event, event_id)
        if not event:
            print(f"Event with ID {event_id} not found for enrichment.")
            return

        original_oid_or_value = ""
        if event.event_type == "snmp_trap":
            if event.oid:
                event.value_original_oid = event.oid
                event.oid = SNMP_OID_MAPPING.get(event.oid, event.oid)
                original_oid_or_value = event.value_original_oid

            event.severity = get_event_severity(event.event_type, original_oid_or_value, event.value)

        elif event.event_type == "syslog":
            original_oid_or_value = event.value # Use full message for rules
            event.severity = get_event_severity(event.event_type, None, event.value)

        db.session.add(event)
    db.session.commit()
    print(f"Event {event.id} enriched: Type={event.event_type}, Severity={event.severity}")