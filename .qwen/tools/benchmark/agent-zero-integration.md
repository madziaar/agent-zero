# Agent Zero Integration Guide - Qwen Benchmark Tools

This guide explains how to integrate the Qwen Benchmark Tools into your Agent Zero workflow for continuous performance monitoring and quality assessment of Qwen model effectiveness.

## Overview

The Qwen Benchmark Tools provide comprehensive performance benchmarking and quality assessment capabilities specifically designed for measuring Qwen's effectiveness across various coding tasks. Integration with Agent Zero enables continuous monitoring, performance tracking, and data-driven optimization of your Qwen interactions.

## Quick Integration

### Basic Setup

```python
# In your Agent Zero configuration or initialization
from benchmark import QwenBenchmark, BenchmarkConfig

class QwenPerformanceAgent:
    def __init__(self):
        # Configure benchmark suite
        config = BenchmarkConfig(
            test_categories=['coding', 'debugging'],
            iterations=3,
            quality_threshold=0.7
        )
        self.benchmark = QwenBenchmark(config)

    def process_with_monitoring(self, user_request: str) -> dict:
        """Process request with performance monitoring."""
        # Run targeted benchmark for this type of request
        benchmark_result = self.benchmark.run_targeted_benchmark(user_request)

        # Process the request
        start_time = time.time()
        response = self.process_with_qwen(user_request)
        response_time = (time.time() - start_time) * 1000

        # Log performance metrics
        self.log_performance_metrics({
            "request_type": "user_request",
            "benchmark_score": benchmark_result.quality_score,
            "response_time": response_time,
            "success": benchmark_result.success_rate > 0.8
        })

        return {
            "response": response,
            "performance_metrics": benchmark_result,
            "response_time": response_time
        }
```

### Advanced Integration

```python
from benchmark import QwenBenchmark, BenchmarkConfig, TestCategory
from typing import Dict, List, Any
import time
from datetime import datetime

class AdvancedPerformanceAgent:
    def __init__(self):
        # Advanced configuration for comprehensive monitoring
        config = BenchmarkConfig(
            test_categories=['coding', 'debugging', 'optimization', 'analysis'],
            iterations=5,
            timeout=45,
            quality_threshold=0.8,
            include_detailed_metrics=True,
            performance_targets={
                "max_response_time": 5000,
                "min_quality_score": 0.8,
                "min_success_rate": 0.9
            }
        )
        self.benchmark = QwenBenchmark(config)
        self.performance_history = []
        self.alert_thresholds = {
            "quality_degradation": 0.1,  # 10% drop
            "response_time_spike": 2.0,   # 2x increase
            "success_rate_drop": 0.15    # 15% drop
        }

    def continuous_monitoring(self):
        """Run continuous performance monitoring."""
        while True:
            try:
                # Run comprehensive benchmark
                results = self.benchmark.run_comprehensive_benchmark()

                # Store results
                self.performance_history.append({
                    "timestamp": datetime.now(),
                    "results": results
                })

                # Check for performance issues
                self._check_performance_alerts(results)

                # Generate performance report
                if len(self.performance_history) % 10 == 0:  # Every 10 runs
                    self._generate_performance_report()

                # Wait before next monitoring cycle
                time.sleep(1800)  # 30 minutes

            except Exception as e:
                logger.error(f"Error in monitoring cycle: {e}")
                time.sleep(300)  # Wait 5 minutes before retry

    def _check_performance_alerts(self, current_results: BenchmarkResult):
        """Check if performance metrics trigger alerts."""
        if len(self.performance_history) < 2:
            return

        # Get recent performance for comparison
        recent_results = [r["results"] for r in self.performance_history[-5:]]
        baseline_quality = statistics.mean([r.quality_score for r in recent_results[:-1]])
        baseline_response_time = statistics.mean([r.avg_response_time for r in recent_results[:-1]])
        baseline_success_rate = statistics.mean([r.success_rate for r in recent_results[:-1]])

        # Check for quality degradation
        quality_drop = baseline_quality - current_results.quality_score
        if quality_drop > self.alert_thresholds["quality_degradation"]:
            self._trigger_alert("quality_degradation", {
                "current_score": current_results.quality_score,
                "baseline_score": baseline_quality,
                "drop_amount": quality_drop
            })

        # Check for response time spikes
        if current_results.avg_response_time > baseline_response_time * self.alert_thresholds["response_time_spike"]:
            self._trigger_alert("response_time_spike", {
                "current_time": current_results.avg_response_time,
                "baseline_time": baseline_response_time,
                "spike_factor": current_results.avg_response_time / baseline_response_time
            })

        # Check for success rate drops
        success_rate_drop = baseline_success_rate - current_results.success_rate
        if success_rate_drop > self.alert_thresholds["success_rate_drop"]:
            self._trigger_alert("success_rate_drop", {
                "current_rate": current_results.success_rate,
                "baseline_rate": baseline_success_rate,
                "drop_amount": success_rate_drop
            })

    def _trigger_alert(self, alert_type: str, metrics: Dict[str, Any]):
        """Trigger performance alert."""
        alert = {
            "type": alert_type,
            "timestamp": datetime.now(),
            "severity": "high" if metrics.get("drop_amount", 0) > 0.2 else "medium",
            "metrics": metrics,
            "recommendations": self._get_alert_recommendations(alert_type, metrics)
        }

        logger.warning(f"Performance Alert: {alert_type} - {alert}")
        # Here you could send notifications, emails, etc.

    def _get_alert_recommendations(self, alert_type: str, metrics: Dict[str, Any]) -> List[str]:
        """Get recommendations for performance alerts."""
        recommendations = []

        if alert_type == "quality_degradation":
            recommendations.extend([
                "Review recent prompt optimizations",
                "Check for changes in Qwen model version",
                "Verify system resource availability",
                "Run diagnostic tests on problematic categories"
            ])

        elif alert_type == "response_time_spike":
            recommendations.extend([
                "Check system resource usage",
                "Review for memory leaks",
                "Consider prompt optimization for efficiency",
                "Check network connectivity and API status"
            ])

        elif alert_type == "success_rate_drop":
            recommendations.extend([
                "Review prompt quality and clarity",
                "Check for API rate limiting",
                "Verify authentication and permissions",
                "Run tests with simpler prompts"
            ])

        return recommendations
```

