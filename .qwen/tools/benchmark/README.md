# Qwen Benchmark Tools

A comprehensive toolkit for performance benchmarking and measuring Qwen model effectiveness. This tool suite helps developers evaluate Qwen's performance across various coding tasks, measure response quality, and track improvements over time.

## Features

- **Performance Benchmarking**: Measure Qwen's speed and accuracy across coding tasks
- **Quality Assessment**: Evaluate response quality, correctness, and completeness
- **Task-Specific Metrics**: Specialized benchmarks for different coding scenarios
- **Historical Tracking**: Track performance improvements over time
- **Comparative Analysis**: Compare Qwen performance against other models
- **Custom Test Suites**: Create and run custom benchmarking scenarios

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from benchmark import QwenBenchmark

# Initialize benchmark suite
benchmark = QwenBenchmark()

# Run basic performance test
results = benchmark.run_basic_test()
print(f"Average Response Time: {results.avg_response_time}ms")
print(f"Success Rate: {results.success_rate}%")
print(f"Quality Score: {results.quality_score}")
```

### Advanced Usage

```python
from benchmark import QwenBenchmark, BenchmarkConfig

# Configure benchmark suite
config = BenchmarkConfig(
    test_categories=['coding', 'debugging', 'optimization'],
    iterations=10,
    timeout=30,
    quality_threshold=0.8
)

benchmark = QwenBenchmark(config)

# Run comprehensive benchmark
results = benchmark.run_comprehensive_benchmark()
```

## Core Components

### QwenBenchmark Class

Main class for running benchmarks and measuring performance.

**Methods:**
- `run_basic_test() -> BasicBenchmarkResult`: Run basic performance test
- `run_comprehensive_benchmark() -> ComprehensiveBenchmarkResult`: Run full benchmark suite
- `run_custom_benchmark(test_cases: List[Dict]) -> CustomBenchmarkResult`: Run custom test cases
- `compare_models(model_results: Dict[str, Any]) -> ModelComparisonResult`: Compare multiple models

### BenchmarkConfig Class

Configuration for customizing benchmark behavior.

**Options:**
- `test_categories`: Categories of tests to run
- `iterations`: Number of iterations per test
- `timeout`: Timeout for individual tests
- `quality_threshold`: Minimum quality score to consider successful
- `include_detailed_metrics`: Whether to include detailed performance metrics

## Test Categories

### Coding Tasks
- **Algorithm Implementation**: Data structures and algorithms
- **Code Generation**: Function and class creation
- **Refactoring**: Code restructuring and improvement
- **API Development**: REST API and service creation

### Debugging Tasks
- **Error Analysis**: Error message interpretation
- **Bug Identification**: Finding and locating bugs
- **Fix Generation**: Creating fixes for identified issues
- **Root Cause Analysis**: Understanding why bugs occur

### Optimization Tasks
- **Performance Optimization**: Speed and efficiency improvements
- **Memory Optimization**: Memory usage reduction
- **Code Simplification**: Complexity reduction
- **Best Practices**: Following coding standards

### Analysis Tasks
- **Code Review**: Reviewing code for issues
- **Security Analysis**: Identifying security vulnerabilities
- **Architecture Analysis**: System design evaluation
- **Documentation**: Code documentation quality

## Quality Metrics

### Response Quality
- **Correctness**: Accuracy of the response
- **Completeness**: How complete the solution is
- **Clarity**: How clear and understandable the response is
- **Usefulness**: How helpful the response is for the task

### Performance Metrics
- **Response Time**: Time taken to generate response
- **Token Efficiency**: Quality per token used
- **Consistency**: Consistency across similar requests
- **Error Rate**: Frequency of errors or failures

### Code Quality (when applicable)
- **Functionality**: Does the code work as expected
- **Efficiency**: Performance of generated code
- **Readability**: How readable the generated code is
- **Best Practices**: Adherence to coding standards

## Examples

### Example 1: Basic Performance Test

```python
from benchmark import QwenBenchmark

benchmark = QwenBenchmark()

# Run basic test
basic_results = benchmark.run_basic_test()

