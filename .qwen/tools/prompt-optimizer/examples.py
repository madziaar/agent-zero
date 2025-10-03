#!/usr/bin/env python3
"""
Example usage scenarios for the Qwen Prompt Optimizer.

This file demonstrates practical applications and integration patterns
for using the prompt optimizer in real-world scenarios.
"""

from prompt_optimizer import PromptOptimizer, QwenPromptTemplate, OptimizationConfig, ModelType, OptimizationLevel
import json
import sys
import os

# Add the current directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def example_basic_usage():
    """Demonstrate basic prompt analysis and optimization."""
    print("=== Basic Usage Example ===\n")

    # Initialize the optimizer
    optimizer = PromptOptimizer()

    # Example prompts to analyze
    prompts = [
        "Fix this code",  # Poor prompt
        "Help me debug this Python function",  # Better prompt
        "I need a Python function that calculates fibonacci numbers with memoization, includes error handling, and has clear documentation"  # Excellent prompt
    ]

    for i, prompt in enumerate(prompts, 1):
        print(f"Prompt {i}: {prompt}")

        # Analyze the prompt
        analysis = optimizer.analyze_prompt(prompt)

        print(f"Overall Score: {analysis.overall_score:.3f}")
        print(f"Clarity: {analysis.clarity_score:.3f}")
        print(f"Specificity: {analysis.specificity_score:.3f}")
        print(f"Structure: {analysis.structure_score:.3f}")
        print(f"Qwen Compatibility: {analysis.qwen_compatibility:.3f}")

        # Get suggestions
        suggestions = optimizer.get_optimization_suggestions(prompt)
        print(f"Suggestions: {suggestions[0] if suggestions else 'None'}")
        print()

    # Optimize a prompt
    basic_prompt = "Write code for sorting"
    optimized = optimizer.optimize_prompt(basic_prompt)

    print(f"Original: {basic_prompt}")
    print(f"Optimized: {optimized}")
    print()


def example_coding_tasks():
    """Demonstrate optimization for coding-specific tasks."""
    print("=== Coding Tasks Example ===\n")

    optimizer = PromptOptimizer()

    # Create a coding task using the template
    template = QwenPromptTemplate.coding_task(
        task="implement a binary search algorithm",
        language="Python",
        constraints=["must be recursive",
                     "include error handling", "add unit tests"]
    )

    print("Generated Template:")
    print(template)
    print()

    # Analyze and optimize the template
    analysis = optimizer.analyze_prompt(template)
    print(f"Template Analysis Score: {analysis.overall_score:.3f}")

    # Get specific suggestions
    suggestions = optimizer.get_optimization_suggestions(template)
    print("Optimization Suggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion}")
    print()


def example_code_review():
    """Demonstrate optimization for code review tasks."""
    print("=== Code Review Example ===\n")

    optimizer = PromptOptimizer()

    # Example code snippet for review
    code_snippet = '''
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
'''

    # Create a code review prompt
    review_prompt = QwenPromptTemplate.code_review(
        code_snippet=code_snippet,
        focus_areas=["performance", "readability", "error_handling"]
    )

    print("Code Review Prompt:")
    print(review_prompt)
    print()

    # Analyze the prompt
    analysis = optimizer.analyze_prompt(review_prompt)
    print(f"Review Prompt Score: {analysis.overall_score:.3f}")
    print(f"Strengths: {', '.join(analysis.strengths)}")
    print()


def example_debugging_tasks():
    """Demonstrate optimization for debugging tasks."""
    print("=== Debugging Tasks Example ===\n")

    optimizer = PromptOptimizer()

    # Create a debugging prompt
    debug_prompt = QwenPromptTemplate.debugging_task(
        error_description="TypeError: 'int' object is not iterable",
        code_context="In a function that processes user data",
        environment="Python 3.9, Flask application"
    )

    print("Debugging Prompt:")
    print(debug_prompt)
    print()

    # Analyze the prompt
    analysis = optimizer.analyze_prompt(debug_prompt)
    print(f"Debug Prompt Score: {analysis.overall_score:.3f}")
    print(f"Issues found: {', '.join(analysis.issues)}")
    print()


def example_prompt_comparison():
    """Demonstrate comparing multiple prompt variations."""
    print("=== Prompt Comparison Example ===\n")

    optimizer = PromptOptimizer()

    # Different approaches to the same task
    prompt_variations = [
        "Sort this list",
        "Write a function to sort a list in Python",
        "Implement an efficient sorting algorithm for a list of integers with error handling and documentation",
        "Create a Python function that sorts a list using quicksort algorithm, handles edge cases, includes comprehensive documentation, and provides usage examples"
    ]

    print("Comparing Prompt Variations:")
    for i, prompt in enumerate(prompt_variations, 1):
        print(f"{i}. {prompt}")
    print()

    # Compare all variations
    comparison = optimizer.compare_prompts(prompt_variations)

    print("Comparison Results:")
    print(f"Best Prompt Index: {comparison.best_prompt_index + 1}")
    print(f"Scores: {[f'{score:.3f}' for score in comparison.prompt_scores]}")
    print()

    print("Recommendations:")
    for rec in comparison.recommendations:
        print(f"- {rec}")
    print()


