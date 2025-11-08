# Golf Tournament Management System - Non-Functional Requirements (NFR) Metrics

## Document Purpose
This document establishes testable, measurable criteria for evaluating the GTMS system's quality attributes. All metrics must be verifiable through automated testing, monitoring, or user testing procedures.

## NFR Categories

### 1. Performance

#### 1.1 Response Time
| Metric | Target | Critical Threshold | Measurement Method | Priority |
|--------|--------|-------------------|-------------------|----------|
| API Read Operations (p50) | < 100ms | < 200ms | Application Performance Monitoring (APM) | High |
| API Read Operations (p95) | < 200ms | < 500ms | APM | High |
| API Write Operations (p50) | < 300ms | < 1s | APM | High |
| API Write Operations (p95) | < 1s | < 2s | APM | Medium |
| Database Query Time (p95) | < 50ms | < 100ms | PostgreSQL slow query log | High |
| Frontend Initial Load Time | < 2s | < 3s | Lighthouse/WebPageTest | Medium |
| Frontend Time to Interactive (TTI) | < 3s | < 5s | Lighthouse | Medium |

**Acceptance Criteria**:
- All target metrics must be met under normal load (100 concurrent users)
- Critical thresholds must not be exceeded under peak load (500 concurrent users)
- Performance regression tests must pass in CI/CD pipeline

**Testing Approach**:
- Load testing with Apache JMeter or Locust
- Continuous monitoring with Prometheus + Grafana
- Performance budgets enforced in CI/CD

#### 1.2 Live Score Update Latency
| Metric | Target | Critical Threshold | Measurement Method | Priority |
|--------|--------|-------------------|-------------------|----------|
| Score Entry to WebSocket Broadcast | < 300ms | < 500ms | Custom WebSocket latency monitoring | Critical |
| WebSocket Broadcast to Frontend Update | < 100ms | < 200ms | Client-side performance markers | High |
| End-to-End Latency (Entry to Display) | < 500ms | < 1s | Synthetic monitoring | Critical |

**Acceptance Criteria**:
- 99% of score updates must meet target latency
- WebSocket connection must auto-reconnect within 5 seconds of disconnection
- Fallback to polling (every 10s) if WebSocket fails

**Testing Approach**:
- WebSocket load testing with custom scripts
- Real-time latency monitoring
- Chaos engineering tests (connection failures)

#### 1.3 Throughput
| Metric | Target | Measurement Method | Priority |
|--------|--------|-------------------|----------|
| Score Submissions per Second | 100 req/s | Load testing | Medium |
| Concurrent WebSocket Connections | 1,000 | WebSocket load testing | High |
| Leaderboard Queries per Second | 500 req/s | Load testing | Medium |

**Acceptance Criteria**:
- System must maintain target throughput without degradation
- Response times must remain within targets under max throughput

### 2. Scalability

#### 2.1 Capacity
| Metric | Target | Measurement Method | Priority |
|--------|--------|-------------------|----------|
| Maximum Concurrent Users | 1,000+ | Load testing with gradual ramp-up | High |
| Maximum Concurrent Tournaments | 20+ | Multi-tenant load testing | High |
| Maximum Players per Tournament | 200+ | Data volume testing | High |
| Maximum Rounds per Tournament | 4 | Functional testing | Low |
| Maximum Hole Scores Stored | 10,000,000+ | Database capacity testing | Medium |

**Acceptance Criteria**:
- System must handle 1,000 concurrent users with < 5% error rate
- 20 concurrent tournaments must run without resource contention
- Database must efficiently store and query 10+ years of tournament data

**Testing Approach**:
- Incremental load testing to find breaking points
- Database stress testing with realistic data volumes
- Resource utilization monitoring (CPU, memory, disk I/O)

#### 2.2 Horizontal Scaling
| Metric | Target | Measurement Method | Priority |
|--------|--------|-------------------|----------|
| Backend Service Instances | 1-10 instances | Container orchestration | Medium |
| Database Read Replicas | 0-3 replicas | PostgreSQL replication | Low |
| Cache Cluster Nodes | 1-3 nodes | Redis Cluster | Low |

**Acceptance Criteria**:
- Adding backend instances must increase throughput linearly (up to 5 instances)
- Load balancer must distribute traffic evenly across instances
- No session affinity required (stateless backend design)

### 3. Availability & Reliability

