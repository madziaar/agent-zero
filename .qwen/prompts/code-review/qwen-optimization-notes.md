# Qwen-Specific Optimization Notes for Code Review

## Model Selection Strategy

### Qwen 7B for Code Review

- **Use Case**: Quick code scans and basic quality assessments
- **Optimization**: Focus on clear violations and obvious issues
- **Context Management**: Keep prompts concise with specific quality criteria
- **Response Pattern**: Direct issue identification with immediate recommendations

### Qwen 14B for Code Review

- **Use Case**: Comprehensive code analysis and moderate complexity reviews
- **Optimization**: Structured evaluation with detailed findings
- **Context Management**: Utilize full context for thorough understanding
- **Response Pattern**: Balanced analysis with actionable recommendations

### Qwen 72B for Code Review

- **Use Case**: Deep architectural analysis and complex system reviews
- **Optimization**: Extensive context with strategic insights
- **Context Management**: Leverage full context window for comprehensive understanding
- **Response Pattern**: Strategic analysis with long-term improvement roadmaps

## Prompt Engineering Techniques

### Context Optimization

```markdown
**Context Structure:**

1. Clear review scope and objectives
2. Specific quality criteria and standards
3. Technical constraints and requirements
4. Business context and impact assessment
5. Success criteria and acceptance standards
```

### Quality Focus Enhancement

- **Explicit Standards**: Clearly specify coding standards and quality metrics
- **Risk Prioritization**: Focus on high-impact issues first
- **Actionable Output**: Request specific recommendations with implementation guidance
- **Validation Criteria**: Include clear acceptance and quality criteria

### Iterative Review Strategy

- **Incremental Analysis**: Break large codebases into manageable review chunks
- **Focused Reviews**: Target specific concerns in separate review passes
- **Progressive Detail**: Start with high-level review, then dive into specifics
- **Validation Loops**: Use follow-up reviews to validate implementations

## Integration with Agent Zero

### Workflow Integration

- **Pre-commit Hooks**: Automated code review before commits
- **Pull Request Reviews**: Comprehensive PR analysis and feedback
- **Quality Gates**: Automated quality checks in CI/CD pipeline
- **Team Collaboration**: Shared review insights and team learning

### Customization Strategy

- **Team Standards**: Incorporate team-specific coding standards
- **Domain Knowledge**: Include industry-specific best practices
- **Project Context**: Consider project-specific requirements and constraints
- **Continuous Learning**: Update review criteria based on findings and outcomes

```

## Integration with Agent Zero

### Workflow Integration
- **Pre-commit Hooks**: Automated code review before commits
- **Pull Request Reviews**: Comprehensive PR analysis and feedback
- **Quality Gates**: Automated quality checks in CI/CD pipeline
- **Team Collaboration**: Shared review insights and team learning

### Customization Strategy
- **Team Standards**: Incorporate team-specific coding standards
- **Domain Knowledge**: Include industry-specific best practices
- **Project Context**: Consider project-specific requirements and constraints
- **Continuous Learning**: Update review criteria based on findings and outcomes
```
