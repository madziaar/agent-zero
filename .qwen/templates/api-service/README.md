# REST API Service Template

This template provides a Qwen-optimized starting point for building production-ready REST API services.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs with Python 3.7+
- **Authentication System**: JWT-based authentication with role-based access control
- **Database Integration**: SQLAlchemy ORM with async support and migrations
- **Comprehensive Testing**: Unit, integration, and API tests with pytest
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **CORS Support**: Cross-origin resource sharing configuration
- **Request Validation**: Pydantic models for data validation and serialization
- **Error Handling**: Centralized error handling with custom exception handlers
- **Logging**: Structured logging with configurable levels
- **Environment Management**: Multiple environment configurations

## Project Structure

```
api-service/
├── app/
│   ├── api/                 # API route handlers organized by feature
│   │   ├── v1/             # API versioning
│   │   └── deps.py         # Dependency injection
│   ├── core/               # Core application configuration
│   │   ├── config.py       # Application settings
│   │   ├── security.py     # Authentication and authorization
│   │   └── logging.py      # Logging configuration
│   ├── db/                 # Database setup and models
│   │   ├── base.py         # Base database models
│   │   ├── session.py      # Database session management
│   │   └── models/         # SQLAlchemy models
│   ├── models/             # Pydantic models for API
│   ├── schemas/            # Response/request schemas
│   └── tests/              # Test modules
├── alembic/                # Database migrations
├── .env.example           # Environment variables template
├── main.py               # Application entry point
├── requirements.txt       # Python dependencies
└── pyproject.toml        # Project configuration
```

## Qwen Optimization Notes

### Prompt Engineering Tips

When using this template with Qwen Coder:

1. **API Endpoint Generation**:

   ```
   Create a user management API with CRUD operations for users.
   Include authentication, input validation, and proper error handling.
   Optimize for Qwen 14B context window and follow REST principles.
   ```

2. **Database Model Design**:

   ```
   Design SQLAlchemy models for e-commerce system with User, Product, Order entities.
   Include proper relationships, constraints, and Qwen-optimized async patterns.
   ```

3. **Authentication Implementation**:

   ```
   Implement JWT authentication system with refresh tokens and role-based access.
   Include password hashing, token blacklisting, and security best practices.
   ```

### Model Selection

- **Qwen 7B**: Simple API endpoints and basic CRUD operations
- **Qwen 14B**: Full API development with authentication and complex business logic
- **Qwen 72B**: Advanced API design, performance optimization, and microservices architecture

## Getting Started

1. **Initialize Project**:

   ```bash
   # Copy template to new project
   cp -r .qwen/templates/api-service/ my-api-service

   # Navigate to project
   cd my-api-service

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Environment**:

   ```bash
   # Copy environment template
   cp .env.example .env

   # Edit .env with your configuration
   nano .env  # Or your preferred editor
   ```

3. **Database Setup**:

   ```bash
   # Run database migrations
   alembic upgrade head

   # Seed initial data (if needed)
   python -m app.scripts.seed_data
   ```

4. **Start Development Server**:

   ```bash
   # Development mode with auto-reload
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Or using Python module
   python -m app.main
   ```

## Integration with Agent Zero

This template is designed to work seamlessly with Agent Zero's development tools:

- **File Browser**: Manage project files through the web interface
- **Code Execution**: Test API endpoints directly in the environment
- **Browser Integration**: Access Swagger UI for API documentation
- **Memory System**: Maintain context across development sessions
- **Terminal Integration**: Run API tests and database operations

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_users.py

# API integration tests
pytest app/tests/test_api/
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Example Usage

To create a new API service using this template:

```
Create a REST API for a blog platform using the api-service template.
Implement user management, post CRUD operations, and commenting system.
Include authentication, rate limiting, and comprehensive API documentation.
Optimize for Qwen 14B and ensure scalability.
```
