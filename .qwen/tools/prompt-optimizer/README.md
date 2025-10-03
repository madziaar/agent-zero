# Qwen Prompt Optimizer

A comprehensive toolkit for analyzing, optimizing, and enhancing prompts specifically designed for Qwen models. This tool helps developers create more effective prompts that leverage Qwen's unique capabilities and improve response quality.

## Features

- **Prompt Analysis**: Analyze existing prompts for structure, clarity, and effectiveness
- **Optimization Suggestions**: Get specific recommendations for improving prompt performance
- **Qwen-Specific Enhancements**: Apply Qwen model-specific optimization techniques
- **Performance Metrics**: Measure prompt effectiveness and response quality
- **A/B Testing**: Compare different prompt variations
- **Template Management**: Create and manage prompt templates for common use cases

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer()

# Analyze an existing prompt
prompt = "Write a Python function to calculate fibonacci numbers"
analysis = optimizer.analyze_prompt(prompt)
print(f"Clarity Score: {analysis.clarity_score}")
print(f"Structure Score: {analysis.structure_score}")

# Get optimization suggestions
suggestions = optimizer.get_optimization_suggestions(prompt)
for suggestion in suggestions:
    print(f"- {suggestion}")
```

### Advanced Usage

```python
from prompt_optimizer import PromptOptimizer, QwenPromptTemplate

# Initialize with Qwen-specific configuration
optimizer = PromptOptimizer(
    model_type="qwen-coder",
    optimization_level="advanced"
)

# Create optimized prompt for coding tasks
template = QwenPromptTemplate.coding_task(
    task="implement a binary search algorithm",
    language="Python",
    constraints=["must be recursive", "include error handling"]
)

optimized_prompt = optimizer.optimize_prompt(template)
print(f"Optimized prompt: {optimized_prompt}")
```

## Core Components

### PromptOptimizer Class

Main class for prompt analysis and optimization.

**Methods:**

- `analyze_prompt(prompt: str) -> PromptAnalysis`: Analyze a prompt's effectiveness
- `optimize_prompt(prompt: str) -> str`: Optimize a prompt for better results
- `get_optimization_suggestions(prompt: str) -> List[str]`: Get specific improvement suggestions
- `compare_prompts(prompts: List[str]) -> ComparisonResult`: Compare multiple prompt variations

### QwenPromptTemplate Class

Specialized templates for common Qwen use cases.

**Available Templates:**

- `coding_task()`: Optimized for code generation tasks
- `debugging_task()`: Enhanced for debugging scenarios
- `explanation_task()`: Improved for explanatory requests
- `analysis_task()`: Tailored for code and system analysis

## Configuration

### Basic Configuration

```python
config = {
    "model_type": "qwen-coder",
    "optimization_level": "standard",  # basic, standard, advanced
    "focus_areas": ["clarity", "specificity", "context"],
    "output_format": "detailed"
}
```

### Advanced Configuration

```python
advanced_config = {
    "model_type": "qwen-coder",
    "optimization_level": "advanced",
    "qwen_specific_features": {
        "use_reasoning_tags": True,
        "context_window_optimization": True,
        "token_efficiency": True
    },
    "analysis_metrics": [
        "clarity_score",
        "specificity_score",
        "context_adequacy",
        "token_efficiency",
        "qwen_compatibility"
    ]
}
```

## Examples

### Example 1: Basic Prompt Optimization

```python
from prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer()

# Original prompt
original = "Fix this code"
optimized = optimizer.optimize_prompt(original)
print(f"Original: {original}")
print(f"Optimized: {optimized}")
```

### Example 2: Code Review Prompt Enhancement

```python
from prompt_optimizer import QwenPromptTemplate

# Create a code review template
template = QwenPromptTemplate.code_review(
    code_snippet="def calculate_total(items): return sum(items)",
    focus_areas=["performance", "readability", "error_handling"]
)

optimizer = PromptOptimizer()
optimized_prompt = optimizer.optimize_prompt(template)
```

### Example 3: A/B Testing Prompts

```python
prompts = [
    "Write a function to sort a list",
    "Create a Python function that sorts a list of numbers using an efficient algorithm",
    "Implement a sorting function with proper error handling and documentation"
]

results = optimizer.compare_prompts(prompts)
for i, result in enumerate(results):
    print(f"Prompt {i+1}: {result.effectiveness_score}")
```

## Integration with Agent Zero

### Basic Integration

```python
# In your Agent Zero workflow
from prompt_optimizer import PromptOptimizer

class QwenAgent:
    def __init__(self):
        self.optimizer = PromptOptimizer()

    def process_request(self, user_input: str):
        # Optimize the prompt before sending to Qwen
        optimized_prompt = self.optimizer.optimize_prompt(user_input)

        # Send to Qwen model
        response = self.call_qwen_model(optimized_prompt)

        return response
```

### Advanced Integration

```python
# Enhanced integration with context awareness
class AdvancedQwenAgent:
    def __init__(self):
        self.optimizer = PromptOptimizer(
            model_type="qwen-coder",
            context_aware=True
        )

    def optimize_with_context(self, prompt: str, context: dict):
        # Analyze context to improve optimization
        analysis = self.optimizer.analyze_prompt_with_context(prompt, context)

        # Apply context-specific optimizations
        optimized = self.optimizer.apply_context_optimizations(analysis)

        return optimized
```

## Best Practices

### For Coding Tasks

1. **Be Specific**: Include language, constraints, and expected output format
2. **Provide Context**: Include relevant code snippets or project information
3. **Use Structure**: Break complex tasks into clear, sequential steps
4. **Error Handling**: Specify how to handle edge cases and errors

### For Code Review

1. **Focus Areas**: Specify which aspects to review (performance, security, style)
2. **Code Context**: Provide surrounding code for better understanding
3. **Review Depth**: Specify whether you want high-level or detailed analysis

### For Debugging

1. **Clear Problem Description**: Describe symptoms and expected behavior
2. **Environment Details**: Include relevant environment and dependency information
3. **Error Messages**: Include full error messages and stack traces

## Performance Tips

- **Token Efficiency**: Optimized prompts use fewer tokens while maintaining clarity
- **Context Window**: Consider Qwen's context window when crafting prompts
- **Reasoning Integration**: Use reasoning tags for complex multi-step tasks
- **Batch Processing**: Process multiple related prompts together for efficiency

## Troubleshooting

### Common Issues

1. **Low Optimization Scores**: Check prompt clarity and add more specific details
2. **Poor Response Quality**: Ensure prompts align with Qwen's capabilities
3. **Token Limits**: Break very long prompts into smaller, focused requests

### Getting Help

For issues and questions:

1. Check the examples directory for usage patterns
2. Review the configuration options for your specific use case
3. Consult the integration guidelines for Agent Zero compatibility

## Contributing

Contributions are welcome! Please see the CONTRIBUTING.md file for guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