## Integration Patterns

### Pattern 1: Request-Level Monitoring

```python
class RequestMonitoringAgent:
    def __init__(self):
        self.benchmark = QwenBenchmark()

    def process_request_with_benchmark(self, request: str) -> Dict[str, Any]:
        """Process request with detailed benchmarking."""
        # Pre-processing benchmark
        pre_benchmark = self.benchmark.run_targeted_benchmark(f"Similar to: {request}")

        # Process request
        start_time = time.time()
        response = self.call_qwen_model(request)
        processing_time = (time.time() - start_time) * 1000

        # Post-processing analysis
        post_benchmark = self.benchmark.run_targeted_benchmark(f"Similar to: {request}")

        # Calculate performance impact
        performance_impact = self._calculate_impact(pre_benchmark, post_benchmark)

        return {
            "response": response,
            "processing_time": processing_time,
            "pre_benchmark": pre_benchmark,
            "post_benchmark": post_benchmark,
            "performance_impact": performance_impact,
            "quality_assessment": self._assess_response_quality(response, request)
        }

    def _calculate_impact(self, pre: BenchmarkResult, post: BenchmarkResult) -> Dict[str, float]:
        """Calculate performance impact of processing."""
        return {
            "quality_impact": post.quality_score - pre.quality_score,
            "response_time_impact": post.avg_response_time - pre.avg_response_time,
            "success_rate_impact": post.success_rate - pre.success_rate
        }
```

### Pattern 2: Scheduled Benchmarking

```python
class ScheduledBenchmarkAgent:
    def __init__(self):
        config = BenchmarkConfig(
            test_categories=['coding', 'debugging', 'optimization'],
            iterations=10
        )
        self.benchmark = QwenBenchmark(config)

    def run_scheduled_benchmarks(self):
        """Run benchmarks on a schedule."""
        schedule = {
            "daily": "run_basic_test",
            "weekly": "run_comprehensive_benchmark",
            "monthly": "run_custom_benchmark"
        }

        for period, method_name in schedule.items():
            try:
                # Run scheduled benchmark
                method = getattr(self.benchmark, method_name)
                results = method()

                # Store results with period tag
                self.store_benchmark_results(results, period)

                # Generate period-specific insights
                insights = self.generate_period_insights(results, period)

                logger.info(f"{period.title()} benchmark completed: {results.success_rate:.1%} success rate")

            except Exception as e:
                logger.error(f"Error in {period} benchmark: {e}")

    def store_benchmark_results(self, results: BenchmarkResult, period: str):
        """Store benchmark results for historical analysis."""
        result_data = {
            "period": period,
            "timestamp": results.timestamp,
            "results": results
        }

        # Here you could save to database, file, etc.
        with open(f"benchmark_results_{period}.json", "a") as f:
            json.dump(result_data, f, indent=2, default=str)
            f.write("\n")
```

