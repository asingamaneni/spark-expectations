### Effortlessly Explore Spark Expectations on Example Dataset with Automated Setup in Databricks

This section provides instructions on how to set up a sample notebook in the Databricks environment to investigate, comprehend, and conduct a feasibility study on the Spark Expectations framework.

#### Prerequisite:

1. Recommended Databricks runtime environment for better experience - DBR 11.0 and above
2. Please install the Kafka jar using the path `dbfs:/kafka-jars/databricks-shaded-strimzi-kafka-oauth-client-1.1.jar`. If the jar is not available in the dbfs location, please raise a ticket with your Platform team to add the jar to your workspace
3. Please follow the [Databricks Git integration guide](https://docs.databricks.com/en/repos/index.html) to integrate and clone this repo from Git into Databricks Repos
4. Please follow the [Microsoft Teams Incoming Webhook guide](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) or [Slack Incoming Webhook guide](https://api.slack.com/messaging/webhooks) to create the webhook URL for your team-specific channel

#### Installing spark-expectations:

You can install spark-expectations directly in your Databricks notebook:

```python
%pip install spark-expectations
```

Or add it to your cluster's library configuration via the Databricks UI under **Compute > Your Cluster > Libraries > Install New > PyPI**.

#### Quick Start:

Once the prerequisites are met, you can explore the example notebooks in the [`examples/`](https://github.com/Nike-Inc/spark-expectations/tree/main/examples) directory of the repository. These notebooks demonstrate how to configure and run data quality rules on sample datasets using Delta Lake, Iceberg, and BigQuery backends.