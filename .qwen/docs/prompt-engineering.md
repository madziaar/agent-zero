# Qwen Prompt Engineering Guide

This comprehensive guide provides best practices for crafting effective prompts that maximize Qwen model performance and code generation quality.

## Prompt Structure Fundamentals

### The Five-Layer Prompt Architecture

#### 1. Context Layer (Foundation)
```markdown
**Project Context:**
- Full-stack e-commerce platform
- React 18+, Node.js/Express, PostgreSQL
- Microservices architecture with Docker

**Current Task:**
- Implement user authentication service
- Integrate with existing user service

**Related Files:**
- ./models/user.js (existing user model)
- ./services/auth.js (current auth service)
- ./components/Login.jsx (login component)
```

#### 2. Objective Layer (What)
```markdown
**Primary Goal:**
Generate a complete authentication service with:

**Core Features:**
- User registration with email verification
- JWT-based login/logout functionality
- Password reset with secure tokens
- Session management and validation

**Success Criteria:**
- All endpoints tested and working
- Security vulnerabilities < CVSS 4.0
- Response time <200ms for auth operations
```

#### 3. Specification Layer (How)
```markdown
**Technical Requirements:**
- FastAPI with Python 3.9+
- SQLAlchemy ORM with PostgreSQL
- JWT tokens with 15-minute expiration
- bcrypt password hashing (rounds=12)
- Redis for session storage

**Code Quality Standards:**
- Type hints for all functions
- Comprehensive error handling
- Input validation and sanitization
- Logging with structured format
```

#### 4. Quality Layer (Standards)
```markdown
**Testing Requirements:**
- Unit tests for all functions (>90% coverage)
- Integration tests for API endpoints
- Security testing for auth flows
- Performance tests (<100ms response time)

**Documentation:**
- OpenAPI/Swagger documentation
- API usage examples
- Security considerations
- Deployment instructions
```

#### 5. Constraint Layer (Boundaries)
```markdown
**Project Constraints:**
- Must integrate with existing user model
- Follow established error handling patterns
- Maintain API versioning compatibility
- Support horizontal scaling

**Performance Targets:**
- Handle 1000+ concurrent users
- Database queries <50ms average
- Memory usage <100MB per instance
```

## Context Management Techniques

### Context Window Optimization

#### Hierarchical Information Structure
```markdown
**Level 1 - Critical (Always Include):**
- Primary task and deliverable
- Technology stack and versions
- Core requirements and constraints

**Level 2 - Important (Include When Relevant):**
- Project architecture and patterns
- Existing code references
- Integration requirements

**Level 3 - Supporting (Include for Complex Tasks):**
- Performance requirements
- Security considerations
- Testing standards
```

#### Context Preservation Strategies

**File Reference Pattern:**
```markdown
**Current Implementation:**
Generate authentication middleware for existing API structure.

**Reference Context:**
- Base API structure: ./api/base.py (lines 45-67)
- Error handling pattern: ./utils/errors.py
- Database models: ./models/user.py

**Integration Points:**
- Apply middleware to all protected routes
- Use existing error response format
- Follow database connection patterns
```

**Incremental Context Building:**
```markdown
**Phase 1 Context:**
Implement core authentication logic and JWT handling.

**Phase 2 Context (Builds on Phase 1):**
Add rate limiting and advanced security features.

**Phase 3 Context (Builds on Phase 1-2):**
Implement comprehensive monitoring and logging.
```

## Prompt Pattern Library

### 1. Function Generation Pattern
```markdown
**Function Pattern:**
```
Generate a [function_type] function with the following specifications:

**Function Signature:**
[Include type hints and parameters]

**Core Logic:**
[Describe the main algorithm or process]

**Edge Cases:**
[Specify error conditions and handling]

**Performance Requirements:**
[Response time, memory usage, optimization needs]

Example:
Generate a data validation function that processes user input with comprehensive error handling and performance optimization.
```
```

### 2. Component Generation Pattern
```markdown
**Component Pattern:**
```
Create a [component_name] component with:

**Props Interface:**
[TypeScript interface with detailed prop types]

**State Management:**
[State structure and management approach]

**Lifecycle Requirements:**
[Component lifecycle and effects]

**Styling Approach:**
[CSS framework, responsive design requirements]

**Integration Points:**
[Parent components, API calls, event handlers]
```
```

### 3. API Development Pattern
```markdown
**API Pattern:**
```
Develop a [service_name] API with:

