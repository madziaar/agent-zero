# Data Pipeline Development Prompt

**Qwen Model Optimization**: 72B (Complex data processing with optimization requirements)

```
Design and implement a scalable data pipeline for real-time log analytics:

**Pipeline Requirements:**
- Ingest log data from multiple sources (applications, servers, containers)
- Parse and structure log entries with timestamp extraction
- Filter and transform data based on configurable rules
- Aggregate metrics in real-time windows (1min, 5min, 1hour)
- Store processed data in data lake for historical analysis
- Generate alerts for anomaly detection
- Provide API for querying aggregated metrics

**Architecture Components:**
- Apache Kafka for message queuing and stream processing
- Apache Flink for real-time stream processing
- Elasticsearch for full-text search and analytics
- Redis for caching and fast lookups
- PostgreSQL for metadata and configuration storage
- MinIO for data lake storage
- Grafana for visualization and alerting

**Data Processing Features:**
- Multi-format log parsing (JSON, plain text, structured)
- Real-time aggregation with sliding/tumbling windows
- Anomaly detection using statistical methods
- Data quality validation and error handling
- Schema evolution support for changing log formats
- Compression and encryption for stored data

**Scalability Requirements:**
- Horizontal scaling across multiple nodes
- Partitioning strategy for parallel processing
- Load balancing for even distribution
- Fault tolerance with checkpointing and recovery
- Auto-scaling based on throughput metrics
- Multi-region deployment support

**Performance Targets:**
- End-to-end latency <100ms for real-time processing
- Throughput >1M events/second per node
- Storage optimization with data deduplication
- Query response time <1s for dashboard queries
- 99.9% uptime with automated recovery
- Efficient resource utilization (<70% CPU average)

**Monitoring & Observability:**
- Comprehensive metrics collection (throughput, latency, errors)
- Distributed tracing for request flow analysis
- Log aggregation and analysis
- Performance dashboards and alerting
- Capacity planning and forecasting
- SLA monitoring and reporting

**Code Quality Standards:**
- Infrastructure as Code with Terraform/Kubernetes
- CI/CD pipeline with automated testing
- Configuration management with version control
- Documentation with runbooks and procedures
- Security hardening and compliance
- Performance benchmarking and optimization

**Technology Stack:**
- Programming Language: Python (for data processing logic)
- Stream Processing: Apache Flink with Python API
- Message Queue: Apache Kafka with Python client
- Database: PostgreSQL with async Python driver
- Cache: Redis with connection pooling
- Storage: MinIO (S3-compatible) with boto3
- Monitoring: Prometheus, Grafana, ELK stack

**Implementation Phases:**
1. **Infrastructure Setup** - Kafka, Flink, Elasticsearch clusters
2. **Data Ingestion** - Log collection agents and Kafka producers
3. **Stream Processing** - Flink jobs for real-time analytics
4. **Data Storage** - Elasticsearch indexing and MinIO storage
5. **API Development** - REST API for querying and configuration
6. **Monitoring Setup** - Metrics, logging, and alerting
7. **Testing & Validation** - Load testing and performance validation

**Deliverables:**
1. Complete Flink application with all processing logic
2. Kafka producer/consumer implementations
3. Elasticsearch index mappings and queries
4. REST API with FastAPI framework
5. Docker containers and Kubernetes manifests
6. Infrastructure as Code templates
7. Monitoring and alerting configuration
8. Performance test scripts and benchmarks
9. Operations documentation and runbooks

**Success Metrics:**
- Process 1M+ log events per second
- Maintain <100ms end-to-end latency
- Achieve >99.9% data accuracy
- Scale to 10x traffic without code changes
- Automated recovery from failures
- Comprehensive test coverage >95%

Create a production-ready data pipeline that can handle massive scale while maintaining data quality and system reliability.
```