#### 3.1 Uptime
| Metric | Target | Critical Threshold | Measurement Method | Priority |
|--------|--------|-------------------|-------------------|----------|
| System Uptime (monthly) | > 99.5% | > 99.0% | Uptime monitoring (UptimeRobot, Pingdom) | High |
| Scheduled Downtime (monthly) | < 2 hours | < 4 hours | Maintenance log | Medium |
| Mean Time Between Failures (MTBF) | > 720 hours (30 days) | > 168 hours (7 days) | Incident tracking | Medium |
| Mean Time To Recovery (MTTR) | < 1 hour | < 4 hours | Incident tracking | High |

**Acceptance Criteria**:
- System uptime of 99.5% allows for approximately 3.6 hours of downtime per month
- Planned maintenance must be scheduled during low-usage windows
- Critical bugs must be patched and deployed within MTTR target

**Testing Approach**:
- Continuous uptime monitoring with alerting
- Regular disaster recovery drills
- Incident postmortem analysis

#### 3.2 Fault Tolerance
| Requirement | Implementation | Testing Method | Priority |
|------------|----------------|----------------|----------|
| Database Failover | Automated failover to standby | Failover testing | High |
| Backend Service Recovery | Auto-restart on crash, health checks | Chaos engineering | High |
| WebSocket Reconnection | Client-side auto-reconnect with exponential backoff | Connection failure simulation | High |
| Graceful Degradation | Leaderboard falls back to polling if WebSocket fails | Feature flag testing | Medium |

**Acceptance Criteria**:
- Database failover must complete within 30 seconds with zero data loss
- Backend services must restart automatically within 10 seconds
- WebSocket clients must reconnect within 5 seconds
- Polling fallback must activate automatically when WebSocket unavailable

### 4. Security

#### 4.1 Authentication & Authorization
| Requirement | Implementation | Testing Method | Priority |
|------------|----------------|----------------|----------|
| Password Strength | Minimum 8 characters, complexity requirements | Unit tests | High |
| Password Storage | PBKDF2 with 260,000 iterations (Django default) | Security audit | Critical |
| Session Timeout | 60 minutes of inactivity | Functional testing | Medium |
| JWT Token Expiry | Access: 15 min, Refresh: 7 days | Token validation testing | High |
| Role-Based Access Control (RBAC) | Admin, Scorer, Player, Public roles | Permission testing | High |

**Acceptance Criteria**:
- No plaintext passwords stored in database
- All API endpoints enforce authentication (except public leaderboard)
- Authorization checks prevent privilege escalation

**Testing Approach**:
- Automated security testing (OWASP ZAP)
- Penetration testing for critical vulnerabilities
- Regular dependency vulnerability scans

#### 4.2 Data Protection
| Requirement | Implementation | Testing Method | Priority |
|------------|----------------|----------------|----------|
| Encryption in Transit | TLS 1.3 for all HTTPS/WSS | SSL Labs testing | Critical |
| Encryption at Rest | PostgreSQL encryption (optional, based on compliance) | Configuration audit | Medium |
| Input Validation | DRF serializers + custom validators | Fuzzing, injection testing | High |
| SQL Injection Prevention | ORM parameterized queries | SAST tools, manual testing | Critical |
| XSS Prevention | React auto-escaping + CSP headers | XSS vulnerability scanning | High |
| CSRF Prevention | CSRF tokens for state-changing operations | CSRF testing | High |

**Acceptance Criteria**:
- SSL Labs rating of A or higher
- No SQL injection vulnerabilities found in penetration testing
- No stored or reflected XSS vulnerabilities
- All user inputs validated and sanitized

#### 4.3 API Security
| Requirement | Implementation | Testing Method | Priority |
|------------|----------------|----------------|----------|
| Rate Limiting | 100 req/min per IP, 1000 req/min per authenticated user | Rate limit testing | High |
| CORS Configuration | Whitelist allowed origins | CORS testing | High |
| API Key Rotation | JWT refresh token rotation | Token management testing | Medium |
| Audit Logging | All score modifications logged with user and timestamp | Log verification | High |

**Acceptance Criteria**:
- Rate limiting prevents abuse without impacting legitimate users
- CORS only allows requests from authorized domains
- Audit logs are tamper-proof and retained for 1 year

### 5. Maintainability