### Pattern 3: Adaptive Performance Optimization

```python
class AdaptivePerformanceAgent:
    def __init__(self):
        self.benchmark = QwenBenchmark()
        self.performance_baseline = None
        self.optimization_strategies = {
            "low_quality": "enhance_prompts",
            "slow_responses": "optimize_requests",
            "high_error_rate": "simplify_tasks"
        }

    def adapt_to_performance(self, current_performance: BenchmarkResult) -> List[str]:
        """Adapt behavior based on current performance."""
        if self.performance_baseline is None:
            self.performance_baseline = current_performance
            return ["Established performance baseline"]

        # Detect performance changes
        quality_change = current_performance.quality_score - self.performance_baseline.quality_score
        speed_change = current_performance.avg_response_time - self.performance_baseline.avg_response_time
        success_change = current_performance.success_rate - self.performance_baseline.success_rate

        adaptations = []

        # Quality-based adaptations
        if quality_change < -0.1:
            adaptations.extend(self._apply_quality_optimization())
        elif quality_change > 0.1:
            adaptations.append("Performance improved - maintaining current approach")

        # Speed-based adaptations
        if speed_change > 1000:  # 1 second slower
            adaptations.extend(self._apply_speed_optimization())

        # Success rate adaptations
        if success_change < -0.1:
            adaptations.extend(self._apply_success_rate_optimization())

        return adaptations

    def _apply_quality_optimization(self) -> List[str]:
        """Apply optimizations for quality issues."""
        return [
            "Switching to optimized prompt templates",
            "Increasing context in requests",
            "Adding explicit instructions for clarity",
            "Using prompt optimizer for request enhancement"
        ]

    def _apply_speed_optimization(self) -> List[str]:
        """Apply optimizations for speed issues."""
        return [
            "Simplifying request structure",
            "Reducing context length",
            "Using more specific, focused prompts",
            "Caching frequent request patterns"
        ]

    def _apply_success_rate_optimization(self) -> List[str]:
        """Apply optimizations for success rate issues."""
        return [
            "Improving prompt clarity",
            "Adding more specific examples",
            "Breaking complex requests into simpler steps",
            "Using more structured request formats"
        ]
```

## Configuration for Agent Zero

### Basic Configuration

```json
{
  "qwen_tools": {
    "benchmark": {
      "enabled": true,
      "run_frequency": "daily",
      "test_categories": ["coding", "debugging"],
      "alert_on_degradation": true,
      "store_results": true
    }
  }
}
```

### Advanced Configuration

```json
{
  "qwen_tools": {
    "benchmark": {
      "enabled": true,
      "monitoring_mode": "continuous",
      "test_categories": ["coding", "debugging", "optimization", "analysis"],
      "iterations": 5,
      "quality_threshold": 0.8,
      "include_detailed_metrics": true,
      "performance_targets": {
        "max_response_time": 5000,
        "min_quality_score": 0.8,
        "min_success_rate": 0.9
      },
      "alert_thresholds": {
        "quality_degradation": 0.1,
        "response_time_spike": 2.0,
        "success_rate_drop": 0.15
      },
      "storage": {
        "results_file": "benchmark_results.json",
        "history_limit": 100,
        "export_format": "json"
      },
      "notifications": {
        "enable_alerts": true,
        "alert_channels": ["log", "email"],
        "degradation_threshold": 0.1
      }
    }
  }
}
```

## Usage Examples

### Example 1: Continuous Monitoring Setup

```python
# Set up continuous monitoring
monitoring_agent = AdvancedPerformanceAgent()

# Start monitoring in background thread
import threading
monitoring_thread = threading.Thread(target=monitoring_agent.continuous_monitoring)
monitoring_thread.daemon = True
monitoring_thread.start()

# Continue with normal operations
print("Performance monitoring started in background")
```

### Example 2: Performance Impact Assessment

```python
# Assess performance impact of changes
agent = RequestMonitoringAgent()

# Test before and after changes
baseline_results = agent.benchmark.run_comprehensive_benchmark()

# Make your changes (e.g., prompt optimization, model updates)

# Test after changes
post_change_results = agent.benchmark.run_comprehensive_benchmark()

# Analyze impact
impact = agent.analyze_performance_impact(baseline_results, post_change_results)
print(f"Quality Impact: {impact['quality_change']:+.3f}")
print(f"Speed Impact: {impact['speed_change']:+.0f}ms")
print(f"Success Rate Impact: {impact['success_rate_change']:+.1%}")
```

