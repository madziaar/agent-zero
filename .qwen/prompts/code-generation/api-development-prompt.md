# API Development Prompt Template

**Qwen Model Optimization**: 14B (API development with moderate complexity)

```
Develop a comprehensive REST API service for e-commerce order management:

**Core API Endpoints:**
- POST /orders - Create new order with validation
- GET /orders/{id} - Retrieve order by ID with full details
- PUT /orders/{id} - Update order status and details
- DELETE /orders/{id} - Cancel/delete order (soft delete)
- GET /orders - List orders with filtering and pagination
- POST /orders/{id}/items - Add items to existing order
- DELETE /orders/{id}/items/{itemId} - Remove items from order

**Technical Architecture:**
- FastAPI (Python) with async support for high performance
- SQLAlchemy ORM with PostgreSQL database
- Pydantic models for request/response validation
- Redis for caching and session management
- Docker containerization with multi-stage builds
- JWT authentication with refresh token rotation

**Code Quality Requirements:**
- Comprehensive error handling with custom exception classes
- Request/response logging with structured JSON format
- Input validation using Pydantic models with detailed error messages
- Database transactions for data consistency
- Unit tests with >90% coverage using pytest
- Integration tests for API endpoints
- API documentation with OpenAPI/Swagger

**Security Implementation:**
- JWT token-based authentication with configurable expiration
- Password hashing using bcrypt with salt rounds
- Rate limiting per user/IP address
- CORS configuration for cross-origin requests
- SQL injection prevention through ORM usage
- XSS protection for any user-generated content

**Performance Optimization:**
- Database query optimization with proper indexing
- Response caching for frequently accessed data
- Pagination for large result sets
- Async database operations for I/O efficiency
- Connection pooling for database connections
- Background task processing for heavy operations

**API Standards Compliance:**
- RESTful URL patterns and HTTP methods
- Proper HTTP status codes (200, 201, 400, 404, 500)
- Consistent response format with metadata
- Versioning strategy in URL path (/v1/orders)
- HATEOAS implementation for navigation links
- Content negotiation (JSON/XML support)

**Monitoring & Observability:**
- Structured logging with correlation IDs
- Performance metrics collection (Prometheus)
- Health check endpoints for load balancer
- Distributed tracing for request flow
- Error tracking and alerting
- API usage analytics and reporting

**Deployment Requirements:**
- Docker Compose for local development
- Kubernetes manifests for production deployment
- Environment-based configuration management
- Database migration scripts with Alembic
- CI/CD pipeline configuration
- Load testing and performance benchmarks

**Deliverables:**
1. Complete FastAPI application with all endpoints
2. Database models and migration scripts
3. Authentication and authorization middleware
4. Comprehensive test suites (unit + integration)
5. API documentation with examples
6. Docker configuration for deployment
7. Monitoring and logging configuration
8. Postman collection for API testing
9. Deployment and operations guide

**Success Criteria:**
- All API endpoints function correctly under load
- Response time <200ms for simple operations
- Security vulnerabilities < CVSS 4.0
- Test coverage >90% with passing tests
- API documentation score >8/10
- Zero critical bugs in production deployment

Focus on creating a production-ready API that follows industry best practices and can scale to handle enterprise-level traffic.
```
