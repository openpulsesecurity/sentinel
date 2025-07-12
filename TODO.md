# Sentinel - Roadmap

This document outlines the planned features and improvements from **Sentinel**.
Items are organized by priority and development phases.

## Phase 1: Core Functionality (High Priority)

### Real-time Alerting System
- [ ] **Alert Rule Engine**
  - [ ] Create `AlertRule` model in database
  - [ ] Implement rule evaluation engine
  - [ ] Support time-based thresholds (e.g., "5 events in 10 minutes")
  - [ ] Support pattern matching
  - [ ] Group events by source IP, event type, etc.

- [ ] **Notification Channels**
  - [ ] Email notifications (SMTP integration)
    - [ ] Slack webhook integration
    - [ ] Microsoft Teams webhook integration
    - [ ] SMS notifications (Twilio integration)
    - [ ] Generic webhook support

- [ ] **Alert Management**
  - [ ] Alert suppression (prevent spam)
  - [ ] Alert escalation (different severity levels)
  - [ ] Alert acknowledgment and resolution
  - [ ] Alert history and audit trail

### Enhanced Syslog Parsing
- [ ] **Multi-format Support**
  - [ ] RFC 3164 (traditional syslog) parser
  - [ ] RFC 5424 (structured syslog) parser
  - [ ] CEF (Common Event Format) parser
  - [ ] JSON log format support

- [ ] **Vendor-specific Parsers**
  - [ ] FortiGate log parser
  - [ ] pfSense log parser
  - [ ] Cisco ASA log parser
  - [ ] Windows Event Log parser (if received via syslog)
  - [ ] Juniper SRX log parser

- [ ] **Field Extraction**
  - [ ] Automatic extraction of common fields (username, src_ip, dst_ip, port, action)
  - [ ] Grok pattern support (Logstash-style)
  - [ ] Custom field extraction rules
  - [ ] Store parsed fields in `parsed_data` JSON column

### SNMP Polling & Monitoring
- [ ] **Device Management**
  - [ ] `Device` model for storing monitored devices
  - [ ] Web UI for adding/editing/deleting devices
  - [ ] Device discovery (SNMP walk to find available OIDs)
  - [ ] Device grouping and tagging

- [ ] **Polling Engine**
  - [ ] Background polling scheduler (APScheduler)
  - [ ] Configurable polling intervals per device/OID
  - [ ] Polling profiles/templates for device types
  - [ ] Store polled metrics in separate `Metric` table

- [ ] **Performance Monitoring**
  - [ ] CPU utilization monitoring
  - [ ] Memory usage monitoring
  - [ ] Interface statistics (bandwidth, errors, discards)
  - [ ] Disk space monitoring
  - [ ] Custom OID monitoring

## Phase 2: User Experience & Visualization (Medium Priority)

### Advanced Web Dashboard
- [ ] **Real-time Features**
  - [ ] WebSocket integration (Flask-SocketIO)
  - [ ] Live event feed without page refresh
  - [ ] Real-time event counters and statistics
  - [ ] Live alert notifications in UI

- [ ] **Interactive Charts & Graphs**
  - [ ] Time-series charts for event volume
  - [ ] Top source IPs chart
  - [ ] Event type distribution pie chart
  - [ ] Severity trend analysis
  - [ ] Geographic heat map (with GeoIP data)

- [ ] **Search & Filtering**
  - [ ] Advanced search with multiple criteria
  - [ ] Date/time range filtering
  - [ ] Saved search queries
  - [ ] Export search results (CSV, JSON)
  - [ ] Elasticsearch-style query syntax

- [ ] **Custom Dashboards**
  - [ ] Drag-and-drop dashboard builder
  - [ ] Customizable widgets
  - [ ] Multiple dashboard support
  - [ ] Dashboard sharing and templates

### Event Correlation & Analytics
- [ ] **Time-based Correlation**
  - [ ] Detect event sequences and patterns
  - [ ] Sliding window analysis
  - [ ] Event clustering algorithms
  - [ ] Correlation rule builder

- [ ] **Cross-protocol Correlation**
  - [ ] Link SNMP and Syslog events
  - [ ] Network topology awareness
  - [ ] Device relationship mapping

- [ ] **Baseline & Anomaly Detection**
  - [ ] Learn normal traffic patterns
  - [ ] Statistical anomaly detection
  - [ ] Threshold-based alerting
  - [ ] Trend analysis

## Phase 3: Security & Intelligence (Medium Priority)

