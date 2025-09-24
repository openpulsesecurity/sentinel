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

## Getting Started

Follow these steps to get Sentinel up and running on your system.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/openpulsesecurity/sentinel.git
    cd sentinel
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Net-SNMP utilities (for testing `snmptrap`):**
    On Debian/Ubuntu:
    ```bash
    sudo apt update
    sudo apt install snmp snmp-mibs-downloader
    sudo download-mibs
    ```
    On other Linux distributions, use your package manager (e.g., `dnf install net-snmp-utils` on Fedora/RHEL).

### Running the Application

1.  **Ensure virtual environment is active:**
    ```bash
    source .venv/bin/activate
    ```

2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will start, and you will see messages indicating that both the SNMP Trap listener and Syslog listener have started.

3.  **Access the Web Dashboard:**
    Open your web browser and navigate to:
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Configuration

### Listener Ports

*   **SNMP Traps**: Listens on UDP port `1162`.
*   **Syslog**: Listens on UDP port `1514`.

    **Important:** By default, standard SNMP (162) and Syslog (514) ports are privileged (below 1024) and require root permissions. For development, we use higher ports (`1162` and `1514`). If you wish to use standard ports in a production environment, you will need to configure your system accordingly (e.g., `sudo setcap 'cap_net_bind_service=+ep' /path/to/python_executable` or use a reverse proxy/port forwarding).

### Configuring Devices to Send Logs

You need to configure your network devices (FortiGate, pfSense, routers, switches, servers) to send their log data to the IP address of the machine running **Sentinel** on the specified ports.

#### FortiGate / pfSense (Syslog)

Configure your firewall to send logs to the Sentinel server's IP address on **UDP port 1514**.
*   **FortiGate:** System > Log & Report > Log Settings -> Enable "Send Logs to Syslog", configure Server IP and Port.
*   **pfSense:** Status > System Logs > Settings -> Enable "Remote Logging", add Server IP and Port.

#### Any Device (SNMP Traps)

Configure devices to send SNMP traps to the Sentinel server's IP address on **UDP port 1162**. Ensure the SNMP community string is set to `public` (or match whatever is configured in `snmp_listener.py`).

## Testing Log Ingestion

### Test SNMP Trap

From your terminal (after installing `snmp` package):

```bash
snmptrap -v 2c -c public 127.0.0.1:1162 '' .1.3.6.1.6.3.1.1.5.1
```

You should see "SNMP Cold Start" with "High" severity in the web UI.

### Test Syslog Message

From your terminal (on Linux):

```bash
echo "<13>Jul 10 15:30:00 myhost program: This is a test syslog message about a failed login attempt." | nc -u -w0 127.0.0.1 1514
```

You should see a syslog event with "Critical" severity in the web UI due to the "failed login" keyword.

## Future Enhancements (Roadmap)

*   **Advanced Syslog Parsing**: Implement robust parsing for various syslog formats (RFC 3164, RFC 5424, FortiGate native logs, pfSense native logs) to extract more structured fields (e.g., username, source/dest IPs, port, action).
*   **SNMP Polling**: Add functionality to actively poll devices for specific OIDs (e.g., CPU, memory, interface status) at regular intervals.
*   **Alerting Notifications**: Integrate with email, Slack, or other platforms to send notifications when critical events occur.
*   **User Interface Improvements**:
    *   Filtering and searching of events.
    *   Pagination for large datasets.
    *   Real-time event updates using WebSockets (Flask-SocketIO).
    *   Dashboard analytics (graphs for event trends, top sources/events).
*   **Rule Management**: Allow web-based configuration of normalization and alerting rules.
*   **Database**: Migrate from SQLite to PostgreSQL for better performance and concurrency in production.
*   **Containerization**: Provide Dockerfiles for easy deployment.
*   **Authentication & Authorization**: Secure the web dashboard with user logins.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is open-source and available under the [MIT License](LICENSE).
