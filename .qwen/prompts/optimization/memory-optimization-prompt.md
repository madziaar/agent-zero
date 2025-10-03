# Memory Optimization Prompt Template

**Qwen Model Optimization**: 14B (Memory management with leak prevention and efficiency focus)

```
Optimize this application's memory usage for improved performance and stability:

**Memory Usage Analysis:**

**Current Memory Assessment:**
- Memory consumption patterns and peak usage identification
- Memory leak detection and analysis using profiling tools
- Garbage collection behavior and performance impact assessment
- Memory fragmentation issues and heap utilization patterns
- Application lifecycle memory behavior and trend analysis

**Memory Leak Investigation:**
- Object retention analysis and reference management review
- Event listener and callback cleanup verification
- Cache implementation and memory accumulation assessment
- Static reference identification and elimination strategies
- Resource disposal pattern implementation and validation

**Heap Memory Optimization:**
- Heap size configuration and JVM/container tuning
- Memory allocation patterns and object pooling opportunities
- Large object handling and memory chunk management
- Heap fragmentation analysis and defragmentation strategies
- Memory pressure monitoring and alerting configuration

**Stack Memory Management:**
- Thread stack size configuration and optimization
- Recursive algorithm optimization and tail recursion implementation
- Local variable management and scope optimization
- Function call optimization and inlining opportunities
- Stack overflow prevention and monitoring strategies

**Native Memory Optimization:**
- Native library memory usage analysis and optimization
- JNI implementation review and memory management assessment
- Off-heap memory usage patterns and allocation strategies
- Native memory leak detection and prevention techniques
- Platform-specific memory management best practices

**Application-Specific Memory Strategies:**
- Collection and data structure memory optimization
- Streaming and lazy loading implementation for large datasets
- Image and media resource memory management optimization
- Database connection and result set memory handling
- Network buffer and I/O memory usage optimization

**Caching Memory Management:**
- Cache size configuration and memory limit strategies
- Cache eviction policies and memory pressure handling
- Distributed cache memory usage and cluster optimization
- Cache warming strategies and memory pre-allocation
- Cache serialization and memory overhead assessment

**Memory Monitoring & Profiling:**
- Memory usage metric collection and trend analysis
- Heap dump analysis and memory leak identification
- Real-time memory monitoring and alerting configuration
- Memory profiler integration and automated analysis
- Performance benchmarking for memory optimization validation

**Garbage Collection Tuning:**
- GC algorithm selection and configuration optimization
- GC pause time reduction and throughput maximization
- Generational garbage collection tuning and parameters
- GC monitoring and diagnostic information analysis
- GC performance impact assessment and optimization

**Memory-Efficient Architecture:**
- Immutable object pattern implementation for reduced allocations
- Object pooling and reuse strategy development
- Flyweight pattern application for memory conservation
- Lazy initialization and deferred object creation
- Memory-mapped file usage for large data handling

**Resource Management Enhancement:**
- Resource acquisition and disposal pattern implementation
- Try-with-resources pattern adoption and best practices
- Finalizer usage review and elimination strategies
- Weak and soft reference usage for memory-sensitive caching
- Resource leak detection and automated testing integration

**Performance Testing for Memory:**
- Memory stress testing and leak detection validation
- Load testing with memory usage monitoring and analysis
- Memory usage regression testing and trend validation
- OutOfMemoryError prevention and graceful degradation
- Memory usage benchmarking and performance comparison

**Production Memory Management:**
- Production memory monitoring and alerting strategies
- Memory dump analysis procedures for incident response
- Memory optimization validation in staging environments
- Memory usage capacity planning and forecasting
- Memory-related incident post-mortem and improvement

**Deliverables:**
1. Memory usage analysis report with leak identification and optimization opportunities
2. Memory optimization implementation plan with performance impact estimates
3. Memory monitoring and alerting framework configuration
4. Garbage collection tuning recommendations and implementation guide
5. Memory leak prevention strategies and coding standards
6. Resource management best practices and implementation guidelines
7. Memory performance testing strategy and automated validation

**Success Criteria:**
- Zero memory leaks identified in extended load testing scenarios
- 30% reduction in overall memory consumption for typical workloads
- Garbage collection pause times maintained under 100ms thresholds
- Memory usage growth stabilized and predictable under load
- Comprehensive memory monitoring with proactive leak detection
- Documented memory management procedures for development team
- Memory optimization best practices adopted across codebase
- Production memory incidents reduced to zero for optimized components

Focus on delivering a memory-efficient application that maintains optimal performance while preventing memory-related stability issues and providing a solid foundation for scalable growth.
```
