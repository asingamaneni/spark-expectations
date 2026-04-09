# Microsoft Teams Notifications

Spark Expectations supports sending notifications to Microsoft Teams channels via incoming webhooks when data quality checks are performed. This allows teams to monitor data quality results directly in their Teams channels.

By default, Teams notifications are disabled. To enable them, configure the required parameters and set up a Teams webhook URL.

## Prerequisites

### Teams Webhook URL

1. In Microsoft Teams, navigate to the channel where you want to receive notifications
2. Click the channel name, then select **Connectors** (or **Manage channel** > **Connectors**)
3. Find **Incoming Webhook** and click **Configure**
4. Provide a name and optional icon for the webhook
5. Click **Create** and copy the generated webhook URL:
   ```
   https://outlook.office.com/webhook/XXXXXXXX/IncomingWebhook/YYYYYYYY/ZZZZZZZZ
   ```

!!! important "Security"
    Store webhook URLs securely using environment variables or a secrets manager. Never commit them to source control.

## Notification Config Parameters

### Required Parameters

!!! info "user_config.se_notifications_enable_teams"
    Master toggle to enable Teams notifications. Set to `True` to activate Teams notifications.

!!! info "user_config.se_notifications_teams_webhook_url"
    The Teams incoming webhook URL obtained from your Teams channel configuration. This is where notifications will be sent.

### Notification Triggers

These parameters control **when** Teams notifications are sent during Spark-Expectations runs:

- <abbr title="Enable notifications when job starts">user_config.se_notifications_on_start</abbr>
- <abbr title="Enable notifications when job ends">user_config.se_notifications_on_completion</abbr>
- <abbr title="Enable notifications on failure">user_config.se_notifications_on_fail</abbr>
- <abbr title="Notify if error drop threshold is breached">user_config.se_notifications_on_error_drop_exceeds_threshold_breach</abbr>
- <abbr title="Notify if rules with action 'ignore' fail">user_config.se_notifications_on_rules_action_if_failed_set_ignore</abbr>
- <abbr title="Threshold value for error drop notifications">user_config.se_notifications_on_error_drop_threshold</abbr>

## Configuration Example

Here is how to configure Teams notifications in your Spark Expectations setup:

```python
from spark_expectations.config.user_config import Constants as user_config

user_conf_dict = {
    # Enable Teams notifications
    user_config.se_notifications_enable_teams: True,

    # Teams webhook URL (replace with your actual webhook URL)
    user_config.se_notifications_teams_webhook_url: "https://outlook.office.com/webhook/...",

    # Configure when to send notifications
    user_config.se_notifications_on_start: True,
    user_config.se_notifications_on_completion: True,
    user_config.se_notifications_on_fail: True,
    user_config.se_notifications_on_error_drop_exceeds_threshold_breach: True,
    user_config.se_notifications_on_error_drop_threshold: 15,
}
```

## Message Format

Teams notifications sent by Spark Expectations include:

- **Title**: "SE Notification" header identifying the source
- **Job Status**: Whether the data quality check started, completed, or failed
- **Data Quality Results**: Summary of passed and failed expectations
- **Error Details**: Information about specific data quality issues
- **Metadata**: Table name, environment, timestamp, and other contextual information

Messages are formatted as Teams Connector Cards with a green theme color for easy visibility in the channel.

### Testing Teams Integration

You can test your Teams webhook configuration using curl:

```bash
curl -X POST -H "Content-Type: application/json" \
  --data '{"title":"Test","text":"Test message from Spark Expectations"}' \
  YOUR_WEBHOOK_URL
```
