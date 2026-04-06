# Zoom Notifications

Spark Expectations supports sending notifications to Zoom channels via webhooks when data quality checks are performed. This enables teams to receive real-time updates about data quality results directly in their Zoom chat channels.

By default, Zoom notifications are disabled. To enable them, you need to configure the required parameters and set up a Zoom webhook URL and authentication token.

## Prerequisites

Before configuring Zoom notifications, you need:

### Zoom Webhook URL and Token

1. Go to the [Zoom App Marketplace](https://marketplace.zoom.us/) and create a new app or use an existing one
2. Configure an **Incoming Webhook** connector for your Zoom chat channel
3. Obtain the webhook URL and bearer token from your app configuration

!!! important "Security"
    Store webhook URLs and tokens securely using environment variables or a secrets manager. Never commit them directly to your codebase.

## Notification Config Parameters

### Required Parameters

!!! info "user_config.se_notifications_enable_zoom"
    Master toggle to enable Zoom notifications. Set to `True` to activate Zoom notifications.

!!! info "user_config.se_notifications_zoom_webhook_url"
    The Zoom incoming webhook URL where notifications will be sent.

!!! info "user_config.se_notifications_zoom_token"
    The bearer token used for authenticating requests to the Zoom webhook endpoint.

### Notification Triggers

These parameters control **when** Zoom notifications are sent during Spark-Expectations runs:

- <abbr title="Enable notifications when job starts">user_config.se_notifications_on_start</abbr>
- <abbr title="Enable notifications when job ends">user_config.se_notifications_on_completion</abbr>
- <abbr title="Enable notifications on failure">user_config.se_notifications_on_fail</abbr>
- <abbr title="Notify if error drop threshold is breached">user_config.se_notifications_on_error_drop_exceeds_threshold_breach</abbr>
- <abbr title="Notify if rules with action 'ignore' fail">user_config.se_notifications_on_rules_action_if_failed_set_ignore</abbr>
- <abbr title="Threshold value for error drop notifications">user_config.se_notifications_on_error_drop_threshold</abbr>

## Configuration Example

Here is how to configure Zoom notifications in your Spark Expectations setup:

```python
from spark_expectations.config.user_config import Constants as user_config

notification_config = {
    # Enable Zoom notifications
    user_config.se_notifications_enable_zoom: True,

    # Zoom webhook URL (replace with your actual webhook URL)
    user_config.se_notifications_zoom_webhook_url: "https://zoom.us/v2/chat/users/me/messages",

    # Zoom bearer token for authentication
    user_config.se_notifications_zoom_token: "<your-zoom-token>",

    # Configure when to send notifications
    user_config.se_notifications_on_start: True,
    user_config.se_notifications_on_completion: True,
    user_config.se_notifications_on_fail: True,
    user_config.se_notifications_on_error_drop_exceeds_threshold_breach: True,
    user_config.se_notifications_on_error_drop_threshold: 15,
}
```

!!! note "Independence from other channels"
    Zoom notifications can be enabled independently of other notification channels (Slack, Teams, Email, PagerDuty). You can enable any combination of channels that fits your workflow.

## Message Format

Zoom notifications sent by Spark Expectations include:

- **Job Status**: Whether the data quality check started, completed, or failed
- **Data Quality Results**: Summary of passed and failed expectations
- **Error Details**: Information about specific data quality issues
- **Metadata**: Table name, environment, timestamp, and other contextual information

The message payload is formatted with a title of "SE Notification" and includes the full notification text with appropriate line breaks for readability in Zoom chat.
