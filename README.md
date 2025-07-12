# Sentinel

**Sentinel** is a lightweight Security Information and Event Management (SIEM) application built with Flask, designed to collect and display network events from various sources using SNMP Traps and Syslog. It aims to provide basic visibility into network activity, security incidents, and operational events.

## Features

*   **SNMP Trap Listener**: Receives and processes SNMP traps (v1/v2c) from network devices.
*   **Syslog Listener**: Collects syslog messages over UDP from firewalls, routers, and other logging sources.
*   **Unified Event Storage**: Stores both SNMP and Syslog events in a SQLite database for easy access and querying.
*   **Event Normalization & Enrichment**:
    *   Maps common SNMP OIDs to human-readable names.
    *   Assigns severity (Critical, High, Medium, Low, Informational) to events based on predefined rules for both SNMP and Syslog messages.
*   **Web-based Dashboard**: A simple Flask web interface to view recent collected events, including their type, source, and assigned severity.
*   **Background Listeners**: SNMP and Syslog listeners run in separate threads, allowing continuous collection while the Flask web server operates.