### Threat Intelligence Integration
- [ ] **IP Reputation**
  - [ ] VirusTotal API integration
  - [ ] AbuseIPDB integration
  - [ ] Custom threat feed support
  - [ ] IP reputation caching

- [ ] **Data Enrichment**
  - [ ] GeoIP location data (MaxMind GeoLite2)
  - [ ] Reverse DNS lookups
  - [ ] WHOIS data integration
  - [ ] ASN (Autonomous System) information

- [ ] **IOC Matching**
  - [ ] Indicators of Compromise database
  - [ ] STIX/TAXII feed integration
  - [ ] Custom IOC lists
  - [ ] Automatic IOC matching against events

### Security & Compliance
- [ ] **User Authentication**
  - [ ] Local user accounts with password hashing
  - [ ] LDAP/Active Directory integration
  - [ ] SAML SSO support
  - [ ] Multi-factor authentication (TOTP)

- [ ] **Authorization & Access Control**
  - [ ] Role-based access control (RBAC)
  - [ ] Permission levels (admin, analyst, viewer)
  - [ ] Resource-based permissions
  - [ ] API key management

- [ ] **Audit & Compliance**
  - [ ] User action audit logging
  - [ ] Data retention policies
  - [ ] Compliance reporting (SOX, PCI-DSS, HIPAA)
  - [ ] Data export for external audits

## Phase 4: Performance & Scalability (Lower Priority)

### Database Optimization
- [ ] **Database Migration**
  - [ ] PostgreSQL support
  - [ ] TimescaleDB for time-series data
  - [ ] Database connection pooling
  - [ ] Query optimization

- [ ] **Data Management**
  - [ ] Automatic data archival
  - [ ] Data compression
  - [ ] Partitioning strategies
  - [ ] Event deduplication

### High Availability & Scaling
- [ ] **Clustering**
  - [ ] Multiple collector nodes
  - [ ] Load balancing
  - [ ] Failover mechanisms
  - [ ] Distributed processing

- [ ] **Performance Monitoring**
  - [ ] System health monitoring
  - [ ] Performance metrics collection
  - [ ] Capacity planning tools
  - [ ] Bottleneck identification

## Phase 5: Advanced Features (Future)

### Machine Learning & AI
- [ ] **Anomaly Detection**
  - [ ] Unsupervised learning models
  - [ ] Behavioral analysis (UEBA)
  - [ ] Predictive alerting
  - [ ] False positive reduction

### Integration & Automation
- [ ] **API Development**
  - [ ] RESTful API for all operations
  - [ ] GraphQL API support
  - [ ] API documentation (Swagger/OpenAPI)
  - [ ] Rate limiting and authentication

- [ ] **SOAR Integration**
  - [ ] Phantom/Splunk SOAR connector
  - [ ] IBM Resilient integration
  - [ ] Custom playbook support
  - [ ] Automated response actions

### Advanced Visualization
- [ ] **Network Topology**
  - [ ] Visual network maps
  - [ ] Device relationship visualization
  - [ ] Attack flow diagrams
  - [ ] Interactive network graphs

## Bug Fixes & Technical Debt

### Current Issues
- [ ] **SNMP Source IP Extraction**
  - [ ] Fix source IP extraction in asyncio SNMP listener
  - [ ] Consider switching to synchronous pysnmp for reliability
  - [ ] Add fallback methods for IP extraction

- [ ] **Error Handling**
  - [ ] Improve error handling in all listeners
  - [ ] Add proper logging throughout application
  - [ ] Graceful degradation for failed components

### Code Quality
- [ ] **Testing**
  - [ ] Unit tests for all modules
  - [ ] Integration tests for listeners
  - [ ] End-to-end testing
  - [ ] Performance testing

- [ ] **Documentation**
  - [ ] Code documentation (docstrings)
  - [ ] API documentation
  - [ ] Deployment guides
  - [ ] Troubleshooting guides

- [ ] **Containerization**
  - [ ] Dockerfile creation
  - [ ] Docker Compose setup
  - [ ] Kubernetes manifests
  - [ ] Container security scanning

## Completed Features

- [x] Basic SNMP trap listener
- [x] Basic syslog listener
- [x] SQLite database storage
- [x] Flask web interface
- [x] Event normalization (OID mapping)
- [x] Basic severity assignment
- [x] Event enrichment processor
- [x] Multi-threaded listeners
- [x] Basic HTML dashboard