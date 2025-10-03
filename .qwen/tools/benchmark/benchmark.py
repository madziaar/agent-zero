#!/usr/bin/env python3
"""
Qwen Benchmark Tools - Core functionality for performance benchmarking and measuring Qwen model effectiveness.

This module provides comprehensive benchmarking capabilities to measure Qwen's performance
across various coding tasks and track improvements over time.
"""

import time
import asyncio
import statistics
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestCategory(Enum):
    """Categories of benchmark tests."""
    CODING = "coding"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"
    ANALYSIS = "analysis"
    CUSTOM = "custom"


class QualityCriteria(Enum):
    """Quality assessment criteria."""
    CORRECTNESS = "correctness"
    COMPLETENESS = "completeness"
    CLARITY = "clarity"
    USEFULNESS = "usefulness"
    EFFICIENCY = "efficiency"


@dataclass
class TestCase:
    """A single test case for benchmarking."""
    id: str
    category: TestCategory
    task: str
    expected_patterns: List[str]
    evaluation_criteria: Dict[str, float]
    difficulty: str
    timeout: int = 30


@dataclass
class TestResult:
    """Result of a single test execution."""
    test_id: str
    success: bool
    response_time: float
    quality_scores: Dict[str, float]
    overall_quality: float
    response: str
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class BenchmarkResult:
    """Results of a benchmark run."""
    timestamp: datetime
    total_tests: int
    successful_tests: int
    avg_response_time: float
    quality_score: float
    success_rate: float
    category_scores: Dict[str, float]
    recommendations: List[str]


@dataclass
class BenchmarkConfig:
    """Configuration for benchmark execution."""
    test_categories: List[TestCategory]
    iterations: int = 5
    timeout: int = 30
    quality_threshold: float = 0.7
    include_detailed_metrics: bool = True
    custom_test_cases: List[TestCase] = None

    def __post_init__(self):
        if self.custom_test_cases is None:
            self.custom_test_cases = []


