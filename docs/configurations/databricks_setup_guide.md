### Effortlessly Explore Spark Expectations on Example Dataset with Automated Setup in Databricks 

This section provides instructions on how to set up a sample notebook in the Databricks environment to investigate, comprehend, and conduct a feasibility study on the Spark Expectations framework.

#### Prerequisite:

1. Recommended Databricks run time environment for better experience - DBS 11.0 and above
2. Please install the Kafka jar using the path `dbfs:/kafka-jars/databricks-shaded-strimzi-kafka-oauth-client-1.1.jar`, If the jar is not available in the dbfs location, please raise a ticket with Platform team to add the jar to your workspace
3. Please follow the steps provided in the [Databricks Git integration guide](https://docs.databricks.com/en/repos/index.html) to integrate and clone a repo from Git in Databricks
4. Please follow the steps to create the webhook URL for your team-specific channel in the [Microsoft Teams webhook setup guide](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)