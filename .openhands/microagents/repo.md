# Agent Zero Repository Overview

## Project Description

Agent Zero is a personal, organic agentic framework designed to grow and learn with you. Unlike predefined agentic frameworks, Agent Zero is dynamic, fully transparent, and completely customizable. It uses the computer as a tool to accomplish tasks, featuring persistent memory, multi-agent cooperation, and the ability to create its own tools as needed.

Key features include:
- **General-purpose Assistant**: Handles diverse tasks through natural language instructions
- **Computer as a Tool**: Uses the operating system directly rather than pre-programmed tools
- **Multi-agent Cooperation**: Agents can create subordinates to handle subtasks
- **Fully Customizable**: Everything from prompts to tools can be modified
- **Persistent Memory**: Learns and remembers solutions for future use

## File Structure Overview

```
agent-zero/
├── agent.py                 # Main agent class and core logic
├── run_ui.py                # Web UI server entry point
├── initialize.py            # Initialization and setup
├── models.py                # LLM model configurations
├── requirements.txt         # Python dependencies
├── python/                  # Core Python modules
│   ├── api/                 # Web API endpoints
│   ├── extensions/          # Extension system hooks
│   ├── helpers/             # Utility modules
│   └── tools/               # Default agent tools
├── prompts/                 # System prompts and templates
├── webui/                   # Frontend web interface
├── docs/                    # Comprehensive documentation
├── conf/                    # Configuration files
├── agents/                  # Agent profiles and configurations
├── instruments/             # Custom instruments/procedures
├── knowledge/               # Knowledge base storage
├── memory/                  # Persistent memory storage
├── logs/                    # Session logs and outputs
└── tests/                   # Test suite
```

## Running the Application

### Quick Start (Docker - Recommended)
```bash
# Pull and run with Docker
docker pull agent0ai/agent-zero
docker run -p 50001:80 agent0ai/agent-zero

# Visit http://localhost:50001 to start
```

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the web UI
python run_ui.py

# Or run in terminal mode
python agent.py
```

### Running Tests
```bash
# Run automated tests
python -m pytest tests/

# Run manual test scripts
python tests/manual/test_run_ui.py
```

## Developer Information

- **Main Entry Points**: `run_ui.py` (web interface), `agent.py` (terminal interface)
- **Configuration**: Modify files in `conf/` directory and `prompts/` for behavior changes
- **Custom Tools**: Add new tools in `python/tools/` directory
- **Extensions**: Hook into agent lifecycle via `python/extensions/`
- **Documentation**: Comprehensive guides available in `docs/` directory

The framework is designed to be completely transparent and hackable - every component can be inspected, modified, or extended to suit your needs.