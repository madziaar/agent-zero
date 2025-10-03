# Agent Zero - Project Documentation

## Project Overview

Agent Zero is a personal, organic agentic framework that grows and learns with you. It's designed to be dynamic, organically growing, and learning as you use it. The framework is fully transparent, readable, comprehensible, customizable, and interactive. It uses the computer as a tool to accomplish tasks.

**Key Features:**
1. **General-purpose Assistant** - Not pre-programmed for specific tasks but meant to be a general-purpose personal assistant that can gather information, execute commands, and cooperate with other agent instances.
2. **Computer as a Tool** - Uses the operating system as a tool through code execution and terminal access to create and use its own tools as needed.
3. **Multi-agent Cooperation** - Every agent has a superior agent giving it tasks and instructions, and can create subordinate agents to help break down and solve subtasks.
4. **Completely Customizable and Extensible** - Almost nothing is hard-coded. The behavior is defined by a system prompt in the `prompts/default/agent.system.md` file.
5. **Communication is Key** - Offers real-time streaming interactive terminal interface with communication between agents and users.

## Architecture

### Core Components

- **agent.py** - Main framework with Agent and AgentContext classes that manage the agent lifecycle, message loops, and interaction with models
- **models.py** - Handles model configuration using LiteLLM wrapper with support for multiple providers and rate limiting
- **run_ui.py** - Flask-based web UI server with basic authentication and API endpoints
- **initialize.py** - Agent initialization logic and configuration loading
- **Prompts** - Located in `prompts/` directory - defines agent behavior through system prompts
- **Tools** - Located in `python/tools/` - extend agent functionality (browser agent, code execution, search, etc.)

### Directory Structure

```
agent-zero/
├── agent.py                 # Main agent class and context management
├── models.py                # Model configuration and LiteLLM wrapper
├── run_ui.py               # Flask web UI server
├── initialize.py           # Agent initialization logic
├── run_tunnel.py           # Tunnel functionality for remote access
├── prompts/                # System prompts defining agent behavior
├── python/
│   ├── api/                # API handlers
│   ├── extensions/         # Extension modules
│   ├── helpers/            # Utility functions
│   └── tools/              # Agent tools (browser, code execution, etc.)
├── conf/                   # Configuration files
├── agents/                 # Agent profiles
├── webui/                  # Web interface files
├── docs/                   # Documentation
├── knowledge/              # Knowledge base
├── memory/                 # Memory storage
└── requirements.txt        # Python dependencies
```

### Agent Configuration

Agents are configured using `AgentConfig` dataclass with these model types:
- **Chat Model** - For primary agent responses
- **Utility Model** - For utility operations like memory consolidation
- **Embedding Model** - For memory and knowledge retrieval
- **Browser Model** - For web browsing capabilities

Model providers are configured in `conf/model_providers.yaml` and support multiple providers including:
- OpenAI, Anthropic, Google, Mistral, Ollama, LM Studio, and others

## Building and Running

### Development Setup

1. **Prerequisites**:
   - Python 3.8+
   - Git
   - Docker (optional, for containerized execution)

2. **Installation**:
   ```bash
   # Clone the repository
   git clone https://github.com/agent0ai/agent-zero.git
   cd agent-zero

   # Install dependencies
   pip install -r requirements.txt

   # Set up environment variables
   cp .env.example .env  # then edit .env with your API keys
   ```

3. **Running the Application**:
   ```bash
   # Direct execution
   python run_ui.py

   # With Docker
   docker build -t agent-zero .
   docker run -p 50001:80 agent-zero

   # Or pull and run pre-built image
   docker pull agent0ai/agent-zero
   docker run -p 50001:80 agent0ai/agent-zero
   ```

4. **Access the Interface**:
   - Web UI: http://localhost:50001
   - The UI is interactive with real-time streaming responses

### Environment Configuration

The application uses a `.env` file to manage API keys and settings:
- `CHAT_MODEL_API_KEY` - API key for the primary chat model
- `UTIL_MODEL_API_KEY` - API key for utility operations
- `EMBED_MODEL_API_KEY` - API key for embedding operations
- `BROWSER_MODEL_API_KEY` - API key for browser operations
- `AUTH_LOGIN` and `AUTH_PASSWORD` - Basic authentication credentials

## Development Conventions

### Coding Style
- Python code follows standard conventions with type hints
- Async/await patterns are used for I/O operations
- Extension system allows for modular functionality
- Error handling with custom exceptions (RepairableException, HandledException)

### Testing
- The codebase includes a `tests/` directory for unit and integration tests
- Testing framework follows the Python testing conventions
- New features should include appropriate test coverage

### Extensibility

The framework provides multiple extension points:
1. **Tools** - Add new capabilities in `python/tools/`
2. **Extensions** - Custom logic hooks in `python/extensions/`
3. **Prompts** - Modify agent behavior in `prompts/`
4. **Profiles** - Different agent configurations in `agents/`

## Security Considerations

- Agent Zero has powerful capabilities that can potentially be dangerous when misused
- Runs in isolated environments (like Docker) to limit potential damage
- Implements rate limiting to prevent API abuse
- Uses authentication for web UI access
- Implements CSRF protection for web interface

## Project Status & Capabilities

Agent Zero is a sophisticated agentic framework with the following capabilities:
- **Natural Language Processing** - Understands and responds to user requests
- **Code Execution** - Can run code in multiple languages safely
- **Web Browsing** - Can navigate and extract information from websites
- **Memory System** - Persistent memory for storing and retrieving information
- **Multi-agent Cooperation** - Can delegate tasks to subordinates
- **Knowledge Base** - Can query documents and information sources
- **Scheduling** - Task scheduling capabilities
- **API Integration** - Can connect to external services via MCP protocol

## Development Guidelines

### Adding New Tools
1. Create a new Python file in `python/tools/`
2. Inherit from the base `Tool` class
3. Implement the required methods
4. Tools are automatically discovered and loaded

### Modifying Agent Behavior
1. Edit the system prompts in the `prompts/` directory
2. The main system prompt is `prompts/agent.system.main.md`
3. Tool-specific prompts are in the same directory

### Configuration Changes
- Model provider configuration is in `conf/model_providers.yaml`
- Runtime settings are loaded from environment variables
- Default configurations can be found in `initialize.py`

## Quick Start for Developers

1. Set up your development environment with Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your API keys
4. Run with `python run_ui.py`
5. Access the UI at `http://localhost:50001`

The framework is designed for flexibility and extensibility - you can modify any aspect of the agent's behavior by adjusting the prompts, adding new tools, or implementing extensions.