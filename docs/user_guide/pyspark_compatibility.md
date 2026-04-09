# PySpark Compatibility

This page documents the PySpark versions that spark-expectations supports and known compatibility considerations for each version range.

## Supported Version Matrix

| PySpark Version | Python Versions | Status | Notes |
|----------------|-----------------|--------|-------|
| 3.3.x -- 3.5.x | 3.9 -- 3.12 | Supported | Stable, widely deployed |
| 4.0.0 -- 4.0.2 | 3.10 -- 3.12 | Supported | Latest tested in CI |
| 4.1.x | 3.10 -- 3.12 | Not yet supported | Requires Kafka client upgrade in CI |
| 4.2.x (preview) | 3.10+ | Not supported | Preview release, not stable |

The current dependency constraint is `pyspark[connect]>=3.0.0,<=4.0.0`. Check the [PyPI page](https://pypi.org/project/spark-expectations/) or `pyproject.toml` for the exact constraint in your installed version.

## Version-Specific Notes

### PySpark 3.5.x (LTS)

PySpark 3.5 is the final 3.x LTS series. The latest maintenance release is 3.5.8 (January 2026). This is the most widely deployed version in production environments and has the broadest Python compatibility (3.9 through 3.12).

### PySpark 4.0.x

PySpark 4.0.0 was released in 2025 and includes several changes relevant to spark-expectations:

- Removed several deprecated pandas API on Spark aliases (e.g., `Y` to `YE`, `H` to `h`). These do not affect spark-expectations directly since the library does not use the pandas API on Spark.
- SparkR is deprecated. This does not affect spark-expectations (Python only).
- The `pyspark[connect]` extra is available for Spark Connect support.

### PySpark 4.1.x

PySpark 4.1 introduces breaking changes that currently prevent spark-expectations from supporting it:

- **Python 3.9 dropped**: The minimum Python version is now 3.10.
- **PyArrow minimum raised** from 11.0.0 to 15.0.0.
- **Pandas minimum raised** from 2.0.0 to 2.2.0.
- **Kafka client upgrade**: PySpark 4.1 bundles newer Kafka client JARs that are incompatible with Kafka 3.0.0 (used in CI). Upgrading requires updating the CI Kafka version.

### ANSI Mode

PySpark 4.x enables ANSI mode by default for certain operations. If your DQ rules use implicit type casting (e.g., comparing strings to integers), you may see `CAST_INVALID_INPUT` errors under PySpark 4.x that did not occur under 3.x. To resolve this, use explicit `CAST()` expressions in your rule expectations.

## CI Testing

spark-expectations CI runs against:

- **Python**: 3.10, 3.11, 3.12
- **Java**: 17 (Temurin)
- **Kafka**: 3.0.0

The Kafka version in CI constrains the maximum PySpark version that can be tested. PySpark 4.1+ introduces Kafka client classes (`LogKeys$TOPIC_PARTITIONS$`) that require a newer Kafka broker, causing `ClassNotFoundException` in integration tests.

## Upgrading PySpark

When upgrading PySpark in your environment, keep these points in mind:

1. **Test your DQ rules**: Rules that rely on implicit casting behavior may need `CAST()` adjustments under PySpark 4.x due to ANSI mode.
2. **Check Python version**: PySpark 4.1+ requires Python 3.10 or later.
3. **Verify Kafka compatibility**: If you use streaming statistics or Kafka-based sinks, ensure your Kafka broker version is compatible with your PySpark version.
4. **sqlglot constraint**: spark-expectations pins `sqlglot<23.0`. If your environment requires a newer sqlglot, check for API compatibility.
