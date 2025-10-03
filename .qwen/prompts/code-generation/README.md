# Qwen-Optimized Code Generation Prompts

This directory contains prompt templates specifically designed to maximize Qwen AI models' coding capabilities.

## Overview

Qwen models excel at code generation when provided with:

- **Clear Context**: Well-defined problem statements and requirements
- **Structured Information**: Organized requirements and constraints
- **Incremental Tasks**: Breaking complex tasks into manageable steps
- **Quality Focus**: Emphasis on code quality, testing, and documentation

## Prompt Categories

### Basic Code Generation

- **Simple Implementation**: Straightforward coding tasks with clear specifications
- **Algorithm Implementation**: Data structures and algorithms with complexity analysis
- **API Integration**: Connecting to external services and APIs

### Complex System Development

- **Full-Stack Applications**: Complete web applications with multiple layers
- **Microservices**: Distributed systems with service communication
- **Data Pipelines**: ETL processes and data processing workflows

### Code Quality & Optimization

- **Refactoring**: Improving existing code structure and performance
- **Performance Optimization**: Identifying and resolving bottlenecks
- **Security Enhancement**: Implementing security best practices

## Model-Specific Optimization

### Qwen 7B Prompts

- **Focus**: Rapid prototyping and simple implementations
- **Strategy**: Clear, concise prompts with essential requirements
- **Context**: Keep context windows focused and avoid complexity

### Qwen 14B Prompts

- **Focus**: Balanced development tasks and moderate complexity
- **Strategy**: Structured prompts with detailed requirements
- **Context**: Utilize context window for comprehensive task information

### Qwen 72B Prompts

- **Focus**: Complex architectures and deep technical analysis
- **Strategy**: Rich context with architectural considerations
- **Context**: Leverage full context window for comprehensive understanding

## Usage Guidelines

### Effective Prompt Structure

1. **Clear Objective**: State exactly what you want to accomplish
2. **Context Information**: Provide relevant background and constraints
3. **Technical Requirements**: Specify languages, frameworks, and standards
4. **Quality Standards**: Define testing, documentation, and performance requirements
5. **Success Criteria**: Establish clear completion and quality metrics

### Example Prompt Patterns

#### Web Application Development

```
Develop a modern React application for task management with the following specifications:

**Core Requirements:**
- User authentication and authorization
- Task creation, editing, and deletion
- Real-time updates using WebSocket
- Responsive design for mobile and desktop

**Technical Stack:**
- React 18+ with TypeScript
- Node.js/Express backend
- MongoDB for data persistence
- Material-UI for components

**Code Quality:**
- Comprehensive test coverage (unit + integration)
- API documentation with OpenAPI spec
- Error handling and logging
- Performance optimization

**Deliverables:**
- Complete source code with build configuration
- Docker containerization
- Deployment documentation
- Testing instructions
```

#### API Development

```
Create a REST API service for e-commerce functionality with Qwen optimization:

**API Endpoints:**
- Product catalog with search and filtering
- Shopping cart management
- Order processing and status tracking
- User profile and preferences

**Architecture Requirements:**
- RESTful design with proper HTTP methods
- JSON API specification compliance
- Rate limiting and caching strategies
- Comprehensive error handling

**Security:**
- JWT-based authentication
- Input validation and sanitization
- CORS configuration
- API versioning strategy

**Performance:**
- Database query optimization
- Response caching implementation
- Pagination for large datasets
- Monitoring and logging integration
```

## Best Practices

### Context Management

- **Prioritize Information**: Place most important requirements first
- **Use Structure**: Organize information with clear headings and sections
- **Stay Focused**: Avoid unnecessary details that consume context space

### Iterative Development

- **Break Complex Tasks**: Divide large projects into manageable phases
- **Use Continuation**: Reference previous work when adding features
- **Maintain Consistency**: Keep coding style and patterns consistent

### Quality Assurance

- **Request Testing**: Always include testing requirements in prompts
- **Specify Standards**: Define code quality and documentation standards
- **Include Validation**: Ask for validation steps and success criteria

## Troubleshooting

### Common Issues

1. **Incomplete Code**: Provide more specific requirements and constraints
2. **Poor Quality**: Emphasize testing, error handling, and documentation
3. **Performance Issues**: Specify performance requirements and optimization needs
4. **Integration Problems**: Include more context about existing systems

### Optimization Tips

- **Model Selection**: Choose appropriate Qwen model size for task complexity
- **Prompt Refinement**: Iterate on prompts based on results
- **Context Window**: Monitor and optimize context usage
- **Error Recovery**: Plan for debugging and error correction phases
