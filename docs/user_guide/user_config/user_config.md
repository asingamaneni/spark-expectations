# User Configuration Reference

The `user_config` dictionary controls the behavior of spark-expectations at runtime. You pass it when
creating a `SparkExpectations` instance and when decorating your processing function with `@se.with_expectations`.

All configuration keys are defined as constants on `spark_expectations.config.user_config.Constants` (imported
as `user_config` in the examples below).

```python
from spark_expectations.config.user_config import Constants as user_config
```

## Core Settings

These settings control the fundamental behavior of the data quality engine.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `user_config.se_dq_rules_params` | `dict` | — | Parameters passed into rule SQL expressions (e.g. `{"env": "prod", "table": "orders"}`) |
| `user_config.se_enable_error_table` | `bool` | `False` | Write rows that fail row-level DQ checks to a separate error table |
| `user_config.is_serverless` | `bool` | `False` | Enable adaptations for Databricks Serverless Compute |
| `user_config.se_job_metadata` | `str` | `None` | Arbitrary JSON metadata attached to every stats record for this job |

## Notification Settings

### Global Triggers

These flags determine which lifecycle events fire notifications across all enabled channels.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `user_config.se_notifications_on_start` | `bool` | `False` | Notify when the DQ run starts |
| `user_config.se_notifications_on_completion` | `bool` | `False` | Notify when the DQ run completes |
| `user_config.se_notifications_on_fail` | `bool` | `False` | Notify when the DQ run fails |
| `user_config.se_notifications_on_error_drop_exceeds_threshold_breach` | `bool` | `False` | Notify when the error-drop percentage exceeds the threshold |
| `user_config.se_notifications_on_error_drop_threshold` | `int` | `0` | Error-drop percentage threshold for breach notification |

### Email

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `user_config.se_notifications_enable_email` | `bool` | `False` | Enable email notifications |
| `user_config.se_notifications_email_smtp_host` | `str` | — | SMTP server hostname |
| `user_config.se_notifications_email_smtp_port` | `int` | — | SMTP server port (typically 587) |
| `user_config.se_notifications_email_from` | `str` | — | Sender address |
| `user_config.se_notifications_email_to_other_mail_id` | `str` | — | Comma-separated recipient addresses |
| `user_config.se_notifications_email_subject` | `str` | — | Email subject line |
| `user_config.se_notifications_enable_smtp_server_auth` | `bool` | `False` | Authenticate with SMTP credentials |
| `user_config.se_notifications_smtp_user_name` | `str` | `None` | SMTP login user (falls back to `email_from` if unset) |
| `user_config.se_notifications_smtp_password` | `str` | `None` | SMTP password (plaintext; prefer secret backends) |
| `user_config.se_notifications_smtp_creds_dict` | `dict` | `None` | Secret-backend credentials dictionary for SMTP password retrieval |

### Slack

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `user_config.se_notifications_enable_slack` | `bool` | `False` | Enable Slack notifications |
| `user_config.se_notifications_slack_webhook_url` | `str` | — | Slack incoming-webhook URL |

### Microsoft Teams

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `user_config.se_notifications_enable_teams` | `bool` | `False` | Enable Teams notifications |
| `user_config.se_notifications_teams_webhook_url` | `str` | — | Teams incoming-webhook URL |

### Zoom

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `user_config.se_notifications_enable_zoom` | `bool` | `False` | Enable Zoom chat notifications |
| `user_config.se_notifications_zoom_webhook_url` | `str` | — | Zoom webhook URL |
| `user_config.se_notifications_zoom_token` | `str` | — | Zoom verification token |

### PagerDuty

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `user_config.se_notifications_enable_pagerduty` | `bool` | `False` | Enable PagerDuty incident creation |
| `user_config.se_notifications_pagerduty_integration_key` | `str` | — | Events API v2 routing/integration key |
| `user_config.se_notifications_pagerduty_webhook_url` | `str` | — | PagerDuty webhook URL |

## Streaming / Kafka Settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `user_config.se_enable_streaming` | `bool` | `False` | Publish DQ statistics to a Kafka topic |
| `user_config.se_streaming_stats_topic_name` | `str` | — | Kafka topic for stats events |
| `user_config.se_streaming_stats_kafka_bootstrap_server` | `str` | — | Kafka bootstrap servers |

## Detailed Statistics Settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `user_config.se_enable_agg_dq_detailed_result` | `bool` | `False` | Write per-rule results to the detailed stats table |
| `user_config.se_enable_query_dq_detailed_result` | `bool` | `False` | Write query-DQ output to the query-DQ output table |
| `user_config.querydq_output_custom_table_name` | `str` | `None` | Override the default query-DQ output table name |

## Minimal Example

```python
from spark_expectations.config.user_config import Constants as user_config

user_conf = {
    user_config.se_enable_error_table: True,
    user_config.se_notifications_enable_slack: True,
    user_config.se_notifications_slack_webhook_url: "https://hooks.slack.com/services/...",
    user_config.se_notifications_on_fail: True,
    user_config.se_dq_rules_params: {"env": "prod", "table": "orders"},
}
```

For a complete working example see the [examples page](../../../examples/#configurations).