**Endpoints Specification:**
- [Method] [Path] - [Purpose and functionality]
- Include request/response schemas
- Specify authentication requirements

**Data Layer:**
- Database models and relationships
- Query optimization requirements
- Transaction management

**Business Logic:**
- Core algorithms and processes
- Validation and transformation rules
- Integration with external services
```
```

### 4. System Design Pattern
```markdown
**Architecture Pattern:**
```
Design a [system_type] system with:

**Architecture Overview:**
- High-level component structure
- Data flow and interactions
- Technology stack decisions

**Component Specifications:**
- Service boundaries and responsibilities
- Communication protocols
- Scalability considerations

**Quality Attributes:**
- Performance requirements
- Security measures
- Maintainability standards
```
```

## Advanced Prompt Techniques

### Context Compression Strategies

#### Selective Information Inclusion
```markdown
**Before (Verbose):**
```
I need you to create a user authentication system for my web application.
The application is a social media platform built with React and Node.js.
We have a PostgreSQL database already set up. I need features like user
registration, login, password reset, and profile management. Also need
JWT tokens for session management and email verification for new users.
```

**After (Structured):**
```
**Project:** Social media platform authentication system

**Tech Stack:** React 18+, Node.js/Express, PostgreSQL

**Required Features:**
- User registration with email verification
- JWT-based login/logout
- Password reset functionality
- Profile management (view/edit)

**Security Requirements:**
- bcrypt password hashing (rounds=12)
- JWT tokens (15min expiration)
- Rate limiting on auth endpoints
- Input validation and sanitization
```
```

#### Smart Context Referencing
```markdown
**Inefficient:**
```
Create a new component that should look and work like the existing
dashboard component I showed you earlier, but for user management instead
of analytics. Remember how the dashboard had that sidebar navigation and
the table with sorting and filtering? I want something similar but for
managing users.
```

**Efficient:**
```
**Component:** UserManagement (similar to ./components/Dashboard.tsx)

**Reference Patterns:**
- Layout: Sidebar navigation (lines 45-78 in Dashboard.tsx)
- Table: Sortable/filterable (Table component lines 120-180)
- Styling: Material-UI with dark theme

**Modifications:**
- Replace analytics data with user data
- Add user action buttons (edit, delete, suspend)
- Include user creation modal
- Add bulk operations for user management
```
```

### Prompt Chaining and Iteration

#### Incremental Prompt Development
```markdown
**Initial Prompt:**
```
Generate a basic user registration form component with:
- Email and password fields
- Basic validation
- Submit button
```

**Refinement Prompt:**
```
Enhance the registration form with:
- Password strength indicator
- Email format validation with real-time feedback
- Terms and conditions checkbox
- Social login options (Google, GitHub)
- Responsive design for mobile devices
```

**Optimization Prompt:**
```
Optimize the registration form for performance:
- Implement form debouncing for validation
- Add skeleton loading states
- Optimize re-renders with React.memo
- Include error boundaries
- Add comprehensive TypeScript types
```
```

## Qwen-Specific Optimization Tips

### Model-Specific Prompt Adjustments

#### Qwen 7B Optimization
```markdown
**Prompt Characteristics:**
- Keep prompts focused and concise
- Use clear, simple language
- Avoid complex architectural decisions
- Focus on immediate implementation needs

**Optimized Structure:**
```
Task: Generate login component
Tech: React + TypeScript
Features: Email/password, validation, error handling
Requirements: Clean UI, responsive, accessible
```
```

#### Qwen 14B/72B Optimization
```markdown
**Prompt Characteristics:**
- Include detailed specifications
- Provide context and examples
- Specify integration requirements
- Include quality standards

**Optimized Structure:**
```
**Project Context:** Full-stack application with existing patterns
**Component Requirements:** Detailed feature specifications
**Technical Standards:** Code quality and testing requirements
**Integration Points:** How component fits into larger system
**Performance Targets:** Response times and optimization goals
```
```

### Context Window Management

#### Efficient Token Usage
```markdown
**High-Efficiency Prompt (200 tokens):**
```
Generate authentication service:

**Core Features:**
- JWT-based user authentication
- Registration with email verification
- Password reset functionality

**Tech Stack:**
- FastAPI, SQLAlchemy, PostgreSQL
- bcrypt, PyJWT, Redis

**Security Standards:**
- Password hashing (rounds=12)
- JWT expiration (15min)
- Rate limiting (100 req/min)