#### 5.1 Code Quality
| Metric | Target | Measurement Method | Priority |
|--------|--------|-------------------|----------|
| Code Coverage (Backend) | > 90% | pytest-cov | High |
| Code Coverage (Frontend) | > 80% | Jest coverage | Medium |
| Linting Compliance (Python) | 100% | flake8, black | High |
| Linting Compliance (TypeScript) | 100% | ESLint, Prettier | High |
| Cyclomatic Complexity | < 10 per function | radon, SonarQube | Medium |
| Code Duplication | < 5% | SonarQube | Low |

**Acceptance Criteria**:
- All new code must meet coverage targets before merge
- CI/CD pipeline must enforce linting rules
- Complex functions must be refactored or documented

**Testing Approach**:
- Automated code quality checks in CI/CD
- Pre-commit hooks for linting
- Regular code review sessions

#### 5.2 Documentation
| Requirement | Implementation | Acceptance Criteria | Priority |
|------------|----------------|---------------------|----------|
| API Documentation | OpenAPI/Swagger spec | All endpoints documented with examples | High |
| Code Documentation | Docstrings for all public functions | 100% of public APIs documented | High |
| Deployment Guide | Step-by-step deployment instructions | Successfully deployable by new team member | High |
| Architecture Diagrams | System, database, deployment diagrams | Diagrams match actual implementation | Medium |
| User Manual | Admin and scorer user guides | User can complete tasks without support | Medium |

**Acceptance Criteria**:
- Documentation is kept up-to-date with code changes
- New developers can onboard within 2 days using documentation
- User manuals validated through user testing

#### 5.3 Modularity
| Requirement | Implementation | Testing Method | Priority |
|------------|----------------|----------------|----------|
| Scoring Engine Isolation | Pure functions, no database dependencies | Unit tests with mocked data | Critical |
| Service Layer Separation | Clear boundaries between services | Integration tests | High |
| Frontend Component Reusability | Atomic design principles | Component library documentation | Medium |

**Acceptance Criteria**:
- Scoring engine can be updated without modifying API layer
- Services can be tested independently
- UI components are reusable across different pages

### 6. Usability

#### 6.1 Mobile Scoring UI
| Metric | Target | Measurement Method | Priority |
|--------|--------|-------------------|----------|
| Touch Target Size | Minimum 44x44 px | Design system audit | High |
| Score Entry Completion Time | < 10 seconds per hole | User testing | High |
| Error Rate on Score Entry | < 2% | User testing, analytics | High |
| User Satisfaction Score | > 4/5 | Post-usage survey | Medium |

**Acceptance Criteria**:
- Scorers can enter 18-hole scores in under 3 minutes
- Score entry requires maximum 3 taps per hole
- Visual feedback confirms save within 1 second
- Works on devices with screen width down to 320px

**Testing Approach**:
- Usability testing with 5+ scorers
- A/B testing for UI variations
- Analytics tracking user flows

#### 6.2 Admin Dashboard
| Metric | Target | Measurement Method | Priority |
|--------|--------|-------------------|----------|
| Task Completion Time | < 2 minutes for common tasks | User testing | Medium |
| Learning Curve | < 30 minutes training for basic operations | Training session observation | Medium |
| Error Recovery | Clear error messages with actionable guidance | Error handling audit | High |

**Acceptance Criteria**:
- Admin can create a tournament and register 50 players in under 10 minutes
- Error messages include specific guidance on how to fix issues
- All critical actions have confirmation dialogs

#### 6.3 Accessibility
| Requirement | Standard | Testing Method | Priority |
|------------|----------|----------------|----------|
| Web Accessibility | WCAG 2.1 Level AA | Automated testing (axe, WAVE) | Medium |
| Keyboard Navigation | All interactive elements accessible | Manual testing | Medium |
| Screen Reader Support | Proper ARIA labels | NVDA/JAWS testing | Low |
| Color Contrast | Minimum 4.5:1 for normal text | Contrast checker | Medium |

**Acceptance Criteria**:
- No critical accessibility violations in automated testing
- All forms navigable via keyboard
- Color is not the only means of conveying information

### 7. Data Integrity

#### 7.1 Data Accuracy
| Requirement | Implementation | Testing Method | Priority |
|------------|----------------|----------------|----------|
| Scoring Calculation Accuracy | Match legacy system output 100% | Regression testing against historical data | Critical |
| Data Validation | Input validation at API and database levels | Validation testing, constraint testing | High |
| Referential Integrity | Foreign key constraints enforced | Database integrity tests | High |
| Audit Trail | All modifications logged with timestamp and user | Audit log verification | High |

