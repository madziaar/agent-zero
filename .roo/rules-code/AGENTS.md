# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Model Wrapper Inheritance Hierarchy

The system implements a sophisticated model wrapper inheritance hierarchy that enables specialized behavior for different use cases:

- **LiteLLMChatWrapper**: Base wrapper providing core LiteLLM integration with unified calling interface for all chat models
- **BrowserCompatibleChatWrapper**: Inherits from LiteLLMChatWrapper to add browser-specific message filtering and sanitization for web-based LLM interactions
- **LiteLLMEmbeddingWrapper**: Separate wrapper for embedding models with optimized batch processing capabilities
- **LocalSentenceTransformerWrapper**: Alternative local embedding implementation that bypasses LiteLLM for HuggingFace sentence-transformer models

## Advanced Reasoning Handling Patterns

The reasoning system implements dual-mode reasoning detection that would surprise experienced developers:

- **Native Reasoning Detection**: Automatically detects and separates native reasoning content from model responses without manual parsing
- **Fallback Thinking Tag Parsing**: Manual parsing system for thinking tags (`<think>`, `<reasoning>`) when native detection fails, with sophisticated partial tag handling
- **Streaming Reasoning Integration**: Real-time reasoning extraction during streaming responses with proper chunk boundary management

## Sophisticated Background Initialization Process Order

The initialization sequence requires strict ordering of background processes:

1. **Chat Persistence**: Must initialize before MCP servers to ensure chat history availability
2. **MCP Server Initialization**: Requires settings to be loaded but can run parallel to other systems
3. **Job Loop Activation**: Depends on MCP being ready but can initialize during other processes
4. **Model Preloading**: Final step requiring all other systems to be operational

## Multi-Layer Authentication Coordination Mechanisms

The authentication system implements coordinated multi-layer security that requires understanding the interaction patterns:

- **Loopback Address Validation**: Network-level filtering that blocks external access attempts
- **API Key Authentication**: Token-based auth integrated with MCP server authentication system
- **HTTP Basic Authentication**: Username/password protection for web interface access
- **CSRF Token Integration**: Session-based protection that validates against runtime ID-embedded cookies
- **Runtime ID Session Binding**: Each session cookie includes the instance runtime ID for complete isolation