**Quality Requirements:**
- 90%+ test coverage
- OpenAPI documentation
- Error handling and logging

**Integration:**
- Use existing user model from ./models/user.py
- Follow error response format from ./utils/errors.py
```

**Low-Efficiency Prompt (350 tokens):**
```
I need an authentication service for my web application. Can you create a complete
authentication system that handles user registration, login, and password reset?
I want it to use JWT tokens for session management and also include email verification
for new user registrations. The technology stack should include FastAPI for the API,
SQLAlchemy for database operations, and PostgreSQL as the database. For security, I
want to make sure passwords are properly hashed using bcrypt, and I want to implement
rate limiting to prevent abuse. Also, I need comprehensive error handling and logging
throughout the system, and I want to make sure it's well tested and documented.
```
```

## Common Prompt Patterns and Examples

### Error Handling Enhancement Pattern
```markdown
**Pattern:**
```
Add comprehensive error handling to [component/function]:

**Error Categories:**
- Network failures and timeouts
- Invalid input validation errors
- Authentication and authorization failures
- Database connection issues
- External service failures

**Error Response Format:**
- Consistent error structure across application
- Appropriate HTTP status codes
- User-friendly error messages
- Detailed logging for debugging

**Recovery Mechanisms:**
- Retry logic for transient failures
- Fallback options where applicable
- User guidance for resolution
```
```

### Performance Optimization Pattern
```markdown
**Pattern:**
```
Optimize [component/system] for performance:

**Current Issues:**
- [Specific performance problems identified]

**Optimization Targets:**
- Response time < [target]ms
- Memory usage < [target]MB
- CPU utilization < [target]%

**Implementation Strategies:**
- Caching for frequently accessed data
- Database query optimization
- Code splitting and lazy loading
- Memoization for expensive computations
```
```

## Troubleshooting Prompt Issues

### Common Prompt Problems and Solutions

#### 1. Incomplete Code Generation
**Problem:** Qwen generates partial or incomplete implementations
**Solutions:**
- Break complex tasks into smaller, focused requests
- Provide more specific requirements and constraints
- Include examples of expected patterns or structures
- Specify integration points and dependencies clearly

#### 2. Poor Code Quality
**Problem:** Generated code lacks proper error handling or follows poor patterns
**Solutions:**
- Explicitly request comprehensive error handling
- Specify testing requirements and coverage targets
- Request documentation and code comments
- Ask for performance considerations upfront

#### 3. Context Window Overflow
**Problem:** Complex projects exceed context limitations
**Solutions:**
- Use incremental development approach
- Reference existing files and components explicitly
- Focus prompts on specific functionality
- Maintain consistent naming and patterns across prompts

### Prompt Quality Checklist

#### Before Submitting a Prompt

- [ ] **Clear Objective**: Primary goal is clearly stated
- [ ] **Complete Context**: All necessary background provided
- [ ] **Technical Specifications**: Technology stack and constraints defined
- [ ] **Quality Standards**: Testing, documentation, performance specified
- [ ] **Success Criteria**: Clear measurement of completion
- [ ] **Integration Points**: How work fits with existing system
- [ ] **Edge Cases**: Error conditions and recovery specified

#### After Receiving Results

- [ ] **Completeness**: All requirements addressed
- [ ] **Quality**: Error handling, testing, documentation included
- [ ] **Integration**: Works with existing codebase
- [ ] **Performance**: Meets specified performance targets
- [ ] **Maintainability**: Code is readable and well-structured

## Best Practices Summary

### Prompt Writing Principles

1. **Structure Over Volume**: Well-organized prompts are more effective than lengthy ones
2. **Specificity Matters**: Clear requirements produce better results than vague descriptions
3. **Context is King**: Provide relevant background and integration information
4. **Quality First**: Specify testing, documentation, and performance requirements upfront
5. **Iterative Refinement**: Use feedback from initial results to improve subsequent prompts

### Optimization Techniques

1. **Match Complexity**: Align prompt detail with model capabilities
2. **Use Patterns**: Follow established prompt patterns for consistency
3. **Manage Context**: Structure information for efficient token usage
4. **Chain Effectively**: Build complex solutions through iterative refinement
5. **Test and Validate**: Verify prompt effectiveness and adjust as needed

By mastering these prompt engineering techniques, you can significantly improve the quality and consistency of code generation from Qwen models, leading to more successful development outcomes and efficient workflows.