# Qwen-Specific Optimization Notes for Debugging

## Model Selection Strategy

### Qwen 7B for Debugging

- **Use Case**: Quick error identification and immediate solutions
- **Optimization**: Focus on error symptoms and basic troubleshooting
- **Context Management**: Keep prompts concise with clear error descriptions
- **Response Pattern**: Direct problem analysis with immediate debugging steps

### Qwen 14B for Debugging

- **Use Case**: Comprehensive debugging with moderate complexity analysis
- **Optimization**: Structured investigation with detailed root cause analysis
- **Context Management**: Full context utilization for thorough problem understanding
- **Response Pattern**: Systematic debugging approach with validation steps

### Qwen 72B for Debugging

- **Use Case**: Complex system debugging and architectural issue resolution
- **Optimization**: Extensive context with deep system analysis
- **Context Management**: Leverage full context for comprehensive system understanding
- **Response Pattern**: Strategic debugging with long-term prevention strategies

## Prompt Engineering Techniques

### Error Context Optimization

```markdown
**Error Information Structure:**

1. Complete error message and stack trace
2. System configuration and environment details
3. Reproduction steps and conditions
4. Expected vs actual behavior description
5. Recent changes that may be related
```

### Debugging Strategy Enhancement

- **Systematic Approach**: Request structured problem-solving frameworks
- **Hypothesis Testing**: Encourage multiple hypothesis generation and validation
- **Root Cause Focus**: Prioritize fundamental cause identification over symptoms
- **Solution Validation**: Include testing and verification strategies

### Production Debugging Considerations

- **Minimal Impact**: Emphasize non-invasive debugging techniques
- **Monitoring Integration**: Leverage existing monitoring and alerting systems
- **Rollback Planning**: Include rollback strategies for debugging-related changes
- **Documentation**: Document all debugging activities for compliance and learning

## Advanced Debugging Patterns

### Multi-Layered Error Analysis

```markdown
**Investigation Layers:**

1. **Symptom Layer**: Observable error symptoms and user impact
2. **Code Layer**: Code path analysis and logic validation
3. **Data Layer**: Data state and transformation verification
4. **Integration Layer**: Component interaction and dependency analysis
5. **Infrastructure Layer**: System and environment configuration review
```

### Debugging Workflow Optimization

- **Reproduction First**: Prioritize reliable error reproduction capability
- **Isolation Strategy**: Implement systematic variable and component isolation
- **Instrumentation Planning**: Strategic logging and monitoring placement
- **Validation Framework**: Comprehensive testing for debugging activities

## Integration with Agent Zero

### Debugging Workflow Integration

- **Error Monitoring**: Automated error detection and reporting integration
- **Debugging Sessions**: Structured debugging process with progress tracking
- **Knowledge Base**: Common issues and solutions documentation system
- **Team Collaboration**: Shared debugging insights and collaborative problem-solving

### Automation and Tool Integration

- **Static Analysis**: Integration with linting and static analysis tools
- **Dynamic Analysis**: Runtime debugging and profiling tool integration
- **Log Aggregation**: Centralized logging and analysis system integration
- **Performance Monitoring**: Real-time system health and debugging visualization

## Specialized Debugging Scenarios

### Performance Debugging Optimization

- **Profiling Integration**: Memory and CPU profiling tool integration
- **Baseline Establishment**: Performance baseline creation and tracking
- **Load Testing**: Systematic load testing for performance issue reproduction
- **Optimization Validation**: Performance improvement measurement and validation

### Logic Error Debugging Enhancement

- **Algorithm Validation**: Systematic algorithm and logic validation techniques
- **Edge Case Analysis**: Comprehensive edge case and boundary condition testing
- **Mathematical Verification**: Numerical computation accuracy validation
- **Business Logic Alignment**: Business requirement and implementation alignment
