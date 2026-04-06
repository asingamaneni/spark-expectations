# Getting Started with Spark-Expectations

This guide will help you set up your environment, install the library, and understand the basic requirements for using Spark-Expectations in your data workflows.

## Prerequisites

### Python

Supported versions: 3.9, 3.10, 3.11, 3.12 (recommended: latest 3.12.x)

### Java

Supported versions: 8, 11, 17 (recommended: 17)

!!! tip "Java Version"
    Java 17 (Temurin) is the recommended version and is used in the project's CI pipeline. You can download it from [Adoptium](https://adoptium.net/).

### Apache Spark

Spark-Expectations works with PySpark 3.0.0 through 4.0.x. If you are running on Databricks, the Spark environment is already available. For local development, install PySpark alongside the library.

## Installation

You can install Spark-Expectations directly from [PyPI](https://pypi.org/project/spark-expectations/):

```sh
pip install spark-expectations
```

To include PySpark as part of the installation:

```sh
pip install "spark-expectations[spark]"
```

Or add it to your dependency manager (e.g., Poetry, Hatch, uv, pip-tools).

## Verify Installation

After installation, verify that everything is set up correctly:

```python
from spark_expectations.core.expectations import SparkExpectations
print("Spark-Expectations imported successfully")
```

## What You Need to Know

Before diving into the quickstart, it helps to understand the three main concepts in Spark-Expectations:

**Rules Table** -- A table (or YAML/JSON file) that defines your data quality rules. Each rule specifies what to check, how to check it, and what to do if the check fails. See [Data Quality Rules](data_quality_rules.md) for details.

**Rule Types** -- There are three rule types: `row_dq` (per-row checks), `agg_dq` (aggregate checks like row counts), and `query_dq` (SQL query-based checks). Each type serves a different validation purpose.

**Actions** -- When a rule fails, one of three actions is taken: `ignore` (log and continue), `drop` (remove failing rows, row_dq only), or `fail` (stop the job).

## Next Steps

- [Quickstart](quickstart.md) -- Set up a minimal working example
- [File-Based Rules](file_based_rules.md) -- Define rules in YAML or JSON instead of SQL tables
- [Notifications](notifications/email_notifications.md) -- Configure alerting via Email, Slack, Teams, Zoom, or PagerDuty
