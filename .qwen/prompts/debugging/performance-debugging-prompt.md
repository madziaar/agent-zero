# Performance Debugging Prompt Template

**Qwen Model Optimization**: 14B (Performance issue analysis with optimization focus)

```
Debug this performance issue with comprehensive analysis and optimization strategy:

**Performance Issue Assessment:**

**Symptom Analysis:**
- Detailed description of performance degradation
- Specific metrics showing performance impact
- User experience effects and business impact
- Conditions under which performance issues occur
- Recent changes that may have introduced the problem

**Resource Utilization Analysis:**
- CPU usage patterns and bottleneck identification
- Memory consumption and potential leak detection
- Disk I/O patterns and storage performance impact
- Network utilization and bandwidth constraints
- Database performance and query execution analysis

**Application Profiling Strategy:**
- Code instrumentation for performance monitoring
- Hotspot identification using profiling tools
- Call stack analysis for performance bottleneck tracing
- Memory allocation patterns and garbage collection impact
- Thread and concurrency performance characteristics

**Database Performance Investigation:**
- Query execution plan analysis and optimization opportunities
- Index utilization and missing index recommendations
- Connection pool configuration and utilization efficiency
- Lock contention and deadlock situation assessment
- Data volume and growth impact on performance

**External Dependencies Analysis:**
- API response times and external service performance
- Third-party library and framework performance impact
- Network latency and bandwidth utilization patterns
- CDN and caching layer effectiveness evaluation
- Load balancer and infrastructure performance assessment

**Code-Level Performance Review:**
- Algorithm complexity assessment and optimization opportunities
- Data structure efficiency and memory allocation patterns
- Loop optimization and computational complexity reduction
- Caching strategy implementation and effectiveness
- I/O operation efficiency and blocking call identification

**Concurrency & Parallelism Issues:**
- Thread pool configuration and utilization analysis
- Lock contention and synchronization bottleneck identification
- Race condition and timing-related performance problems
- Resource contention and blocking operation assessment
- Async programming implementation effectiveness

**Caching & Memory Management:**
- Cache hit rate analysis and optimization opportunities
- Memory leak identification and prevention strategies
- Object pooling and resource reuse effectiveness
- Garbage collection tuning and memory pressure assessment
- Buffer and stream management optimization

**Monitoring & Measurement Setup:**
- Key performance indicator definition and tracking
- Performance baseline establishment for comparison
- Alert threshold configuration for proactive detection
- Trend analysis and performance regression identification
- Capacity planning and resource forecasting

**Immediate Performance Improvements:**
- Quick wins and immediate optimization opportunities
- Temporary performance patches for urgent relief
- Configuration tuning for immediate impact
- Resource allocation adjustments for quick improvement
- Caching enhancements for rapid response time improvement

**Long-term Performance Strategy:**
- Architectural improvements for sustained performance
- Code refactoring for efficiency and maintainability
- Infrastructure upgrades and scaling strategy implementation
- Performance testing and continuous optimization culture
- Monitoring and alerting for ongoing performance management

**Deliverables:**
1. Performance analysis report with root cause identification
2. Immediate optimization recommendations with impact estimates
3. Long-term performance improvement roadmap
4. Monitoring and alerting configuration guidelines
5. Performance testing strategy and automation recommendations
6. Capacity planning and scaling strategy documentation
7. Team training materials for performance optimization

**Success Criteria:**
- Performance issue completely resolved with measurable improvement
- Monitoring and alerting in place for performance regression detection
- Performance baselines established for ongoing tracking
- Team capability enhanced for performance issue prevention
- Documentation updated for future performance optimization reference
- Automated performance testing integrated into development lifecycle

Focus on delivering a comprehensive performance debugging solution that provides immediate relief while establishing long-term performance optimization practices.
```