**Acceptance Criteria**:
- Scoring engine produces identical results to legacy system for all test cases
- Invalid data cannot be saved to database
- All data modifications are traceable

#### 7.2 Data Backup & Recovery
| Metric | Target | Measurement Method | Priority |
|--------|--------|-------------------|----------|
| Backup Frequency | Daily automated backups | Backup job monitoring | High |
| Backup Retention | 30 days | Backup storage audit | Medium |
| Recovery Point Objective (RPO) | < 24 hours | Disaster recovery plan | High |
| Recovery Time Objective (RTO) | < 4 hours | Disaster recovery testing | High |
| Backup Verification | Weekly restore testing | Automated restore tests | High |

**Acceptance Criteria**:
- Automated daily backups complete successfully 99% of the time
- Full database restore completes within RTO
- Restored data passes integrity checks

### 8. Deployment & Operations

#### 8.1 Deployment
| Requirement | Implementation | Testing Method | Priority |
|------------|----------------|----------------|----------|
| Deployment Time | < 10 minutes (zero-downtime) | Deployment automation testing | High |
| Rollback Time | < 5 minutes | Rollback procedure testing | High |
| Environment Parity | Dev, staging, production identical | Configuration management audit | High |

**Acceptance Criteria**:
- Deployments can be triggered with a single command
- Rollback procedure is documented and tested monthly
- No manual configuration changes required

#### 8.2 Monitoring & Alerting
| Requirement | Implementation | Acceptance Criteria | Priority |
|------------|----------------|---------------------|----------|
| Application Metrics | Prometheus + Grafana | All critical metrics dashboarded | High |
| Error Tracking | Sentry or similar | All production errors captured and alerted | High |
| Log Aggregation | ELK Stack or CloudWatch | Logs searchable with 5-minute latency | High |
| Alerting | PagerDuty or similar | Critical alerts trigger within 1 minute | High |

**Acceptance Criteria**:
- Dashboards display real-time system health
- Critical errors trigger immediate alerts
- Logs retained for 90 days minimum

#### 8.3 Resource Utilization
| Metric | Target | Alert Threshold | Measurement Method | Priority |
|--------|--------|----------------|-------------------|----------|
| Backend CPU Usage | < 50% average | > 80% | Container monitoring | Medium |
| Backend Memory Usage | < 60% average | > 85% | Container monitoring | Medium |
| Database CPU Usage | < 60% average | > 80% | PostgreSQL monitoring | High |
| Database Storage Growth | < 1 GB/month | > 80% capacity | Disk monitoring | Medium |

**Acceptance Criteria**:
- Resource usage remains within targets under normal load
- Alerts trigger before resource exhaustion
- Auto-scaling configured for backend services

## NFR Testing Schedule

### Continuous Testing (CI/CD)
- Unit tests (code coverage)
- Linting and code quality checks
- Security vulnerability scanning
- API contract tests

### Weekly Testing
- Load testing (performance regression)
- Backup restoration verification
- Accessibility testing

### Monthly Testing
- Penetration testing
- Disaster recovery drills
- Performance benchmarking
- Usability testing

### Quarterly Testing
- Full security audit
- Capacity planning review
- Documentation review
- Technology upgrade assessment

## Acceptance Sign-Off

### Phase 1 (Architecture Design) - Complete when:
- [x] Database schema reviewed and approved
- [x] Architecture blueprint reviewed and approved
- [x] NFR metrics defined and approved
- [ ] Legacy system scoring logic documented

### Phase 2 (Core Development) - Complete when:
- [ ] All unit tests pass with > 90% coverage (backend)
- [ ] Scoring engine produces identical results to legacy system
- [ ] All API endpoints documented and tested
- [ ] Mobile scoring UI meets usability targets
- [ ] Admin dashboard and leaderboard functional

### Phase 3 (Testing & Deployment) - Complete when:
- [ ] All NFR targets met in load testing
- [ ] Data migration tool successfully migrates historical data
- [ ] Simulated UAT identifies no critical UX issues
- [ ] Production environment deployed with monitoring

### Phase 4 (Maintenance) - Ongoing:
- [ ] Documentation complete and up-to-date
- [ ] Monitoring and alerting operational
- [ ] Automated backups verified

---
**Document Version**: 1.0
**Last Updated**: 2024-11-08
**Status**: Final for Phase 1
