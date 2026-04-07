# Notification Architecture

Spark-Expectations uses a plugin-based notification system built on [pluggy](https://pluggy.readthedocs.io/). This page explains how notification channels are registered, when notifications are dispatched, and how to add a custom notification plugin.

## How It Works

The notification system has three layers:

1. **Plugin registry** (`spark_expectations/notifications/__init__.py`) — registers all notification channel plugins (Email, Slack, Teams, Zoom, PagerDuty) with a `pluggy.PluginManager`.
2. **Notification hooks** (`spark_expectations/notifications/plugins/base_notification.py`) — defines the `hookspec` interface that every plugin must implement: `send_notification(...)` and `set_notification_param(...)`.
3. **Notification orchestrator** (`spark_expectations/notifications/push/spark_expectations_notify.py`) — decides *when* to send notifications (on start, completion, failure, threshold breach) and constructs the message body.

When a notification is triggered, the orchestrator calls `_notification_hook.send_notification(...)`. Because pluggy broadcasts hook calls to all registered plugins, every channel receives the call. Each plugin checks its own enable flag (e.g., `get_enable_slack`) and only sends the message if that channel is enabled.

## Notification Triggers

Spark-Expectations sends notifications at several points during a DQ run:

| Trigger | Method | When |
|---------|--------|------|
| Job start | `notify_on_start()` | Before DQ rules execute, if `notification_on_start` is enabled |
| Job completion | `notify_on_completion()` | After all DQ rules pass successfully |
| Job failure | `notify_on_failure()` | When the DQ run raises an exception |
| Error threshold exceeded | `notify_on_exceeds_of_error_threshold()` | When overall error drop percentage exceeds the configured threshold |
| Per-rule threshold exceeded | `notify_rules_exceeds_threshold()` | When individual rules with `enable_error_drop_alert` exceed their thresholds |
| Ignored rules failed | `notify_on_ignore_rules()` | When rules with `action_if_failed=ignore` actually fail |
| Priority-based failed DQ | `notify_on_failed_dq()` | When DQ rules fail, filtered by priority level |

## Supported Channels

| Channel | Plugin class | Enable config key |
|---------|-------------|-------------------|
| Email | `SparkExpectationsEmailPluginImpl` | `se_enable_mail` |
| Slack | `SparkExpectationsSlackPluginImpl` | `se_enable_slack` |
| Microsoft Teams | `SparkExpectationsTeamsPluginImpl` | `se_enable_teams` |
| Zoom | `SparkExpectationsZoomPluginImpl` | `se_enable_zoom` |
| PagerDuty | `SparkExpectationsPagerDutyPluginImpl` | `se_enable_pagerduty` |

Each channel is independently configured. You can enable any combination of channels simultaneously.

## Adding a Custom Notification Plugin

To add a new notification channel:

1. Create a new plugin class that implements the `SparkExpectationsNotification` hookspec:

    ```python
    from spark_expectations.notifications.plugins.base_notification import (
        SparkExpectationsNotification,
        SPARK_EXPECTATIONS_NOTIFICATION_PLUGIN,
    )
    import pluggy

    hookimpl = pluggy.HookimplMarker(SPARK_EXPECTATIONS_NOTIFICATION_PLUGIN)


    class MyCustomNotificationPlugin:

        @hookimpl
        def send_notification(self, _context, _config_args):
            if _context.get_enable_my_channel is True:
                message = _config_args.get("message", "")
                # Send the message via your channel
                ...

        @hookimpl
        def set_notification_param(self, _context):
            # Read configuration from _context and validate
            ...
    ```

2. Register the plugin in `spark_expectations/notifications/__init__.py`:

    ```python
    from spark_expectations.notifications.plugins.my_channel import MyCustomPlugin

    # Inside get_notifications_hook():
    pm.register(MyCustomPlugin(), "spark_expectations_my_channel_notification")
    ```

3. Add the corresponding configuration keys to `SparkExpectationsContext` and `SparkExpectationsReader`.

## Message Format

All notification messages are sent as plain text by default. The Email channel additionally supports HTML and Jinja2 templates for rich formatting. See the [Email Notification Types](email_notification_types.md) page for template details.

When custom email body is enabled (`se_enable_custom_email_body`), the completion and failure notifications use a JSON-formatted body constructed from the DQ statistics dictionary, allowing structured reporting of specific metrics.
