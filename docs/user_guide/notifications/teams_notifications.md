# Microsoft Teams Notifications

Spark Expectations supports sending notifications to Microsoft Teams channels via webhooks when data quality checks are performed. This enables teams using Microsoft Teams as their primary communication platform to stay informed about data quality issues in real-time.

By default, Teams notifications are disabled. To enable them, you need to configure the required parameters and set up a Teams incoming webhook URL.

## Prerequisites

Before configuring Teams notifications, you need:

### Teams Incoming Webhook URL

1. In Microsoft Teams, go to the channel where you want to receive notifications
2. Click the **...** (more options) menu and select **Connectors** (or **Workflows** in newer Teams versions)
3. Search for **Incoming Webhook** and click **Configure**
4. Provide a name (e.g., "Spark Expectations DQ Alerts") and optionally upload an icon
5. Click **Create** and copy the generated webhook URL

!!! important "Security"
    Store webhook URLs securely using environment variables or a secrets manager. Never commit them directly to your codebase.

## Notification Config Parameters

### Required Parameters

!!! info "user_config.se_notifications_enable_teams"
    Master toggle to enable Teams notifications. Set to `True` to activate Teams notifications.

!!! info "user_config.se_notifications_teams_webhook_url"
    The Teams incoming webhook URL where notifications will be sent.

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

notification_config = {
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

Teams notifications use a **MessageCard** format with:

- **Title**: "SE Notification"
- **Theme Color**: Green (`#008000`) header accent
- **Text**: The full notification message body with appropriate formatting

The notification text includes line break formatting optimized for Teams rendering, with double newlines for paragraph separation and indentation cleanup for readability.

## Testing Teams Integration

You can test your Teams webhook configuration using curl:

```bash
curl -H "Content-Type: application/json" -d '{
    "title": "Test Notification",
    "themeColor": "008000",
    "text": "Test message from Spark Expectations"
}' YOUR_WEBHOOK_URL
```

A successful request returns HTTP status 200.