def example_advanced_configuration():
    """Demonstrate advanced configuration and customization."""
    print("=== Advanced Configuration Example ===\n")

    # Create custom configuration
    config = OptimizationConfig(
        model_type=ModelType.QWEN_CODER,
        optimization_level=OptimizationLevel.ADVANCED,
        focus_areas=["clarity", "specificity",
                     "context", "qwen_compatibility"],
        qwen_specific_features={
            "use_reasoning_tags": True,
            "context_window_optimization": True,
            "token_efficiency": True
        }
    )

    # Initialize optimizer with custom config
    optimizer = PromptOptimizer(config)

    # Test with a complex prompt
    complex_prompt = """
    I need help with a programming problem. I have some data and I want to process it.
    There are some issues with the current implementation but I'm not sure what's wrong.
    Can you help me figure out how to fix it?
    """

    print(f"Original Prompt: {complex_prompt.strip()}")
    print()

    # Analyze with advanced configuration
    analysis = optimizer.analyze_prompt(complex_prompt)

    print("Advanced Analysis:")
    print(f"Overall Score: {analysis.overall_score:.3f}")
    metrics = {k: f'{v:.3f}' for k, v in analysis.__dict__.items()
               if isinstance(v, float)}
    print(f"All Metrics: {metrics}")
    print()

    # Get detailed suggestions
    suggestions = optimizer.get_optimization_suggestions(complex_prompt)
    print("Detailed Suggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion}")
    print()


def example_agent_zero_integration():
    """Demonstrate integration with Agent Zero workflow."""
    print("=== Agent Zero Integration Example ===\n")

    class QwenAgentWithOptimizer:
        """Example agent that uses prompt optimization."""

        def __init__(self):
            self.config = OptimizationConfig(model_type=ModelType.QWEN_CODER)
            self.optimizer = PromptOptimizer(self.config)

        def process_request(self, user_input: str) -> str:
            """Process a user request with prompt optimization."""
            print(f"Original Request: {user_input}")

            # Analyze the input prompt
            analysis = self.optimizer.analyze_prompt(user_input)

            # Optimize the prompt before sending to Qwen
            optimized_prompt = self.optimizer.optimize_prompt(user_input)

            print(f"Optimization Score: {analysis.overall_score:.3f}")
            print(f"Optimized Prompt: {optimized_prompt}")

            # Here you would send the optimized prompt to Qwen
            # response = self.call_qwen_model(optimized_prompt)

            return optimized_prompt

        def batch_optimize(self, requests: list) -> list:
            """Batch optimize multiple requests."""
            return [self.process_request(req) for req in requests]

    # Example usage
    agent = QwenAgentWithOptimizer()

    requests = [
        "Help me write Python code",
        "Debug this error message",
        "Review my code for performance issues"
    ]

    print("Batch Processing:")
    optimized_requests = agent.batch_optimize(requests)

    for i, (original, optimized) in enumerate(zip(requests, optimized_requests), 1):
        print(f"\nRequest {i}:")
        print(f"Original: {original}")
        print(f"Optimized: {optimized}")
    print()


def example_cli_interface():
    """Demonstrate a simple CLI interface."""
    print("=== CLI Interface Example ===\n")

    def interactive_mode():
        """Simple interactive mode for testing prompts."""
        optimizer = PromptOptimizer()

        print("Qwen Prompt Optimizer - Interactive Mode")
        print("Enter 'quit' to exit")
        print()

        while True:
            user_input = input("Enter a prompt to analyze: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            if not user_input:
                continue

            # Analyze the prompt
            analysis = optimizer.analyze_prompt(user_input)

            print(f"\nOverall Score: {analysis.overall_score:.3f}")
            print(f"Clarity: {analysis.clarity_score:.3f}")
            print(f"Specificity: {analysis.specificity_score:.3f}")
            print(f"Structure: {analysis.structure_score:.3f}")

            # Show top suggestion
            suggestions = optimizer.get_optimization_suggestions(user_input)
            if suggestions:
                print(f"Top Suggestion: {suggestions[0]}")

            # Ask if they want to optimize
            optimize = input("\nOptimize this prompt? (y/n): ").lower().strip()
            if optimize == 'y':
                optimized = optimizer.optimize_prompt(user_input)
                print(f"\nOptimized: {optimized}")

            print("\n" + "="*50 + "\n")

    # Uncomment to run interactive mode
    # interactive_mode()


def main():
    """Run all examples."""
    print("Qwen Prompt Optimizer - Examples and Demonstrations\n")
    print("=" * 60 + "\n")

    # Run all examples
    examples = [
        example_basic_usage,
        example_coding_tasks,
        example_code_review,
        example_debugging_tasks,
        example_prompt_comparison,
        example_advanced_configuration,
        example_agent_zero_integration,
        # example_cli_interface,  # Uncomment to enable interactive mode
    ]

    for example in examples:
        try:
            example()
            print("\n" + "=" * 60 + "\n")
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
            print()

    print("All examples completed!")


if __name__ == "__main__":
    main()
