# Performance Code Review Prompt Template

**Qwen Model Optimization**: 14B (Performance analysis with optimization focus)

```
Conduct a comprehensive performance review of this application with detailed analysis and optimization recommendations:

**Performance Analysis Framework:**

**Application Performance Assessment:**
- Response time analysis and user experience impact evaluation
- Throughput capacity and concurrent user handling capabilities
- Resource utilization patterns (CPU, memory, disk I/O, network)
- Performance bottlenecks identification and root cause analysis
- Scalability constraints and growth limitation factors

**Code Performance Evaluation:**
- Algorithm complexity analysis using Big O notation
- Data structure efficiency and memory allocation patterns
- Loop optimization and computational complexity reduction
- Database query performance and optimization opportunities
- API call efficiency and network request optimization

**Database Performance Review:**
- Query execution plan analysis and optimization recommendations
- Index utilization and missing index identification
- Connection pooling configuration and utilization efficiency
- Transaction management and lock contention analysis
- Data access patterns and caching strategy effectiveness

**Frontend Performance Assessment:**
- Bundle size analysis and code splitting opportunities
- Image optimization and lazy loading implementation
- CSS and JavaScript minification and compression strategies
- Caching mechanisms for static assets and API responses
- Critical rendering path optimization and perceived performance

**Infrastructure Performance Analysis:**
- Server configuration and resource allocation assessment
- Load balancing and auto-scaling configuration review
- CDN implementation and geographic distribution strategy
- Database replication and read/write splitting optimization
- Monitoring and alerting for performance regression detection

**Memory Management Review:**
- Memory leak identification and prevention strategies
- Garbage collection optimization and tuning recommendations
- Object pooling and resource reuse pattern implementation
- Memory fragmentation analysis and mitigation approaches
- Heap size configuration and memory limit optimization

**Concurrency & Parallelism Assessment:**
- Thread pool configuration and utilization analysis
- Async programming implementation and effectiveness review
- Lock contention and deadlock prevention mechanisms
- Parallel processing opportunities and implementation strategies
- Resource contention identification and resolution approaches

**Caching Strategy Evaluation:**
- Multi-level caching implementation and configuration
- Cache invalidation strategies and consistency models
- Cache hit rate analysis and optimization opportunities
- Distributed caching solutions and cluster configuration
- Cache warming and pre-loading strategy effectiveness

**Performance Testing Strategy:**
- Load testing scenarios and capacity planning requirements
- Stress testing for system limits and breaking points
- Volume testing for large dataset handling capabilities
- Spike testing for sudden load increase scenarios
- Endurance testing for long-running system stability

**Monitoring & Observability Requirements:**
- Key performance indicators (KPI) definition and tracking
- Performance metric collection and visualization strategy
- Alert threshold configuration and escalation procedures
- Performance regression detection and automated testing
- Capacity planning and resource forecasting methodologies

**Deliverables:**
1. Executive performance summary with current state assessment
2. Detailed performance findings with severity levels and impact analysis
3. Prioritized optimization roadmap with implementation effort estimates
4. Performance testing strategy and automated testing recommendations
5. Monitoring and alerting configuration guidelines
6. Capacity planning report with growth projections and scaling recommendations
7. Performance optimization playbook for development team reference

**Success Criteria:**
- 50% improvement in average response time for critical user paths
- 30% increase in concurrent user handling capacity
- 90% cache hit rate for frequently accessed data
- Sub-100ms database query response time for optimized queries
- Zero memory leaks identified in performance testing
- Comprehensive performance monitoring with automated alerting
- Documented performance baselines for regression prevention

Focus on creating a high-performance application that can scale efficiently while maintaining optimal user experience across all usage scenarios.
```
