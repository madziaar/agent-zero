# Agent Zero - Agent Profiles Summary

This directory contains the extracted prompts for various Agent Zero profiles. Below is a summary of all identified agent profiles in the system:

## Agent Profiles

### 1. Agent Zero (agent0)
- **Purpose**: Main top-level agent that communicates with the user and delegates to subordinates
- **Specialization**: General-purpose assistant with communication skills and formatted output
- **Key Prompts**:
  - `agent.system.main.role.md` - Defines the role as the top-level agent with general AI assistance
  - `agent.system.tool.response.md` - Specifies how the response tool should be used for final answers

### 2. Developer
- **Purpose**: Specialized in complex software development
- **Specialization**: Software architecture, implementation, and development lifecycle management
- **Key Prompts**:
  - `agent.system.main.role.md` - Defines the role as 'Master Developer' with comprehensive software engineering capabilities
  - `agent.system.main.communication.md` - Communication guidelines for requirements elicitation and structured interviews

### 3. Hacker
- **Purpose**: Specialized in cyber security and penetration testing
- **Specialization**: Both red and blue team security testing
- **Key Prompts**:
  - `agent.system.main.role.md` - Defines the role as a cybersecurity professional working in penetration testing
  - `agent.system.main.environment.md` - Details about the Kali Linux environment and security tools

### 4. Researcher
- **Purpose**: Specialized in research, data analysis, and reporting
- **Specialization**: Corporate research, academic analysis, and data mining
- **Key Prompts**:
  - `agent.system.main.role.md` - Defines the role as 'Deep Research' agent with analytical mastery
  - `agent.system.main.communication.md` - Communication guidelines for research requirements and systematic analysis

### 5. Analyst
- **Purpose**: Specialized in business analysis and strategic insights
- **Specialization**: Process analysis, requirements engineering, and business intelligence
- **Key Prompts**:
  - `agent.system.main.role.md` - Defines the role as 'Business Analyst' with comprehensive analytical capabilities
  - `agent.system.main.communication.md` - Communication guidelines for business analysis requirements and structured interviews

### 6. Qwen Coder
- **Purpose**: Specialized in software development optimized for Qwen AI models
- **Specialization**: Multi-language coding, Qwen-specific optimization, architecture design
- **Key Prompts**:
  - `agent.system.main.role.md` - Defines the role as 'Qwen Coder' with comprehensive coding capabilities
  - `agent.system.main.communication.md` - Communication guidelines for coding requirements and structured interviews

### 7. Default
- **Purpose**: Contains default prompt templates that should be inherited and overridden by specialized profiles
- **Specialization**: General template for other agent profiles

### 8. Example
- **Purpose**: Example agent profile with extensions, prompts, and tools directories
- **Specialization**: Serves as a template or example for creating new agent profiles

## Notes
- Each agent profile is designed to specialize in specific domains while maintaining the core Agent Zero framework
- The agent0 profile serves as the primary interface between users and the agent system
- Specialized profiles (developer, hacker, researcher, analyst, qwen-coder) can be used as subordinates to handle domain-specific tasks
- The system supports hierarchical delegation where higher-level agents can delegate tasks to specialized subordinates