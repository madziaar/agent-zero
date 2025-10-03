# Data Processing Pipeline Template

This template provides a Qwen-optimized starting point for building robust, scalable data processing pipelines.

## Features

- **Async Processing**: Concurrent data processing with asyncio and async/await patterns
- **Error Handling**: Comprehensive error handling with retry mechanisms and dead letter queues
- **Monitoring & Observability**: Structured logging, metrics collection, and health checks
- **Configuration Management**: Environment-based configuration with validation
- **Data Validation**: Pydantic models for input/output validation and serialization
- **Pipeline Orchestration**: Workflow management with dependency resolution
- **Scalability**: Horizontal scaling support with queue-based processing
- **Testing Framework**: Unit and integration tests for pipeline components
- **Documentation**: Auto-generated API documentation for pipeline endpoints
- **Security**: Input sanitization and secure data handling practices

## Project Structure

```
data-pipeline/
├── pipeline/
│   ├── core/               # Core pipeline functionality
│   │   ├── engine.py       # Main pipeline execution engine
│   │   ├── config.py       # Pipeline configuration management
│   │   └── exceptions.py   # Custom pipeline exceptions
│   ├── stages/             # Processing stages and steps
│   │   ├── extract.py      # Data extraction stages
│   │   ├── transform.py    # Data transformation stages
│   │   └── load.py         # Data loading stages
│   ├── monitoring/         # Monitoring and observability
│   │   ├── metrics.py      # Metrics collection
│   │   ├── logging.py      # Structured logging
│   │   └── health.py       # Health check endpoints
│   └── utils/              # Utility functions
├── config/                 # Configuration files
│   ├── pipeline.yaml       # Pipeline definition
│   ├── logging.conf        # Logging configuration
│   └── stages/             # Stage-specific configs
├── tests/                  # Test suites
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── scripts/                # Utility scripts
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container definition
└── docker-compose.yml     # Multi-container setup
```

## Qwen Optimization Notes

### Prompt Engineering Tips

When using this template with Qwen Coder:

1. **Pipeline Stage Development**:

   ```
   Create a data transformation stage that processes JSON data with field mapping.
   Include error handling, validation, and Qwen-optimized async processing patterns.
   ```

2. **Error Handling Strategy**:

   ```
   Implement comprehensive error handling for data pipeline with retry logic,
   dead letter queues, and monitoring integration for production reliability.
   ```

3. **Monitoring Implementation**:

   ```
   Add monitoring and metrics collection to track pipeline performance,
   data quality, and error rates with Qwen's observability best practices.
   ```

### Model Selection

- **Qwen 7B**: Simple data transformations and basic pipeline stages
- **Qwen 14B**: Complex data processing workflows and pipeline orchestration
- **Qwen 72B**: Advanced pipeline optimization and distributed processing design

## Getting Started

1. **Initialize Project**:

   ```bash
   # Copy template to new project
   cp -r .qwen/templates/data-pipeline/ my-data-pipeline

   # Navigate to project
   cd my-data-pipeline

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Pipeline**:

   ```bash
   # Copy configuration template
   cp config/pipeline.yaml.example config/pipeline.yaml

   # Edit pipeline configuration
   nano config/pipeline.yaml
   ```

3. **Customize Processing Stages**:

   ```bash
   # Add your custom processing stages in pipeline/stages/
   # Follow the existing patterns for consistency
   ```

4. **Start Pipeline**:

   ```bash
   # Run pipeline in development mode
   python -m pipeline.core.engine --config config/pipeline.yaml

   # Run with specific stage
   python -m pipeline.core.engine --stage extract_data

   # Run in daemon mode
   python -m pipeline.core.engine --daemon
   ```

## Integration with Agent Zero

This template is designed to work seamlessly with Agent Zero's development tools:

- **File Browser**: Manage project files through the web interface
- **Code Execution**: Test pipeline stages directly in the environment
- **Terminal Integration**: Monitor pipeline execution and view logs
- **Memory System**: Maintain context across development sessions
- **Browser Integration**: Access pipeline monitoring dashboards

## Configuration

### Pipeline Configuration (pipeline.yaml)

```yaml
pipeline:
  name: "data-processing-pipeline"
  version: "1.0.0"

stages:
  - name: "extract"
    type: "extract"
    config:
      source: "api"
      format: "json"

  - name: "transform"
    type: "transform"
    depends_on: ["extract"]
    config:
      mapping:
        field1: "source_field1"
        field2: "source_field2"

  - name: "load"
    type: "load"
    depends_on: ["transform"]
    config:
      destination: "database"
      table: "processed_data"

monitoring:
  metrics:
    enabled: true
    interval: 30

  logging:
    level: "INFO"
    format: "json"
```

### Environment Variables

```bash
# Core settings
PIPELINE_NAME=my-pipeline
ENVIRONMENT=development

# Processing configuration
BATCH_SIZE=1000
MAX_WORKERS=4
TIMEOUT=300

# Monitoring
METRICS_PORT=9090
HEALTH_CHECK_INTERVAL=30
```

## Testing

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Run with coverage
pytest --cov=pipeline

# Test specific pipeline stage
pytest tests/unit/test_transform.py::test_field_mapping
```

## Monitoring & Observability

### Metrics Collection

The pipeline automatically collects metrics including:

- Processing throughput (records/second)
- Error rates by stage
- Queue depths and processing latency
- System resource utilization

### Health Checks

```bash
# Health check endpoint
curl http://localhost:8000/health

# Detailed pipeline status
curl http://localhost:8000/status
```

### Logging

Structured JSON logging with configurable levels:

- **DEBUG**: Detailed execution information
- **INFO**: General pipeline progress
- **WARN**: Non-critical issues
- **ERROR**: Processing failures and exceptions

## Example Usage

To create a new data pipeline using this template:

```
Create a customer data processing pipeline using the data-pipeline template.
Implement data extraction from multiple sources, transformation with data cleansing,
and loading into a data warehouse. Include comprehensive error handling,
monitoring, and retry mechanisms. Optimize for Qwen 14B processing efficiency.
```
