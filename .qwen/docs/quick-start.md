# Qwen Coder Quick Start Guide

This guide helps you get started quickly with Qwen Coder subagents for enhanced coding assistance.

## First Steps

### 1. Basic Usage

To invoke a Qwen Coder subagent:

```
I need help with Python development. Deploy qwen-coder subagent for this task.
```

Or for specific model targeting:

```
Create a React component for user management. Use qwen-coder with Qwen 14B optimization.
```

### 2. Template Usage

Use the provided templates for common tasks:

```
Generate a modern web application using the web-app template from .qwen/templates/
Include authentication, dashboard, and API integration.
```

## Prompt Examples by Category

### Web Development

#### React Component

```
Create a reusable DataTable component with the following features:
- Server-side pagination and sorting
- Column filtering and search
- Row selection and bulk actions
- Responsive design with mobile support
- TypeScript interfaces for type safety
- Unit tests with React Testing Library

Use Material-UI for styling and optimize for Qwen 14B context window.
```

#### Full-Stack Application

```
Develop a task management application with:
- User authentication (JWT-based)
- Task CRUD operations
- Real-time updates with WebSocket
- File attachment support
- Team collaboration features
- Responsive React frontend
- Node.js/Express backend
- MongoDB database

Include Docker configuration and deployment scripts.
Focus on code quality with comprehensive testing.
```

### API Development

#### REST API Service

```
Build a REST API for e-commerce functionality:
- Product catalog with search and filtering
- Shopping cart management
- Order processing with status tracking
- User authentication and authorization
- Payment integration (Stripe/PayPal)

Use FastAPI with PostgreSQL, include comprehensive documentation,
implement rate limiting and caching for production readiness.
```

### Data Processing

#### Data Pipeline

```
Create a data pipeline for log analytics:
- Ingest logs from multiple sources
- Parse and structure log entries
- Real-time aggregation and alerting
- Data storage in Elasticsearch
- API for querying analytics data

Use Apache Kafka and Python for implementation,
include monitoring and error handling.
```

## Model Selection Guide

### Quick Reference

| Task Type                | Recommended Model | Rationale                            |
| ------------------------ | ----------------- | ------------------------------------ |
| **Simple Components**    | Qwen 7B           | Fast iteration, clear requirements   |
| **Web Applications**     | Qwen 14B          | Balanced complexity and quality      |
| **Complex Systems**      | Qwen 72B          | Deep analysis, architecture design   |
| **Performance Critical** | Qwen 72B          | Optimization and benchmarking        |
| **Rapid Prototyping**    | Qwen 7B           | Quick results, iterative development |

### Context Window Tips

#### Qwen 7B (8K tokens)

- Keep prompts focused and concise
- Use clear, simple requirements
- Avoid complex architectural decisions

#### Qwen 14B (8K tokens)

- Provide detailed requirements
- Include examples and constraints
- Structure information hierarchically

#### Qwen 72B (32K tokens)

- Include comprehensive context
- Specify architectural requirements
- Detail performance and quality standards

## Quality Enhancement

### Always Include

1. **Clear Requirements**: What should the code do?
2. **Technical Specifications**: Languages, frameworks, constraints
3. **Quality Standards**: Testing, documentation, performance
4. **Success Criteria**: How to measure completion

### Example Quality-Focused Prompt

```
Develop a user authentication system with these specifications:

**Functional Requirements:**
- User registration with email verification
- Login/logout with JWT tokens
- Password reset functionality
- Role-based access control

**Technical Implementation:**
- React frontend with TypeScript
- Node.js backend with Express
- MongoDB database
- Redis for session storage

**Security Requirements:**
- Password hashing with bcrypt
- JWT token expiration and refresh
- Rate limiting on auth endpoints
- Input validation and sanitization

**Quality Standards:**
- Unit tests for all components (>90% coverage)
- Integration tests for auth flows
- API documentation with examples
- Error handling and logging
- Performance optimization

**Deliverables:**
1. Complete source code for frontend and backend
2. Database models and migrations
3. Test suites and configuration
4. API documentation
5. Deployment guide

**Success Criteria:**
- All authentication flows work correctly
- Security vulnerabilities < CVSS 4.0
- Response time <200ms for auth operations
- Test coverage >90% with passing tests
- Zero critical security issues

Ensure production-ready code with proper error handling and security measures.
```

## Common Patterns

### Incremental Development

For complex projects, break them down:

1. **Phase 1**: Core functionality
2. **Phase 2**: Advanced features
3. **Phase 3**: Optimization and testing

### Error Handling

Always request comprehensive error handling:

```
Include robust error handling for:
- Network failures and timeouts
- Invalid user input
- Database connection issues
- Authentication failures
- Rate limiting scenarios
```

### Testing Requirements

Specify testing needs explicitly:

```
Include comprehensive testing with:
- Unit tests for all functions
- Integration tests for API endpoints
- End-to-end tests for user flows
- Performance tests for critical paths
- Minimum 90% test coverage
```

## Integration with Agent Zero

### Using File Browser

- Upload files to `.qwen/` workspace for reference
- Download generated code and artifacts
- Organize projects in dedicated directories

### Memory and Context

- Use Agent Zero's memory system for project context
- Reference previous work in new prompts
- Maintain consistent patterns across sessions

## Getting Help

### When Things Go Wrong

1. **Incomplete Code**: Provide more specific requirements
2. **Poor Quality**: Emphasize testing and error handling
3. **Performance Issues**: Specify performance targets
4. **Integration Problems**: Include existing system context

### Optimization Tips

- **Start Simple**: Begin with clear, focused tasks
- **Iterate**: Refine prompts based on results
- **Test**: Validate generated code thoroughly
- **Document**: Request comprehensive documentation

## Next Steps

1. **Explore Templates**: Check `.qwen/templates/` for project starters
2. **Review Examples**: Study `.qwen/examples/` for coding patterns
3. **Read Documentation**: Review `.qwen/docs/` for detailed guides
4. **Experiment**: Try different prompt styles and model sizes
5. **Share Results**: Document successful patterns for future use

The Qwen Coder workspace is designed to grow with your needs. As you use it more, you'll discover patterns and approaches that work best for your specific use cases.
