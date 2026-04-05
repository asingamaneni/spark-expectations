# PySpark Compatibility

This page documents PySpark version compatibility and known considerations when using Spark-Expectations with different PySpark releases.

## Supported Versions

| Component | Supported Versions | Notes |
|---|---|---|
| PySpark | 3.0.0 - 4.0.0 | Optional dependency via `pip install spark-expectations[pyspark]` |
| Python | 3.9 - 3.13 | CI tests run on 3.10, 3.11, 3.12 |
| Java | 17 | Temurin distribution recommended |
| Scala | 2.12, 2.13 | PySpark 4.0 defaults to Scala 2.13 |

## PySpark 4.0 Considerations

PySpark 4.0 introduced several changes that may affect how you write data quality rules.

### ANSI Mode Enabled by Default

PySpark 4.0 enables ANSI mode (`spark.sql.ansi.enabled=true`) by default. This means implicit type casts that previously succeeded silently may now raise errors. When writing DQ rules, use explicit casts:

```sql
-- Instead of relying on implicit cast:
-- sum(string_column) > 100

-- Use explicit casting:
CAST(sum(CAST(string_column AS DOUBLE)) AS DOUBLE) > 100
```

### Wildcard Import Changes

PySpark 4.0 removed `DataFrame`, `Column`, and type classes from `pyspark.sql.functions` wildcard imports. If you have custom UDFs or extensions that use wildcard imports, update them:

```python
# Before (PySpark 3.x)
from pyspark.sql.functions import *  # DataFrame, Column included

# After (PySpark 4.0+)
from pyspark.sql.functions import col, expr, when, lit
from pyspark.sql import DataFrame, Column
from pyspark.sql.types import StructType, StringType
```

### Delta Lake Compatibility

PySpark 4.0 uses Delta Lake 4.0. The `delta-spark` package artifact changed from `delta-spark_2.12` to `delta-spark_2.13` for Scala 2.13 builds. Spark-Expectations handles this internally.

## PySpark 3.x Support

Spark-Expectations maintains backward compatibility with PySpark 3.0+. Most features work identically across the 3.x and 4.0 release lines.

### Kafka Client Compatibility

When running integration tests locally, ensure your Kafka client version is compatible with your PySpark version. PySpark 4.0.0 ships with Kafka client jars compatible with Kafka 3.0+. PySpark 4.0.1+ upgraded to Kafka 3.9.1 client jars.

## Version Constraint Details

The PySpark dependency is declared as optional in `pyproject.toml`:

```toml
[project.optional-dependencies]
pyspark = ["pyspark[connect]>=3.0.0,<=4.0.0"]
```

The upper bound of `<=4.0.0` ensures compatibility with the Kafka 3.0.0 jars used in CI testing. This constraint will be widened as the CI infrastructure is updated.
