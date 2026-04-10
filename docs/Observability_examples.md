# Spark Expectations Observability Features

## Overview

This document provides an overview of the observability features available in Spark Expectations for data quality (DQ) checks. Observability in this context refers to the ability to monitor, measure, and understand the state and performance of data quality rules applied to datasets.

## Required Configuration

To enable observability, add the following attributes to your `user_conf` dictionary:

```python
user_conf = {
    user_config.se_enable_obs_dq_report_result: True,
    user_config.se_dq_obs_alert_flag: True,
    user_config.se_dq_obs_default_email_template: "",
    # SMTP details are required for email alerts
    user_config.se_notifications_email_smtp_host: "smtp.example.com",
    user_config.se_notifications_email_smtp_port: 587,
    user_config.se_notifications_email_from: "dq-alerts@example.com",
    user_config.se_notifications_email_to_other_mail_id: "team@example.com",
    user_config.se_notifications_smtp_password: "************",
}
```

## Observability Flows

Spark Expectations supports two observability flows, controlled by the configuration flags above.

### Flow 1: DQ Report Generation

When only the DQ report flag is enabled (`se_enable_obs_dq_report_result: True`), the system generates a report table upon the successful completion of Spark Expectations. This flow focuses solely on report generation without triggering any alerts.

### Flow 2: DQ Report Generation with Email Alerts

When both the DQ report flag and alert flag are enabled (`se_dq_obs_alert_flag: True`), the system performs two actions:

1. Generates the report table after Spark Expectations completes.
2. Sends an email alert to the configured email address with the results.

### Key Differences

| Setting | Report Generated | Email Alert Sent |
|---------|:----------------:|:----------------:|
| `se_enable_obs_dq_report_result: True` only | Yes | No |
| Both `se_enable_obs_dq_report_result: True` and `se_dq_obs_alert_flag: True` | Yes | Yes |

The report table is auto-generated — you do not need to create it manually.

## Report Table Details

The report table is derived from the **Query DQ Output Table** and the **Detailed Table**. It calculates key metrics, numerical summaries, and other analytical insights. To ensure consistency and accuracy, users must follow predefined standards when writing queries for the Query DQ Output Table.

Below is an example of how rules can be configured:

```python
RULES_DATA = """
("your_product", "dq_spark_dev.customer_order", "row_dq", "sales_greater_than_zero",
 "sales", "sales > 2", "ignore", "accuracy",
 "sales value should be greater than zero",
 false, true, true, false, 0, null, null, "medium")

,("your_product", "dq_spark_{env}.customer_order", "row_dq", "discount_threshold",
  "discount", "discount*100 < 60", "drop", "validity",
  "discount should be less than 40",
  true, true, true, false, 0, null, null, "medium")

,("your_product", "dq_spark_{env}.customer_order", "row_dq", "ship_mode_in_set",
  "ship_mode", "lower(trim(ship_mode)) in('second class', 'standard class', 'standard class')",
  "drop", "validity", "ship_mode mode belongs in the sets",
  true, true, true, false, 0, null, null, "medium")

,("your_product", "dq_spark_{env}.customer_order", "row_dq", "profit_threshold",
  "profit", "profit>0", "ignore", "validity",
  "profit threshold should be greater than 0",
  false, true, false, true, 0, null, null, "medium")

,("your_product", "dq_spark_dev.customer_order", "query_dq", "product_missing_count_threshold",
  "column_name",
  "((select count(*) from ({source_f1}) a) - (select count(*) from ({target_f1}) b)) > 3
   @source_f1@SELECT DISTINCT product_id, order_id, order_date, COUNT(*) AS count
              FROM order_source GROUP BY product_id, order_id, order_date
   @target_f1@SELECT DISTINCT product_id, order_id, order_date, COUNT(*) AS count
              FROM order_target GROUP BY product_id, order_id, order_date",
  "ignore", "validity", "row count threshold",
  true, false, true, false, 0, null, true, "medium")
"""
```

## Template Options for Report Table Rendering

Users have two options for rendering the report table in email alerts:

**Custom Template:** If you provide a custom template through the `se_dq_obs_default_email_template` attribute, the system will use it to render the report table.

```python
user_config.se_dq_obs_default_email_template: "/path/to/your/template.jinja"
```

**Default Jinja Template:** If no custom template is provided (empty string), the system falls back to the built-in default template located at [`spark_expectations/config/templates/advanced_email_alert_template.jinja`](../spark_expectations/config/templates/advanced_email_alert_template.jinja).

## Sample Email Alert

Below is an example of the alert received via email:

![Spark Expectations alert](se_diagrams/alert_sample.png)