class QwenBenchmark:
    """Main benchmarking class for Qwen models."""

    def __init__(self, config: BenchmarkConfig = None):
        """Initialize the benchmark suite."""
        self.config = config or BenchmarkConfig(
            test_categories=[TestCategory.CODING, TestCategory.DEBUGGING]
        )
        self.test_cases = self._initialize_test_cases()
        self.results_history = []

    def _initialize_test_cases(self) -> Dict[TestCategory, List[TestCase]]:
        """Initialize built-in test cases."""
        return {
            TestCategory.CODING: [
                TestCase(
                    id="coding_001",
                    category=TestCategory.CODING,
                    task="Implement a binary search algorithm in Python",
                    expected_patterns=["def binary_search", "mid = ", "return "],
                    evaluation_criteria={
                        "correctness": 0.4,
                        "completeness": 0.3,
                        "efficiency": 0.2,
                        "readability": 0.1
                    },
                    difficulty="medium"
                ),
                TestCase(
                    id="coding_002",
                    category=TestCategory.CODING,
                    task="Create a Python class for a simple bank account",
                    expected_patterns=["class BankAccount", "def __init__", "def deposit", "def withdraw"],
                    evaluation_criteria={
                        "correctness": 0.3,
                        "completeness": 0.3,
                        "encapsulation": 0.2,
                        "documentation": 0.2
                    },
                    difficulty="easy"
                ),
                TestCase(
                    id="coding_003",
                    category=TestCategory.CODING,
                    task="Write a function to find the longest common subsequence",
                    expected_patterns=["def lcs", "dynamic programming", "dp[", "return"],
                    evaluation_criteria={
                        "correctness": 0.5,
                        "efficiency": 0.3,
                        "clarity": 0.2
                    },
                    difficulty="hard"
                )
            ],
            TestCategory.DEBUGGING: [
                TestCase(
                    id="debug_001",
                    category=TestCategory.DEBUGGING,
                    task="Fix the TypeError: 'int' object is not iterable",
                    expected_patterns=["for item in", "if not isinstance", "try-except"],
                    evaluation_criteria={
                        "root_cause_accuracy": 0.4,
                        "fix_correctness": 0.4,
                        "prevention_suggestion": 0.2
                    },
                    difficulty="medium"
                ),
                TestCase(
                    id="debug_002",
                    category=TestCategory.DEBUGGING,
                    task="Debug this function that should calculate factorial",
                    expected_patterns=["def factorial", "if n == 0", "return 1", "return n *"],
                    evaluation_criteria={
                        "bug_identification": 0.3,
                        "fix_implementation": 0.4,
                        "edge_case_handling": 0.3
                    },
                    difficulty="easy"
                )
            ],
            TestCategory.OPTIMIZATION: [
                TestCase(
                    id="opt_001",
                    category=TestCategory.OPTIMIZATION,
                    task="Optimize this O(n²) sorting algorithm",
                    expected_patterns=["def ", "quicksort", "partition", "pivot"],
                    evaluation_criteria={
                        "algorithm_choice": 0.3,
                        "implementation_correctness": 0.3,
                        "performance_improvement": 0.4
                    },
                    difficulty="medium"
                ),
                TestCase(
                    id="opt_002",
                    category=TestCategory.OPTIMIZATION,
                    task="Reduce memory usage in this data processing function",
                    expected_patterns=["generator", "yield", "memory", "efficient"],
                    evaluation_criteria={
                        "memory_optimization": 0.4,
                        "correctness_preservation": 0.3,
                        "performance_maintenance": 0.3
                    },
                    difficulty="hard"
                )
            ],
            TestCategory.ANALYSIS: [
                TestCase(
                    id="analysis_001",
                    category=TestCategory.ANALYSIS,
                    task="Review this code for security vulnerabilities",
                    expected_patterns=["input validation", "SQL injection", "XSS", "security"],
                    evaluation_criteria={
                        "vulnerability_identification": 0.4,
                        "risk_assessment": 0.3,
                        "mitigation_suggestions": 0.3
                    },
                    difficulty="medium"
                ),
                TestCase(
                    id="analysis_002",
                    category=TestCategory.ANALYSIS,
                    task="Analyze the time complexity of this algorithm",
                    expected_patterns=["O(", "time complexity", "Big O", "analysis"],
                    evaluation_criteria={
                        "complexity_accuracy": 0.5,
                        "explanation_clarity": 0.3,
                        "completeness": 0.2
                    },
                    difficulty="medium"
                )
            ]
        }

    def run_basic_test(self) -> BenchmarkResult:
        """Run a basic performance test."""
        # Use a subset of test cases for basic testing
        basic_tests = []
        for category in [TestCategory.CODING, TestCategory.DEBUGGING]:
            basic_tests.extend(self.test_cases[category][:2])  # First 2 tests per category

        return self._run_benchmark(basic_tests, iterations=3)

    def run_comprehensive_benchmark(self) -> BenchmarkResult:
        """Run comprehensive benchmark across all categories."""
        all_tests = []
        for category_tests in self.test_cases.values():
            all_tests.extend(category_tests)

        return self._run_benchmark(all_tests, iterations=self.config.iterations)

    def run_coding_benchmark(self, custom_coding_tasks: List[str] = None) -> BenchmarkResult:
        """Run benchmark focused on coding tasks."""
        coding_tests = self.test_cases[TestCategory.CODING].copy()

        # Add custom coding tasks if provided
        if custom_coding_tasks:
            for i, task in enumerate(custom_coding_tasks, len(coding_tests) + 1):
                coding_tests.append(TestCase(
                    id=f"coding_custom_{i}",
                    category=TestCategory.CODING,
                    task=task,
                    expected_patterns=["def ", "class ", "return "],
                    evaluation_criteria={
                        "correctness": 0.4,
                        "completeness": 0.3,
                        "readability": 0.3
                    },
                    difficulty="medium"
                ))

        return self._run_benchmark(coding_tests, iterations=self.config.iterations)

    def run_debugging_benchmark(self, debugging_scenarios: List[Dict[str, Any]] = None) -> BenchmarkResult:
        """Run benchmark focused on debugging tasks."""
        debug_tests = self.test_cases[TestCategory.DEBUGGING].copy()

        # Add custom debugging scenarios if provided
        if debugging_scenarios:
            for i, scenario in enumerate(debugging_scenarios, len(debug_tests) + 1):
                debug_tests.append(TestCase(
                    id=f"debug_custom_{i}",
                    category=TestCategory.DEBUGGING,
                    task=scenario.get("task", "Debug this code issue"),
                    expected_patterns=scenario.get("expected_patterns", ["fix", "solution"]),
                    evaluation_criteria=scenario.get("evaluation_criteria", {
                        "fix_correctness": 0.5,
                        "explanation_quality": 0.5
                    }),
                    difficulty="medium"
                ))

        return self._run_benchmark(debug_tests, iterations=self.config.iterations)

    def run_custom_benchmark(self, test_cases: List[TestCase]) -> BenchmarkResult:
        """Run benchmark with custom test cases."""
        return self._run_benchmark(test_cases, iterations=self.config.iterations)

    def _run_benchmark(self, tests: List[TestCase], iterations: int = 5) -> BenchmarkResult:
        """Run benchmark with specified test cases."""
        start_time = datetime.now()
        all_results = []

        logger.info(f"Starting benchmark with {len(tests)} tests, {iterations} iterations each")

        for test_case in tests:
            test_results = []

            for iteration in range(iterations):
                try:
                    result = self._execute_test(test_case)
                    test_results.append(result)

                    # Small delay between iterations
                    time.sleep(0.5)

                except Exception as e:
                    logger.error(f"Error in iteration {iteration} for test {test_case.id}: {e}")
                    test_results.append(TestResult(
                        test_id=test_case.id,
                        success=False,
                        response_time=0,
                        quality_scores={},
                        overall_quality=0,
                        response="",
                        error=str(e)
                    ))

            all_results.extend(test_results)

        # Calculate aggregate results
        successful_tests = [r for r in all_results if r.success]
        success_rate = len(successful_tests) / len(all_results) if all_results else 0

        avg_response_time = statistics.mean([r.response_time for r in successful_tests]) if successful_tests else 0

        # Calculate quality scores
        quality_scores = [r.overall_quality for r in successful_tests]
        avg_quality = statistics.mean(quality_scores) if quality_scores else 0

        # Calculate category scores
        category_scores = self._calculate_category_scores(all_results)

        # Generate recommendations
        recommendations = self._generate_recommendations(all_results, avg_quality, success_rate)

        result = BenchmarkResult(
            timestamp=start_time,
            total_tests=len(all_results),
            successful_tests=len(successful_tests),
            avg_response_time=avg_response_time,
            quality_score=avg_quality,
            success_rate=success_rate,
            category_scores=category_scores,
            recommendations=recommendations
        )

        # Store in history
        self.results_history.append(result)

        logger.info(f"Benchmark completed. Success rate: {success_rate:.2%}, Quality: {avg_quality:.3f}")
        return result

    def _execute_test(self, test_case: TestCase) -> TestResult:
        """Execute a single test case."""
        start_time = time.time()

        try:
            # Simulate Qwen API call (replace with actual implementation)
            response = self._simulate_qwen_response(test_case.task)

            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Evaluate response quality
            quality_scores = self._evaluate_response_quality(response, test_case)
            overall_quality = sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0

            success = overall_quality >= self.config.quality_threshold

            return TestResult(
                test_id=test_case.id,
                success=success,
                response_time=response_time,
                quality_scores=quality_scores,
                overall_quality=overall_quality,
                response=response
            )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return TestResult(
                test_id=test_case.id,
                success=False,
                response_time=response_time,
                quality_scores={},
                overall_quality=0,
                response="",
                error=str(e)
            )

    def _simulate_qwen_response(self, task: str) -> str:
        """Simulate Qwen model response (replace with actual Qwen API call)."""
        # This is a simulation - replace with actual Qwen API integration

        # Simulate processing time
        time.sleep(0.5 + (hash(task) % 100) / 1000)  # 0.5-1.5 seconds

        # Generate simulated response based on task type
        if "binary search" in task.lower():
            return """```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```"""
        elif "bank account" in task.lower():
            return """```python
class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance
```"""
        elif "debug" in task.lower() or "fix" in task.lower():
            return """The TypeError: 'int' object is not iterable usually occurs when you try to iterate over an integer instead of an iterable object.

**Root Cause:** The variable `items` is expected to be a list or other iterable, but it's receiving an integer value.

**Solution:** Add a type check before iteration:

```python
def process_data(data):
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")

    for item in data:
        print(f"Processing: {item}")
```

**Prevention:** Always validate input types and provide meaningful error messages."""

        else:
            return """Here's a solution for your request:

```python
# Example implementation
def example_function():
    '''This is an example function that demonstrates the solution.'''
    return "Hello, World!"
```

This implementation provides a clean, efficient solution that follows Python best practices."""

    def _evaluate_response_quality(self, response: str, test_case: TestCase) -> Dict[str, float]:
        """Evaluate the quality of a response."""
        scores = {}

        for criterion, weight in test_case.evaluation_criteria.items():
            score = self._evaluate_criterion(response, criterion, test_case)
            scores[criterion] = score * weight

        return scores

    def _evaluate_criterion(self, response: str, criterion: str, test_case: TestCase) -> float:
        """Evaluate a specific quality criterion."""
        response_lower = response.lower()

        if criterion == "correctness":
            # Check if expected patterns are present
            found_patterns = sum(1 for pattern in test_case.expected_patterns
                               if pattern.lower() in response_lower)
            return min(1.0, found_patterns / len(test_case.expected_patterns))

        elif criterion == "completeness":
            # Check if response is substantial
            word_count = len(response.split())
            # Expect at least 50 words for complete response
            return min(1.0, word_count / 50)

        elif criterion == "clarity":
            # Check for clear explanations
            clarity_indicators = ["explanation", "example", "step by step", "clearly"]
            found_indicators = sum(1 for indicator in clarity_indicators
                                 if indicator in response_lower)
            return min(1.0, found_indicators / 3)

        elif criterion == "usefulness":
            # Check if response provides actionable information
            usefulness_indicators = ["```", "example", "solution", "implementation"]
            found_indicators = sum(1 for indicator in usefulness_indicators
                                 if indicator in response_lower)
            return min(1.0, found_indicators / 3)

        elif criterion == "efficiency":
            # Check for efficient solutions
            efficiency_indicators = ["optimize", "efficient", "performance", "O(", "algorithm"]
            found_indicators = sum(1 for indicator in efficiency_indicators
                                 if indicator in response_lower)
            return min(1.0, found_indicators / 3)

        elif criterion == "root_cause_accuracy":
            # Check for accurate root cause identification
            accuracy_indicators = ["root cause", "reason", "because", "issue is", "problem is"]
            found_indicators = sum(1 for indicator in accuracy_indicators
                                 if indicator in response_lower)
            return min(1.0, found_indicators / 3)

        elif criterion == "fix_correctness":
            # Check if fix is correct
            fix_indicators = ["solution", "fix", "correct", "resolve", "answer"]
            found_indicators = sum(1 for indicator in fix_indicators
                                 if indicator in response_lower)
            return min(1.0, found_indicators / 3)

        else:
            # Default scoring for unknown criteria
            return 0.5

    def _calculate_category_scores(self, results: List[TestResult]) -> Dict[str, float]:
        """Calculate average scores by category."""
        category_results = {}

        for result in results:
            if result.success:
                # Extract category from test_id (simplified)
                category = result.test_id.split('_')[0]
                if category not in category_results:
                    category_results[category] = []
                category_results[category].append(result.overall_quality)

        # Calculate averages
        category_scores = {}
        for category, scores in category_results.items():
            category_scores[category] = statistics.mean(scores) if scores else 0

        return category_scores

    def _generate_recommendations(self, results: List[TestResult],
                                 avg_quality: float, success_rate: float) -> List[str]:
        """Generate recommendations based on benchmark results."""
        recommendations = []

        if success_rate < 0.8:
            recommendations.append("Success rate is below 80%. Consider reviewing prompt quality and task clarity.")

        if avg_quality < 0.7:
            recommendations.append("Average quality score is below 0.7. Focus on improving response quality criteria.")

        # Analyze failure patterns
        failed_tests = [r for r in results if not r.success]
        if failed_tests:
            error_types = {}
            for result in failed_tests:
                if result.error:
                    error_type = result.error.split(':')[0] if ':' in result.error else "Unknown"
                    error_types[error_type] = error_types.get(error_type, 0) + 1

            if error_types:
                most_common_error = max(error_types.items(), key=lambda x: x[1])
                recommendations.append(f"Most common error: {most_common_error[0]}. Address this issue for better results.")

        # Performance recommendations
        slow_responses = [r for r in results if r.response_time > 5000]  # > 5 seconds
        if slow_responses:
            recommendations.append(f"{len(slow_responses)} responses were slow (>5s). Consider optimizing response time.")

        # Quality-specific recommendations
        low_quality_responses = [r for r in results if r.overall_quality < 0.5]
        if low_quality_responses:
            recommendations.append("Several responses had low quality scores. Review evaluation criteria and expected patterns.")

        if not recommendations:
            recommendations.append("Performance looks good! Continue with current approach.")

        return recommendations

    def compare_models(self, model_results: Dict[str, BenchmarkResult]) -> Dict[str, Any]:
        """Compare performance across multiple models."""
        if len(model_results) < 2:
            return {"error": "Need at least 2 models to compare"}

        comparison = {
            "models": list(model_results.keys()),
            "best_overall": None,
            "best_quality": None,
            "best_speed": None,
            "detailed_comparison": {}
        }

        # Find best performers
        best_overall_score = 0
        best_quality_score = 0
        best_speed_score = float('inf')

        for model_name, results in model_results.items():
            overall_score = results.quality_score * 0.7 + results.success_rate * 0.3

            comparison["detailed_comparison"][model_name] = {
                "overall_score": overall_score,
                "quality_score": results.quality_score,
                "success_rate": results.success_rate,
                "avg_response_time": results.avg_response_time,
                "total_tests": results.total_tests
            }

            if overall_score > best_overall_score:
                best_overall_score = overall_score
                comparison["best_overall"] = model_name

            if results.quality_score > best_quality_score:
                best_quality_score = results.quality_score
                comparison["best_quality"] = model_name

            if results.avg_response_time < best_speed_score:
                best_speed_score = results.avg_response_time
                comparison["best_speed"] = model_name

        return comparison

    def get_performance_trends(self) -> Dict[str, List[float]]:
        """Get performance trends over time."""
        if len(self.results_history) < 2:
            return {"error": "Need at least 2 benchmark runs for trends"}

        trends = {
            "quality_scores": [r.quality_score for r in self.results_history],
            "success_rates": [r.success_rate for r in self.results_history],
            "response_times": [r.avg_response_time for r in self.results_history],
            "timestamps": [r.timestamp.isoformat() for r in self.results_history]
        }

        return trends

    def export_results(self, format: str = "json") -> str:
        """Export benchmark results."""
        if format.lower() == "json":
            export_data = {
                "config": asdict(self.config),
                "results_history": [asdict(r) for r in self.results_history],
                "export_timestamp": datetime.now().isoformat()
            }
            return json.dumps(export_data, indent=2, default=str)

        elif format.lower() == "csv":
            # Simple CSV export
            lines = ["timestamp,quality_score,success_rate,avg_response_time"]

            for result in self.results_history:
                line = f"{result.timestamp},{result.quality_score},{result.success_rate},{result.avg_response_time}"
                lines.append(line)

            return "\n".join(lines)

        else:
            return f"Unsupported export format: {format}"

    def run_targeted_benchmark(self, target_task: str) -> BenchmarkResult:
        """Run benchmark targeted at a specific type of task."""
        # Create a custom test case for the target task
        custom_test = TestCase(
            id="targeted_test",
            category=TestCategory.CUSTOM,
            task=target_task,
            expected_patterns=["solution", "implementation", "example"],
            evaluation_criteria={
                "correctness": 0.4,
                "completeness": 0.3,
                "clarity": 0.3
            },
            difficulty="medium"
        )

        return self._run_benchmark([custom_test], iterations=3)


