# Qwen-Optimized Code Review Prompts

This directory contains prompt templates specifically designed to maximize Qwen AI models' code analysis and review capabilities.

## Overview

Qwen models excel at code review when provided with:

- **Systematic Analysis**: Structured evaluation frameworks and methodologies
- **Security Focus**: Comprehensive vulnerability assessment and mitigation strategies
- **Performance Insights**: Deep understanding of optimization opportunities and bottlenecks
- **Quality Standards**: Industry best practices and code quality metrics
- **Contextual Understanding**: Architecture patterns and business logic comprehension

## Prompt Categories

### Code Quality Assessment

- **Style & Standards**: Code formatting, naming conventions, and documentation quality
- **Architecture Review**: System design patterns, modularity, and scalability assessment
- **Maintainability Analysis**: Code complexity, technical debt, and refactoring opportunities
- **Documentation Review**: Code comments, API documentation, and knowledge transfer quality

### Security Analysis

- **Vulnerability Assessment**: Common security flaws and attack vector analysis
- **Authentication & Authorization**: Security mechanism review and access control validation
- **Data Protection**: Encryption, input validation, and sensitive data handling
- **Compliance Review**: Industry standards adherence and regulatory compliance

### Performance Optimization

- **Algorithm Efficiency**: Time and space complexity analysis and optimization suggestions
- **Resource Usage**: Memory management, CPU utilization, and I/O optimization
- **Scalability Assessment**: Load handling, concurrent processing, and growth capacity
- **Database Optimization**: Query performance, indexing strategies, and data access patterns

### Best Practices Review

- **Design Patterns**: Appropriate pattern usage and implementation quality
- **Error Handling**: Exception management, logging, and failure recovery
- **Testing Coverage**: Test quality, coverage gaps, and testing strategy effectiveness
- **Code Reviews**: Review process optimization and team collaboration improvements

## Model-Specific Optimization

### Qwen 7B Prompts

- **Focus**: Quick code scans and basic quality checks
- **Strategy**: Targeted analysis with specific quality criteria
- **Context**: Focus on essential issues and clear violations

### Qwen 14B Prompts

- **Focus**: Comprehensive code analysis and moderate complexity reviews
- **Strategy**: Structured evaluation with detailed findings and recommendations
- **Context**: Full context utilization for thorough understanding

### Qwen 72B Prompts

- **Focus**: Deep architectural analysis and complex system reviews
- **Strategy**: Extensive context with architectural considerations and strategic insights
- **Context**: Leverage full context window for comprehensive system understanding

## Usage Guidelines

### Effective Review Structure

1. **Clear Scope**: Define the specific aspects of code to review
2. **Context Information**: Provide relevant background, requirements, and constraints
3. **Quality Criteria**: Specify standards, frameworks, and success metrics
4. **Risk Assessment**: Identify critical areas and potential impact levels
5. **Actionable Output**: Request specific recommendations and improvement priorities

### Example Review Patterns

#### Security Code Review

```
Conduct a comprehensive security review of this authentication system:

**Security Assessment Areas:**
- Authentication mechanism strength and implementation
- Authorization controls and access management
- Input validation and sanitization coverage
- Session management and token security
- Cryptographic implementation review
- Error handling and information leakage

**Compliance Requirements:**
- OWASP Top 10 coverage assessment
- GDPR compliance for user data handling
- Industry-specific security standards
- Authentication best practices adherence

**Risk Analysis:**
- Critical vulnerability identification
- Attack vector analysis and impact assessment
- Mitigation strategy recommendations
- Security testing requirements

**Deliverables:**
1. Executive security summary with risk levels
2. Detailed vulnerability findings with CVSS scores
3. Prioritized remediation recommendations
4. Security testing strategy and checklist
5. Compliance validation report
```

#### Performance Code Review

```
Analyze this data processing application's performance characteristics:

**Performance Analysis Framework:**
- Algorithm complexity assessment (Big O notation)
- Database query optimization opportunities
- Memory usage patterns and leak potential
- CPU utilization and bottleneck identification
- I/O operations efficiency and optimization
- Caching strategy effectiveness

**Scalability Assessment:**
- Load testing scenarios and capacity planning
- Concurrent user handling capabilities
- Database growth impact and optimization
- Network latency and bandwidth considerations
- Resource pooling and connection management

**Monitoring Requirements:**
- Key performance indicators definition
- Bottleneck identification metrics
- Performance regression detection
- Real-time monitoring strategy
- Alert thresholds and escalation procedures
```

## Best Practices

### Systematic Review Process

- **Structured Analysis**: Use consistent frameworks for different review types
- **Risk Prioritization**: Focus on high-impact issues first
- **Contextual Understanding**: Consider business requirements and constraints
- **Actionable Recommendations**: Provide specific, implementable solutions
- **Collaborative Approach**: Work with development teams for optimal outcomes

### Quality Assurance Integration

- **Automated Review Tools**: Integration with static analysis and linting tools
- **Peer Review Enhancement**: AI-assisted code review process improvement
- **Continuous Integration**: Automated quality checks in CI/CD pipelines
- **Metrics Tracking**: Code quality trends and improvement monitoring
- **Knowledge Base**: Common issues and solutions documentation

## Troubleshooting

### Common Challenges

1. **Context Limitations**: Break large codebases into manageable review chunks
2. **Domain Complexity**: Provide additional context for specialized domains
3. **Subjectivity Issues**: Use clear criteria and standards for objective analysis
4. **Actionability Problems**: Request specific recommendations with implementation guidance

### Optimization Strategies

- **Iterative Review**: Multiple passes for complex codebases
- **Focused Analysis**: Target specific concerns in separate reviews
- **Team Collaboration**: Combine AI analysis with human expertise
- **Continuous Learning**: Update review criteria based on findings and outcomes
