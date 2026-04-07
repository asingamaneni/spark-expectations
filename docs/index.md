# Welcome to Spark-Expectations

Taking inspiration from DLT - data quality expectations: Spark-Expectations is built, so that the data quality rules can 
run using decorator pattern while the spark job is in flight and Additionally, the framework able to perform data 
quality checks when the data is at rest.

## Features Of Spark Expectations

Please find the spark-expectations flow and feature diagrams below

<p align="center">
<img src=https://github.com/Nike-Inc/spark-expectations/blob/main/docs/se_diagrams/flow.png?raw=true width=1000></p>

<p align="center">
<img src=https://github.com/Nike-Inc/spark-expectations/blob/main/docs/se_diagrams/features.png?raw=true width=1000></p>

### Rules

Rules table holds most important building block that defines data quality expectations. Tool currently support three different types of Rules. 


Proceed to [User Guide / Data Quality Rules](user_guide/data_quality_rules/) for details how rules can be configured


### Output

Spark-Expectations creates multiple tables to store output of the job. 
Creation of those tables is managed by the library and certain tables can be toggled or are only created if certain data quality rules exist.

`Stats Table` is most important one and captures Data Quality metrics. 
Check [User Guide / Data Quality Metrics](user_guide/data_quality_metrics/) for more information about it but also other tables shown in SE diagram.


### Compatibility

Spark-Expectations supports a range of PySpark and Python versions. Below is the current compatibility matrix:

| Component | Supported Versions |
|---|---|
| Python | 3.9 - 3.13 |
| PySpark | 3.0.0 - 4.0.0 |
| Java | 17 (Temurin recommended) |
| Scala | 2.12, 2.13 |

When using PySpark 4.0, be aware that ANSI mode is enabled by default. Spark-Expectations handles type comparisons internally and is designed to work correctly under ANSI mode. If you encounter casting errors in your DQ rules, ensure your rule expressions use explicit type casts (e.g., `CAST(column AS DOUBLE)`) rather than relying on implicit conversions.

### Integrations

#### Notifications

Spark Expectation provides way to enable different behavior and thresholds for data quality run notifications. Currently supported notifications are:

- [Slack](user_guide/notifications/slack_notifications/)
- [Email](user_guide/notifications/email_notifications/)
- [PagerDuty](user_guide/notifications/pagerduty_notifications/)