print("Basic Performance Results:")
print(f"Response Time: {basic_results.avg_response_time}ms")
print(f"Success Rate: {basic_results.success_rate}%")
print(f"Quality Score: {basic_results.quality_score:.2f}")
```

### Example 2: Coding Task Benchmark

```python
# Test coding capabilities
coding_results = benchmark.run_coding_benchmark([
    "Implement binary search algorithm",
    "Create a REST API endpoint",
    "Write a unit test for sorting function"
])

print("Coding Performance:")
for result in coding_results:
    print(f"Task: {result.task}")
    print(f"Success: {result.success}")
    print(f"Quality: {result.quality_score:.2f}")
    print(f"Time: {result.response_time}ms")
```

### Example 3: Debugging Benchmark

```python
# Test debugging capabilities
debugging_results = benchmark.run_debugging_benchmark([
    {
        "error": "TypeError: 'int' object is not iterable",
        "code": "for item in items: process(item)",
        "expected_fix": "Check if items is iterable"
    }
])

print("Debugging Performance:")
for result in debugging_results:
    print(f"Error: {result.error_message}")
    print(f"Fix Quality: {result.fix_quality:.2f}")
    print(f"Root Cause Accuracy: {result.root_cause_accuracy:.2f}")
```

## Integration with Agent Zero

### Basic Integration

```python
# In your Agent Zero workflow
from benchmark import QwenBenchmark

class QwenPerformanceAgent:
    def __init__(self):
        self.benchmark = QwenBenchmark()

    def monitor_performance(self, user_request: str) -> dict:
        """Monitor Qwen performance for a request."""
        # Run benchmark before processing
        benchmark_result = self.benchmark.run_targeted_benchmark(user_request)

        # Process the request
        response = self.process_with_qwen(user_request)

        # Run benchmark after processing
        post_benchmark = self.benchmark.run_targeted_benchmark(user_request)

        return {
            "request": user_request,
            "response": response,
            "pre_benchmark": benchmark_result,
            "performance_impact": self._calculate_performance_impact(benchmark_result, post_benchmark)
        }
```

### Advanced Integration

```python
class PerformanceMonitoringAgent:
    def __init__(self):
        config = BenchmarkConfig(
            test_categories=['coding', 'debugging', 'optimization'],
            iterations=5,
            include_detailed_metrics=True
        )
        self.benchmark = QwenBenchmark(config)
        self.performance_history = []

    def continuous_monitoring(self):
        """Continuously monitor Qwen performance."""
        while True:
            # Run periodic benchmarks
            results = self.benchmark.run_comprehensive_benchmark()

            # Store results
            self.performance_history.append({
                "timestamp": datetime.now(),
                "results": results
            })

            # Check for performance degradation
            if self._detect_performance_degradation(results):
                self._handle_performance_issue(results)

            # Wait before next check
            time.sleep(3600)  # Check every hour

    def _detect_performance_degradation(self, current_results) -> bool:
        """Detect if performance has degraded."""
        if len(self.performance_history) < 2:
            return False

        # Compare with recent history
        recent_results = [r["results"] for r in self.performance_history[-5:]]
        avg_recent_score = sum(r.quality_score for r in recent_results) / len(recent_results)

        return current_results.quality_score < avg_recent_score * 0.9  # 10% degradation
```

## Configuration

### Basic Configuration

```python
config = BenchmarkConfig(
    test_categories=['coding', 'debugging'],
    iterations=5,
    timeout=30,
    quality_threshold=0.7
)
```

### Advanced Configuration

```python
advanced_config = BenchmarkConfig(
    test_categories=['coding', 'debugging', 'optimization', 'analysis'],
    iterations=10,
    timeout=60,
    quality_threshold=0.8,
    include_detailed_metrics=True,
    custom_test_cases=[
        {
            "category": "security",
            "task": "Identify security vulnerabilities in login code",
            "evaluation_criteria": ["identifies_sql_injection", "suggests_input_validation"]
        }
    ],
    performance_targets={
        "max_response_time": 5000,  # 5 seconds
        "min_quality_score": 0.8,
        "min_success_rate": 0.9
    }
)
```

## Benchmark Results

### Basic Results

```python
@dataclass
class BasicBenchmarkResult:
    avg_response_time: float
    success_rate: float
    quality_score: float
    total_requests: int
    successful_requests: int
