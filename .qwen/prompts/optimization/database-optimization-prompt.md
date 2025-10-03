# Database Optimization Prompt Template

**Qwen Model Optimization**: 14B (Database performance with query optimization focus)

```
Optimize this database system for maximum performance, scalability, and efficiency:

**Database Performance Assessment:**

**Current Database Analysis:**
- Database engine version and configuration assessment
- Schema design review and normalization opportunities
- Data volume and growth patterns analysis
- Query performance baseline and bottleneck identification
- Resource utilization and capacity constraint evaluation

**Query Optimization Strategy:**
- Query execution plan analysis and performance improvement
- Index utilization assessment and missing index recommendations
- Query rewriting for optimal performance and readability
- Stored procedure and function optimization and tuning
- Subquery and join optimization for complex operations

**Index Optimization Implementation:**
- Existing index analysis and usage pattern evaluation
- Missing index identification and creation strategy
- Index maintenance and fragmentation management
- Composite index design and selectivity optimization
- Index naming conventions and documentation standards

**Schema Design Optimization:**
- Table design review and normalization strategy refinement
- Data type selection for performance and storage efficiency
- Constraint implementation for data integrity and performance
- Partitioning strategy for large table management
- Archive and purge policy implementation for data lifecycle

**Connection & Transaction Management:**
- Connection pool configuration and utilization optimization
- Transaction scope and isolation level tuning
- Lock contention analysis and deadlock prevention
- Connection timeout and retry strategy implementation
- Transaction log management and recovery optimization

**Data Access Layer Optimization:**
- ORM configuration and query generation optimization
- Repository pattern implementation and caching strategies
- Lazy loading vs eager loading strategy optimization
- Batch operation implementation for bulk data operations
- Connection lifecycle management and resource cleanup

**Database Configuration Tuning:**
- Memory allocation and buffer pool configuration
- CPU affinity and thread configuration optimization
- Storage configuration and I/O optimization strategies
- Network configuration and connection parameter tuning
- Backup and maintenance window optimization

**Scalability Strategy Implementation:**
- Read replica configuration and load distribution strategy
- Database sharding and partitioning implementation
- Master-slave replication configuration and monitoring
- Horizontal and vertical scaling strategy development
- Geographic distribution and data localization planning

**Monitoring & Performance Tracking:**
- Database performance metric collection and analysis
- Query performance monitoring and slow query detection
- Lock and deadlock monitoring and alerting configuration
- Resource utilization tracking and capacity forecasting
- Performance regression detection and automated testing

**Security & Compliance Optimization:**
- Authentication and authorization mechanism review
- Encryption implementation for data at rest and in transit
- Audit logging and compliance reporting configuration
- Access pattern analysis and privilege optimization
- Backup encryption and secure data handling procedures

**Maintenance & Operational Excellence:**
- Automated maintenance task scheduling and configuration
- Statistics update strategy and histogram maintenance
- Index defragmentation and rebuild scheduling
- Backup strategy optimization and recovery testing
- Disaster recovery planning and high availability configuration

**Migration & Upgrade Strategy:**
- Database version upgrade planning and testing
- Schema migration strategy and rollback procedures
- Data migration performance optimization and validation
- Application compatibility testing and validation
- Production deployment strategy and rollback planning

**Deliverables:**
1. Database performance assessment report with optimization opportunities
2. Query optimization recommendations with before/after comparisons
3. Index strategy and implementation plan with performance impact estimates
4. Schema optimization recommendations and migration strategy
5. Database configuration tuning guide and best practice implementation
6. Monitoring and alerting framework for ongoing performance management
7. Maintenance and operational procedures for sustained optimization

**Success Criteria:**
- 70% improvement in query response time for critical operations
- 50% reduction in database resource utilization under normal load
- Zero deadlocks in concurrent transaction scenarios
- 99% index utilization rate for optimal query performance
- Comprehensive monitoring with proactive alerting for performance issues
- Automated maintenance procedures for ongoing optimization
- Documented backup and recovery procedures with tested reliability
- Team capability for ongoing database performance management

Focus on delivering a high-performance, scalable database solution that supports current and future application requirements while maintaining data integrity and operational excellence.
```