def main():
    """Example usage and testing."""
    print("=== Qwen Benchmark Example ===\n")

    # Initialize benchmark
    benchmark = QwenBenchmark()

    # Run basic test
    print("Running basic benchmark...")
    basic_results = benchmark.run_basic_test()

    print(f"Basic Test Results:")
    print(f"Success Rate: {basic_results.success_rate:.1%}")
    print(f"Average Quality: {basic_results.quality_score".3f"}")
    print(f"Average Response Time: {basic_results.avg_response_time".0f"}ms")
    print(f"Total Tests: {basic_results.total_tests}")
    print()

    # Run coding-specific benchmark
    print("Running coding benchmark...")
    coding_results = benchmark.run_coding_benchmark([
        "Create a Python decorator for caching function results",
        "Implement a priority queue using a heap"
    ])

    print(f"Coding Test Results:")
    print(f"Success Rate: {coding_results.success_rate".1%"}")
    print(f"Average Quality: {coding_results.quality_score".3f"}")
    print()

    # Show recommendations
    print("Recommendations:")
    for rec in basic_results.recommendations:
        print(f"- {rec}")
    print()

    # Export results
    print("Exporting results...")
    json_results = benchmark.export_results("json")
    print(f"Results exported as JSON ({len(json_results)} characters)")


if __name__ == "__main__":
    main()