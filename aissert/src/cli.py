"""CLI tool for running AI metrics checks."""

import sys

import click
from aissert.src.metrics.base import some_metric


@click.command()
@click.argument("metric")
@click.argument("input")
@click.argument("output")
@click.option("-t", "--threshold", type=float, default=0.5, show_default=True)
def check_metric(metric: str, input: str, output: str, threshold: float) -> None:
    """Execute a certain metric."""
    metric_value = some_metric("", "")
    if metric_value < threshold:
        # TODO: log instead of print?
        print(f"ERROR: Metric {metric}={metric_value} below threshold {threshold}", file=sys.stderr)
        sys.exit(1)
    else:
        print(metric)


if __name__ == "__main__":
    check_metric()
