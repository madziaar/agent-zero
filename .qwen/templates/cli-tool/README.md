# Command-Line Tool Template

This template provides a Qwen-optimized starting point for building robust, user-friendly command-line applications.

## Features

- **Argument Parsing**: Comprehensive CLI interface using argparse with subcommands
- **Configuration Management**: YAML/JSON configuration files with environment variable support
- **Interactive Mode**: Rich interactive experience with prompts and progress bars
- **Error Handling**: Graceful error handling with helpful error messages
- **Logging System**: Configurable logging with multiple output formats
- **Shell Integration**: Tab completion and shell-friendly output formatting
- **Testing Framework**: Comprehensive test coverage for CLI functionality
- **Documentation**: Auto-generated help text and manual pages
- **Cross-Platform**: Windows, macOS, and Linux compatibility
- **Security**: Secure handling of sensitive data and credentials

## Project Structure

```
cli-tool/
├── cli/
│   ├── __main__.py         # Entry point for `python -m cli`
│   ├── __init__.py         # CLI package initialization
│   ├── main.py             # Main CLI application logic
│   ├── commands/           # Command implementations
│   │   ├── configure.py    # Configuration management
│   │   ├── data.py         # Data processing commands
│   │   └── utils.py        # Utility commands
│   ├── core/               # Core CLI functionality
│   │   ├── parser.py       # Argument parser setup
│   │   ├── config.py       # Configuration management
│   │   └── output.py       # Output formatting
│   └── utils/              # CLI utilities
├── config/                 # Configuration files
│   ├── default.yaml        # Default configuration
│   └── schema.json         # Configuration schema
├── tests/                  # Test suites
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── scripts/                # Utility scripts
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── setup.py               # Package distribution
└── MANIFEST.in            # Package manifest
```

## Qwen Optimization Notes

### Prompt Engineering Tips

When using this template with Qwen Coder:

1. **Command Implementation**:

   ```
   Create a file processing command that handles multiple file formats with progress tracking.
   Include comprehensive argument validation and Qwen-optimized error handling patterns.
   ```

2. **Configuration Management**:

   ```
   Implement configuration system with YAML files, environment variables, and validation.
   Include secure credential handling and Qwen's configuration best practices.
   ```

3. **Interactive Features**:

   ```
   Add interactive prompts with validation and progress bars for long-running operations.
   Optimize for user experience with Qwen's UX patterns.
   ```

### Model Selection

- **Qwen 7B**: Simple CLI tools and basic command implementations
- **Qwen 14B**: Advanced CLI applications with multiple subcommands and complex workflows
- **Qwen 72B**: Enterprise-grade CLI tools with extensive configuration and customization

## Getting Started

1. **Initialize Project**:

   ```bash
   # Copy template to new project
   cp -r .qwen/templates/cli-tool/ my-cli-tool

   # Navigate to project
   cd my-cli-tool

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Tool**:

   ```bash
   # Copy configuration template
   cp config/default.yaml.example config/default.yaml

   # Edit configuration
   nano config/default.yaml

   # Run initial configuration
   python -m cli configure init
   ```

3. **Install for Development**:

   ```bash
   # Install in development mode
   pip install -e .

   # Or install for local use only
   pip install -e . --no-deps
   ```

4. **Basic Usage**:

   ```bash
   # Show help
   python -m cli --help

   # Show version
   python -m cli --version

   # Run a command
   python -m cli data process --input file.csv --output results.json
   ```

## Integration with Agent Zero

This template is designed to work seamlessly with Agent Zero's development tools:

- **File Browser**: Manage project files through the web interface
- **Code Execution**: Test CLI commands directly in the environment
- **Terminal Integration**: Interactive CLI development and testing
- **Memory System**: Maintain context across development sessions
- **Shell Integration**: Tab completion and command history

## Configuration

### Configuration File (config/default.yaml)

```yaml
cli:
  name: "my-cli-tool"
  version: "1.0.0"
  description: "A powerful command-line tool"

logging:
  level: "INFO"
  format: "text"
  file: "logs/cli.log"

output:
  format: "table"
  colors: true
  pagination: true

defaults:
  input_format: "auto"
  output_format: "json"
  verbose: false
```

### Environment Variables

```bash
# Tool configuration
CLI_NAME=my-tool
CLI_LOG_LEVEL=DEBUG

# Default settings
CLI_DEFAULT_FORMAT=yaml
CLI_OUTPUT_COLORS=true

# Security settings
CLI_CONFIG_ENCRYPTION=false
CLI_SENSITIVE_KEYS=api_key,token,password
```

## Command Structure

### Basic Command Pattern

```python
# cli/commands/example.py
from ..core.parser import Command
from ..core.output import output

class ExampleCommand(Command):
    """Example command implementation."""

    def setup_parser(self, parser):
        parser.add_argument('--input', '-i', required=True, help='Input file')
        parser.add_argument('--output', '-o', help='Output file')
        parser.add_argument('--format', choices=['json', 'yaml', 'csv'], default='json')

    def execute(self, args):
        # Command implementation
        data = self.load_data(args.input)
        result = self.process_data(data, args.format)
        self.save_result(result, args.output)
        output.success(f"Processed {len(data)} items")
```

### Subcommands

```bash
# Main command structure
python -m cli [OPTIONS] COMMAND [ARGS]...

# Available commands:
python -m cli configure    # Configuration management
python -m cli data         # Data processing commands
python -m cli utils        # Utility commands

# Command-specific help
python -m cli data --help
python -m cli data process --help
```

## Testing

```bash
# Run all tests
pytest

# Run CLI-specific tests
pytest tests/ -k "cli" -v

# Test command functionality
pytest tests/integration/test_commands.py -v

# Test with coverage
pytest --cov=cli --cov-report=html

# Test CLI interface
python -m cli --help | grep -q "my-cli-tool"
```

## Packaging and Distribution

### Building for Distribution

```bash
# Create source distribution
python setup.py sdist

# Create wheel distribution
python setup.py bdist_wheel

# Upload to PyPI (when ready)
twine upload dist/*
```

### Installation from Source

```bash
# For development
pip install -e .

# For production
pip install .

# Global installation
sudo pip install .
```

## Interactive Mode

The CLI supports interactive mode for complex operations:

```bash
# Interactive configuration
python -m cli configure --interactive

# Interactive data processing
python -m cli data process --interactive

# Guided workflow
python -m cli workflow start --guided
```

## Shell Integration

### Tab Completion

```bash
# Bash completion (add to .bashrc)
source <(python -m cli completion bash)

# Zsh completion (add to .zshrc)
source <(python -m cli completion zsh)

# Fish completion
python -m cli completion fish > ~/.config/fish/completions/cli.fish
```

### Alias Setup

```bash
# Create convenient aliases
alias ct='python -m cli'
alias mytool='python -m cli'

# In your shell profile
echo "alias ct='python -m cli'" >> ~/.bashrc
```

## Example Usage

To create a new CLI tool using this template:

```
Create a file management CLI tool using the cli-tool template.
Implement commands for file processing, directory operations, and batch renaming.
Include configuration management, progress tracking, and comprehensive help system.
Optimize for Qwen 14B and ensure cross-platform compatibility.
```
