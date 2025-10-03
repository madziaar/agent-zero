# Qwen-Optimized Debugging Prompts

This directory contains prompt templates specifically designed to maximize Qwen AI models' debugging and troubleshooting capabilities.

## Overview

Qwen models excel at debugging when provided with:

- **Systematic Analysis**: Structured problem-solving frameworks and methodologies
- **Root Cause Identification**: Deep understanding of error patterns and failure modes
- **Diagnostic Strategies**: Comprehensive troubleshooting approaches and validation techniques
- **Solution Validation**: Testing and verification of proposed fixes
- **Preventive Insights**: Learning from issues to prevent future occurrences

## Prompt Categories

### Error Diagnosis & Analysis

- **Runtime Errors**: Exception handling, stack trace analysis, and error pattern recognition
- **Logic Errors**: Algorithm flaws, incorrect implementations, and behavioral issues
- **Performance Issues**: Bottleneck identification, resource exhaustion, and optimization problems
- **Integration Problems**: API failures, dependency conflicts, and compatibility issues

### Debugging Strategies

- **Interactive Debugging**: Step-by-step problem isolation and hypothesis testing
- **Log Analysis**: Error log interpretation, pattern recognition, and diagnostic information extraction
- **Code Instrumentation**: Strategic debugging code placement and trace point identification
- **Test Case Development**: Targeted test creation for issue reproduction and validation

### Environment-Specific Debugging

- **Development Environment**: Local development setup issues and configuration problems
- **Production Debugging**: Live system analysis, minimal-invasive troubleshooting
- **Container Issues**: Docker, Kubernetes, and orchestration-related problems
- **Cloud Platform**: AWS, Azure, GCP specific issues and service interactions

### Application Domain Debugging

- **Web Applications**: Frontend, backend, database, and network-related issues
- **Data Processing**: ETL pipeline failures, data quality issues, and transformation errors
- **Machine Learning**: Model training problems, inference issues, and data pipeline failures
- **Microservices**: Service communication, distributed tracing, and coordination problems

## Model-Specific Optimization

### Qwen 7B Prompts

- **Focus**: Quick error identification and immediate solutions
- **Strategy**: Direct problem analysis with straightforward debugging steps
- **Context**: Focus on error symptoms and basic troubleshooting

### Qwen 14B Prompts

- **Focus**: Comprehensive debugging with moderate complexity analysis
- **Strategy**: Structured investigation with detailed root cause analysis
- **Context**: Full context utilization for thorough problem understanding

### Qwen 72B Prompts

- **Focus**: Complex system debugging and architectural issue resolution
- **Strategy**: Extensive context with deep system analysis and strategic solutions
- **Context**: Leverage full context window for comprehensive system understanding

## Usage Guidelines

### Effective Debugging Structure

1. **Problem Definition**: Clear description of symptoms, expected vs actual behavior
2. **Environment Context**: System configuration, versions, dependencies, and recent changes
3. **Error Information**: Complete error messages, stack traces, and log excerpts
4. **Reproduction Steps**: Detailed steps to reproduce the issue consistently
5. **Expected Resolution**: Specific criteria for successful problem resolution

### Example Debugging Patterns

#### Runtime Error Analysis

```
Debug this critical application crash with detailed root cause analysis:

**Error Context:**
- Complete error message and stack trace
- System configuration and environment details
- Recent code changes or deployments
- Frequency and conditions of occurrence

**Diagnostic Strategy:**
- Step-by-step error reproduction verification
- Code path analysis leading to the error
- Variable state examination at key points
- External dependency and resource validation

**Root Cause Investigation:**
- Exception hierarchy and error propagation analysis
- Resource availability and constraint checking
- Concurrency and timing-related issue assessment
- Configuration and environment mismatch identification

**Solution Development:**
1. Immediate workaround for production stability
2. Permanent fix with proper error handling
3. Prevention measures for similar issues
4. Testing strategy for fix validation
5. Documentation for future reference
```

#### Performance Issue Investigation

```
Investigate this application slowdown with comprehensive performance analysis:

**Performance Symptoms:**
- Specific performance degradation description
- Load conditions and timing information
- Resource utilization patterns (CPU, memory, I/O)
- User experience impact assessment

**Profiling Strategy:**
- Code instrumentation for performance monitoring
- Database query analysis and optimization opportunities
- Memory usage patterns and leak detection
- Network and external service performance impact

**Bottleneck Identification:**
- Critical path analysis and timing breakdown
- Resource contention and locking issues
- Algorithm complexity and data structure efficiency
- Caching strategy effectiveness evaluation

**Optimization Plan:**
1. Immediate performance improvement measures
2. Long-term architectural optimizations
3. Monitoring and alerting strategy
4. Load testing and capacity planning
5. Continuous performance tracking implementation
```

## Best Practices

### Systematic Debugging Process

- **Scientific Method**: Formulate hypotheses, test systematically, validate conclusions
- **Isolation Technique**: Isolate variables and components for focused analysis
- **Documentation**: Maintain debugging logs, findings, and resolution steps
- **Collaboration**: Work with domain experts and team members for comprehensive insight
- **Learning**: Document patterns and prevention strategies for future issues

### Production Debugging Considerations

- **Minimal Impact**: Use non-invasive debugging techniques in production
- **Monitoring Integration**: Leverage existing monitoring and alerting systems
- **Rollback Planning**: Prepare rollback strategies for debugging-related changes
- **Communication**: Keep stakeholders informed during debugging process
- **Documentation**: Document all debugging activities for compliance and learning

## Troubleshooting

### Common Debugging Challenges

1. **Non-Reproducible Issues**: Implement comprehensive logging and monitoring
2. **Complex Dependencies**: Use dependency injection and mocking for isolation
3. **Timing Issues**: Implement proper synchronization and concurrency controls
4. **Resource Constraints**: Monitor resource usage and implement proper cleanup

### Debugging Tool Integration

- **IDE Integration**: Utilize debugging features of development environments
- **Profiler Tools**: Performance profiling and memory analysis tools
- **Log Aggregation**: Centralized logging and analysis systems
- **Monitoring Dashboards**: Real-time system health and performance visualization
- **Version Control Integration**: Track changes and correlate with issue occurrence