### Example 3: Custom Benchmarking Scenarios

```python
# Create custom benchmarks for specific use cases
custom_scenarios = [
    "Create a REST API with authentication",
    "Debug a complex inheritance issue",
    "Optimize a database query function",
    "Review code for security vulnerabilities"
]

# Run custom benchmark
custom_results = agent.benchmark.run_custom_benchmark([
    TestCase(
        id=f"custom_{i}",
        category=TestCategory.CUSTOM,
        task=task,
        expected_patterns=["implementation", "solution", "example"],
        evaluation_criteria={
            "correctness": 0.3,
            "completeness": 0.3,
            "best_practices": 0.4
        },
        difficulty="medium"
    ) for i, task in enumerate(custom_scenarios)
])

print(f"Custom Benchmark Results: {custom_results.success_rate:.1%} success rate")
```

## Best Practices

### 1. Regular Monitoring

```python
def setup_regular_monitoring():
    """Set up regular performance monitoring."""
    monitoring_config = BenchmarkConfig(
        test_categories=['coding', 'debugging'],
        iterations=3  # Quick checks
    )

    # Schedule different types of benchmarks
    schedules = {
        "quick_check": {"interval": 3600, "method": "run_basic_test"},  # Every hour
        "comprehensive": {"interval": 86400, "method": "run_comprehensive_benchmark"},  # Daily
        "coding_focused": {"interval": 43200, "method": "run_coding_benchmark"}  # Twice daily
    }

    for check_name, schedule in schedules.items():
        # Set up scheduled execution
        pass  # Implementation would use scheduling library
```

### 2. Performance-Based Adaptation

```python
def adapt_based_on_performance(current_performance: BenchmarkResult):
    """Adapt agent behavior based on performance metrics."""
    adaptations = []

    # Quality-based adaptations
    if current_performance.quality_score < 0.7:
        adaptations.extend([
            "Using prompt optimizer for all requests",
            "Adding more context to requests",
            "Breaking complex requests into simpler steps"
        ])

    # Speed-based adaptations
    if current_performance.avg_response_time > 5000:
        adaptations.extend([
            "Simplifying request structure",
            "Reducing context length",
            "Caching frequent request patterns"
        ])

    return adaptations
```

### 3. Historical Analysis

```python
def analyze_performance_trends():
    """Analyze performance trends over time."""
    if len(agent.performance_history) < 7:
        return "Need more data for trend analysis"

    # Extract trends
    quality_trend = [r["results"].quality_score for r in agent.performance_history[-7:]]
    speed_trend = [r["results"].avg_response_time for r in agent.performance_history[-7:]]

    # Calculate trend direction
    quality_trend_direction = "improving" if quality_trend[-1] > quality_trend[0] else "degrading"
    speed_trend_direction = "faster" if speed_trend[-1] < speed_trend[0] else "slower"

    return {
        "quality_trend": quality_trend_direction,
        "speed_trend": speed_trend_direction,
        "recommendations": generate_trend_recommendations(quality_trend, speed_trend)
    }
```

## Performance Considerations

- **Efficient Benchmarking**: Use appropriate iteration counts and timeouts
- **Resource Management**: Monitor system resources during benchmarking
- **Background Processing**: Run benchmarks in background to avoid blocking
- **Data Management**: Implement proper storage and cleanup of benchmark data

## Troubleshooting

### Common Issues

1. **Inconsistent Results**: Increase iterations for more stable measurements
2. **Resource Conflicts**: Run benchmarks during low-usage periods
3. **Network Issues**: Monitor API connectivity and handle timeouts gracefully
4. **Data Storage**: Implement proper data rotation for historical results

### Debugging

```python
def debug_benchmark_issue():
    """Debug benchmark issues."""
    # Test with minimal configuration
    debug_config = BenchmarkConfig(
        test_categories=['coding'],
        iterations=1,
        timeout=10
    )

    debug_benchmark = QwenBenchmark(debug_config)

    try:
        # Run single test
        result = debug_benchmark.run_basic_test()

        return {
            "success": True,
            "results": result,
            "debug_info": "Basic functionality working"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "debug_info": "Check Qwen API connectivity and configuration"
        }
```

## Contributing

When extending the integration:

1. Follow existing configuration patterns
2. Maintain performance characteristics
3. Add appropriate error handling and logging
4. Include comprehensive testing
5. Document new integration patterns

This integration provides a solid foundation for continuous performance monitoring and optimization of Qwen interactions in Agent Zero, enabling data-driven improvements and proactive issue detection.