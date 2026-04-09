# Notifications

Spark Expectations can send notifications at key points during data quality execution, keeping your team informed about job status, failures, and threshold breaches. Notifications are disabled by default and must be explicitly enabled per channel.

## Supported Channels

| Channel    | Protocol          | Use Case                                          |
|------------|-------------------|---------------------------------------------------|
| **Email**  | SMTP              | Detailed reports with HTML templates               |
| **Slack**  | Incoming Webhook  | Real-time team alerts in Slack channels            |
| **Teams**  | Incoming Webhook  | Real-time team alerts in Microsoft Teams channels  |
| **PagerDuty** | Events API v2 | Incident creation for critical failures only       |

## Notification Triggers

All channels share a common set of trigger parameters that control **when** notifications are sent. Each trigger can be independently enabled or disabled:

| Trigger | Config Key | Description |
|---------|-----------|-------------|
| Job Start | `se_notifications_on_start` | Fires when the DQ job begins |
| Job Completion | `se_notifications_on_completion` | Fires when the DQ job finishes successfully |
| Job Failure | `se_notifications_on_fail` | Fires when the DQ job encounters a failure |
| Error Drop Threshold | `se_notifications_on_error_drop_exceeds_threshold_breach` | Fires when dropped rows exceed the configured threshold |
| Ignored Rule Failure | `se_notifications_on_rules_action_if_failed_set_ignore` | Fires when rules with `action_if_failed=ignore` fail |

!!! note "PagerDuty Exception"
    PagerDuty only creates incidents for failure-related triggers (job failure and error threshold breach). Start, completion, and ignored-rule triggers are skipped for PagerDuty to avoid unnecessary incident noise.

## Quick Setup

To enable any notification channel, you need two things: the channel's master toggle set to `True`, and the channel-specific connection details (webhook URL, SMTP host, etc.). See the individual channel guides for complete configuration examples.

## Channel Guides

- [Email Notifications](email_notifications.md) -- SMTP-based alerts with HTML template support
- [Slack Notifications](slack_notifications.md) -- Webhook-based Slack channel alerts
- [Teams Notifications](teams_notifications.md) -- Webhook-based Microsoft Teams alerts
- [PagerDuty Notifications](pagerduty_notifications.md) -- Incident creation via Events API v2