```

### Comprehensive Results

```python
@dataclass
class ComprehensiveBenchmarkResult:
    overall_score: float
    category_scores: Dict[str, float]
    detailed_metrics: Dict[str, Any]
    recommendations: List[str]
    performance_trends: List[float]
```

### Custom Results

```python
@dataclass
class CustomBenchmarkResult:
    test_results: List[Dict[str, Any]]
    summary_statistics: Dict[str, float]
    custom_metrics: Dict[str, Any]
    insights: List[str]
```

## Best Practices

### For Benchmarking
1. **Regular Testing**: Run benchmarks regularly to track performance
2. **Representative Tests**: Use test cases that represent real usage patterns
3. **Proper Evaluation**: Use clear criteria for evaluating response quality
4. **Statistical Significance**: Run enough iterations for reliable results

### For Performance Monitoring
1. **Automated Monitoring**: Set up continuous monitoring for production systems
2. **Alert Thresholds**: Define thresholds for performance degradation alerts
3. **Historical Analysis**: Track performance trends over time
4. **Resource Monitoring**: Monitor system resources during benchmarking

### For Quality Assessment
1. **Multiple Criteria**: Use multiple quality metrics for comprehensive evaluation
2. **Human Validation**: Include human validation for subjective quality measures
3. **Context Awareness**: Consider the context and complexity of tasks
4. **Fair Comparison**: Ensure fair comparison between different models/versions

## Custom Test Cases

### Creating Custom Tests

```python
def create_custom_test_case(task: str, expected_patterns: List[str], evaluation_criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Create a custom test case."""
    return {
        "task": task,
        "expected_patterns": expected_patterns,
        "evaluation_criteria": evaluation_criteria,
        "category": "custom",
        "difficulty": "medium"
    }

# Example custom test
custom_test = create_custom_test_case(
    task="Create a Python decorator for timing functions",
    expected_patterns=["@timing", "def timing", "time.perf_counter"],
    evaluation_criteria={
        "correctness": 0.4,
        "completeness": 0.3,
        "efficiency": 0.2,
        "readability": 0.1
    }
)
```

### Running Custom Benchmarks

```python
# Create custom test suite
custom_tests = [
    create_custom_test_case(
        task="Implement a cache decorator",
        expected_patterns=["functools.lru_cache", "@cache"],
        evaluation_criteria={"performance_impact": 0.5, "correctness": 0.5}
    ),
    create_custom_test_case(
        task="Create a data validation function",
        expected_patterns=["raise ValueError", "if not isinstance"],
        evaluation_criteria={"security": 0.6, "robustness": 0.4}
    )
]

# Run custom benchmark
custom_results = benchmark.run_custom_benchmark(custom_tests)
```

## Performance Tips

- **Batch Testing**: Test multiple scenarios together for efficiency
- **Caching**: Cache test results to avoid redundant evaluations
- **Parallel Execution**: Run independent tests in parallel when possible
- **Resource Management**: Monitor and manage system resources during benchmarking

## Troubleshooting

### Common Issues

1. **Inconsistent Results**: Increase iterations for more stable results
2. **Timeout Issues**: Adjust timeout settings based on task complexity
3. **Quality Evaluation**: Refine evaluation criteria for better assessment
4. **Resource Constraints**: Monitor system resources and optimize accordingly

### Debugging

```python
def debug_benchmark_issue(test_case: Dict[str, Any]) -> Dict[str, Any]:
    """Debug benchmark issues."""
    # Run single test with detailed logging
    result = benchmark.run_single_test(test_case, debug=True)

    return {
        "test_case": test_case,
        "result": result,
        "evaluation_details": result.evaluation_breakdown,
        "performance_metrics": result.detailed_metrics,
        "suggested_fixes": result.suggested_improvements
    }
```

## Contributing

Contributions are welcome! Please see the CONTRIBUTING.md file for guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.