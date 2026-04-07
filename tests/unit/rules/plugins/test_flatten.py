"""Tests for spark_expectations.rules.plugins._flatten"""

import pytest
from unittest.mock import patch

from spark_expectations.core.exceptions import SparkExpectationsUserInputOrConfigInvalidException
from spark_expectations.rules.plugins._flatten import (
    COLUMN_DEFAULTS,
    RULES_SCHEMA_COLUMNS,
    _cast_value,
    _warn_duplicate_rule_names,
    flatten_rules_list,
)


@pytest.fixture
def minimal_rules_list():
    return {
        "product_id": "prod1",
        "table_name": "db.table1",
        "rules": [
            {
                "rule": "col1_not_null",
                "rule_type": "row_dq",
                "expectation": "col1 IS NOT NULL",
                "column_name": "col1",
                "tag": "completeness",
            }
        ],
    }


@pytest.fixture
def minimal_dq_env_rules():
    return {
        "product_id": "prod1",
        "dq_env": {
            "DEV": {
                "table_name": "catalog.schema.orders",
                "action_if_failed": "ignore",
                "is_active": True,
                "priority": "medium",
            },
            "QA": {
                "table_name": "catalog2.schema.orders",
                "action_if_failed": "ignore",
                "is_active": True,
                "priority": "medium",
            },
            "PROD": {
                "table_name": "catalog3.schema.orders",
                "action_if_failed": "fail",
                "is_active": True,
                "priority": "high",
            },
        },
        "rules": [
            {
                "rule": "col1_not_null",
                "rule_type": "row_dq",
                "expectation": "col1 IS NOT NULL",
                "column_name": "col1",
                "tag": "completeness",
            }
        ],
    }


# ── rules-list format (classic with table_name) ────────────────────────


def test_flatten_rules_list_basic(minimal_rules_list):
    rows = flatten_rules_list(minimal_rules_list)
    assert len(rows) == 1
    row = rows[0]
    assert row["product_id"] == "prod1"
    assert row["table_name"] == "db.table1"
    assert row["rule_type"] == "row_dq"
    assert row["rule"] == "col1_not_null"
    assert row["expectation"] == "col1 IS NOT NULL"


def test_flatten_rules_list_all_schema_columns_present(minimal_rules_list):
    rows = flatten_rules_list(minimal_rules_list)
    for col in RULES_SCHEMA_COLUMNS:
        assert col in rows[0], f"Missing column: {col}"


def test_flatten_rules_list_defaults_applied(minimal_rules_list):
    rows = flatten_rules_list(minimal_rules_list)
    row = rows[0]
    assert row["action_if_failed"] == COLUMN_DEFAULTS["action_if_failed"]
    assert row["is_active"] == COLUMN_DEFAULTS["is_active"]
    assert row["priority"] == COLUMN_DEFAULTS["priority"]


def test_flatten_rules_list_user_defaults_override_column_defaults():
    data = {
        "product_id": "prod1",
        "table_name": "t1",
        "defaults": {"action_if_failed": "fail", "priority": "high"},
        "rules": [{"rule": "r1", "rule_type": "row_dq", "expectation": "x > 0"}],
    }
    rows = flatten_rules_list(data)
    assert rows[0]["action_if_failed"] == "fail"
    assert rows[0]["priority"] == "high"


def test_flatten_rules_list_rule_level_overrides_defaults():
    data = {
        "product_id": "prod1",
        "table_name": "t1",
        "defaults": {"action_if_failed": "ignore"},
        "rules": [
            {
                "rule": "r1",
                "rule_type": "row_dq",
                "expectation": "x > 0",
                "action_if_failed": "drop",
            }
        ],
    }
    rows = flatten_rules_list(data)
    assert rows[0]["action_if_failed"] == "drop"


def test_flatten_rules_list_rule_type_from_defaults():
    data = {
        "product_id": "prod1",
        "table_name": "t1",
        "defaults": {"rule_type": "row_dq"},
        "rules": [{"rule": "r1", "expectation": "x > 0"}],
    }
    rows = flatten_rules_list(data)
    assert rows[0]["rule_type"] == "row_dq"


def test_flatten_rules_list_rule_type_per_rule_overrides_default():
    data = {
        "product_id": "prod1",
        "table_name": "t1",
        "defaults": {"rule_type": "row_dq"},
        "rules": [
            {"rule": "r1", "expectation": "x > 0"},
            {"rule": "r2", "rule_type": "agg_dq", "expectation": "count(*) > 0"},
        ],
    }
    rows = flatten_rules_list(data)
    assert rows[0]["rule_type"] == "row_dq"
    assert rows[1]["rule_type"] == "agg_dq"


def test_flatten_rules_list_table_name_override_per_rule():
    data = {
        "product_id": "prod1",
        "table_name": "default_table",
        "rules": [
            {"rule": "r1", "rule_type": "row_dq", "expectation": "x > 0"},
            {"rule": "r2", "rule_type": "row_dq", "expectation": "y > 0", "table_name": "other_table"},
        ],
    }
    rows = flatten_rules_list(data)
    assert rows[0]["table_name"] == "default_table"
    assert rows[1]["table_name"] == "other_table"


def test_flatten_rules_list_mixed_rule_types():
    data = {
        "product_id": "prod1",
        "table_name": "t1",
        "rules": [
            {"rule": "r1", "rule_type": "row_dq", "expectation": "c1 > 0"},
            {"rule": "r2", "rule_type": "agg_dq", "expectation": "count(*) > 10"},
            {"rule": "r3", "rule_type": "query_dq", "expectation": "SELECT 1"},
        ],
    }
    rows = flatten_rules_list(data)
    assert len(rows) == 3
    assert {r["rule_type"] for r in rows} == {"row_dq", "agg_dq", "query_dq"}


def test_flatten_rules_list_missing_product_id_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="product_id"):
        flatten_rules_list({"rules": [{"rule": "r", "expectation": "x"}]})


def test_flatten_rules_list_empty_rules_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="non-empty"):
        flatten_rules_list({"product_id": "p1", "rules": []})


def test_flatten_rules_list_missing_rule_field_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="missing required"):
        flatten_rules_list(
            {
                "product_id": "p1",
                "rules": [{"expectation": "x > 0"}],
            }
        )


def test_flatten_rules_list_missing_expectation_field_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="missing required"):
        flatten_rules_list(
            {
                "product_id": "p1",
                "rules": [{"rule": "r1"}],
            }
        )


def test_flatten_rules_list_missing_rule_type_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="missing 'rule_type'"):
        flatten_rules_list(
            {
                "product_id": "p1",
                "table_name": "t1",
                "rules": [{"rule": "r1", "expectation": "x > 0"}],
            }
        )


def test_flatten_rules_list_invalid_rule_type_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="Invalid rule_type"):
        flatten_rules_list(
            {
                "product_id": "p1",
                "rules": [{"rule": "r1", "rule_type": "bad_type", "expectation": "x > 0"}],
            }
        )


def test_flatten_rules_list_boolean_values_are_native(minimal_rules_list):
    rows = flatten_rules_list(minimal_rules_list)
    row = rows[0]
    assert isinstance(row["is_active"], bool)
    assert isinstance(row["enable_error_drop_alert"], bool)


def test_flatten_rules_list_no_table_name_at_top_or_rule():
    data = {
        "product_id": "p1",
        "rules": [{"rule": "r1", "rule_type": "row_dq", "expectation": "x > 0"}],
    }
    rows = flatten_rules_list(data)
    assert rows[0]["table_name"] == ""


# ── rules-list format (dq_env) ─────────────────────────────────────────


def test_flatten_rules_list_dq_env_basic(minimal_dq_env_rules):
    rows = flatten_rules_list(minimal_dq_env_rules, env="DEV")
    assert len(rows) == 1
    row = rows[0]
    assert row["product_id"] == "prod1"
    assert row["table_name"] == "catalog.schema.orders"
    assert row["rule"] == "col1_not_null"
    assert row["action_if_failed"] == "ignore"
    assert row["priority"] == "medium"


def test_flatten_rules_list_dq_env_selects_correct_env(minimal_dq_env_rules):
    rows_dev = flatten_rules_list(minimal_dq_env_rules, env="DEV")
    rows_prod = flatten_rules_list(minimal_dq_env_rules, env="PROD")
    assert rows_dev[0]["table_name"] == "catalog.schema.orders"
    assert rows_prod[0]["table_name"] == "catalog3.schema.orders"
    assert rows_prod[0]["action_if_failed"] == "fail"
    assert rows_prod[0]["priority"] == "high"


def test_flatten_rules_list_dq_env_qa_env(minimal_dq_env_rules):
    rows = flatten_rules_list(minimal_dq_env_rules, env="QA")
    assert rows[0]["table_name"] == "catalog2.schema.orders"


def test_flatten_rules_list_dq_env_all_schema_columns(minimal_dq_env_rules):
    rows = flatten_rules_list(minimal_dq_env_rules, env="DEV")
    for col in RULES_SCHEMA_COLUMNS:
        assert col in rows[0], f"Missing column: {col}"


def test_flatten_rules_list_dq_env_rule_overrides_env_defaults():
    data = {
        "product_id": "prod1",
        "dq_env": {
            "DEV": {
                "table_name": "t1",
                "action_if_failed": "ignore",
                "priority": "medium",
            },
        },
        "rules": [
            {
                "rule": "r1",
                "rule_type": "row_dq",
                "expectation": "x > 0",
                "action_if_failed": "drop",
                "priority": "high",
            }
        ],
    }
    rows = flatten_rules_list(data, env="DEV")
    assert rows[0]["action_if_failed"] == "drop"
    assert rows[0]["priority"] == "high"


def test_flatten_rules_list_dq_env_case_insensitive_lookup(minimal_dq_env_rules):
    for env_value in ("DEV", "dev", "Dev", "dEv"):
        rows = flatten_rules_list(minimal_dq_env_rules, env=env_value)
        assert rows[0]["table_name"] == "catalog.schema.orders"


def test_flatten_rules_list_dq_env_lowercase_option_matches_uppercase_key():
    data = {
        "product_id": "prod1",
        "dq_env": {
            "DEV": {
                "table_name": "dev.orders",
                "priority": "medium",
            },
        },
        "rules": [{"rule": "r1", "rule_type": "row_dq", "expectation": "x > 0"}],
    }
    rows = flatten_rules_list(data, env="dev")
    assert rows[0]["table_name"] == "dev.orders"


def test_flatten_rules_list_dq_env_no_env_raises(minimal_dq_env_rules):
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="no environment"):
        flatten_rules_list(minimal_dq_env_rules)


def test_flatten_rules_list_dq_env_missing_env_raises(minimal_dq_env_rules):
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="not found"):
        flatten_rules_list(minimal_dq_env_rules, env="staging")


def test_flatten_rules_list_dq_env_empty_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="non-empty mapping"):
        flatten_rules_list(
            {
                "product_id": "p1",
                "dq_env": {},
                "rules": [{"rule": "r1", "expectation": "x > 0"}],
            },
            env="DEV",
        )


def test_flatten_rules_list_dq_env_not_dict_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="non-empty mapping"):
        flatten_rules_list(
            {
                "product_id": "p1",
                "dq_env": "not_a_dict",
                "rules": [{"rule": "r1", "expectation": "x > 0"}],
            },
            env="DEV",
        )


def test_flatten_rules_list_dq_env_with_multiple_rules():
    data = {
        "product_id": "prod1",
        "dq_env": {
            "DEV": {
                "table_name": "dev.orders",
                "action_if_failed": "ignore",
                "is_active": True,
                "priority": "medium",
            },
        },
        "rules": [
            {
                "rule": "r1",
                "rule_type": "row_dq",
                "expectation": "col1 IS NOT NULL",
                "action_if_failed": "drop",
                "priority": "high",
            },
            {
                "rule": "r2",
                "rule_type": "agg_dq",
                "expectation": "count(*) > 0",
                "action_if_failed": "fail",
            },
        ],
    }
    rows = flatten_rules_list(data, env="DEV")
    assert len(rows) == 2
    assert rows[0]["table_name"] == "dev.orders"
    assert rows[0]["action_if_failed"] == "drop"
    assert rows[0]["priority"] == "high"
    assert rows[1]["table_name"] == "dev.orders"
    assert rows[1]["action_if_failed"] == "fail"
    assert rows[1]["priority"] == "medium"


# ── helper coverage ────────────────────────────────────────────────────


def test_flatten_rules_list_non_dict_rule_entry_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="must be a dict"):
        flatten_rules_list(
            {
                "product_id": "p1",
                "rules": ["not_a_dict"],
            }
        )


def test_flatten_rules_list_rules_not_a_list_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="non-empty"):
        flatten_rules_list(
            {
                "product_id": "p1",
                "rules": "not_a_list",
            }
        )


def test_flatten_rules_list_non_numeric_error_drop_threshold_raises():
    with pytest.raises(SparkExpectationsUserInputOrConfigInvalidException, match="expects an integer"):
        flatten_rules_list(
            {
                "product_id": "p1",
                "table_name": "t1",
                "rules": [
                    {
                        "rule": "r1",
                        "rule_type": "row_dq",
                        "expectation": "x > 0",
                        "error_drop_threshold": "abc",
                    }
                ],
            }
        )


# ── _cast_value coverage ───────────────────────────────────────────────


def test_cast_value_none_boolean_column():
    assert _cast_value("is_active", None) is True
    assert _cast_value("enable_error_drop_alert", None) is False


def test_cast_value_none_int_column():
    assert _cast_value("error_drop_threshold", None) == 0


def test_cast_value_none_string_column():
    assert _cast_value("description", None) == ""
    assert _cast_value("tag", None) == ""


def test_cast_value_boolean_from_string():
    assert _cast_value("is_active", "true") is True
    assert _cast_value("is_active", "True") is True
    assert _cast_value("is_active", "1") is True
    assert _cast_value("is_active", "yes") is True
    assert _cast_value("is_active", "false") is False
    assert _cast_value("is_active", "0") is False
    assert _cast_value("is_active", "no") is False


def test_cast_value_boolean_from_non_bool_non_str():
    assert _cast_value("is_active", 1) is True
    assert _cast_value("is_active", 0) is False


# ── _warn_duplicate_rule_names coverage ───────────────────────────────

_FLATTEN_LOGGER = "spark_expectations.rules.plugins._flatten"


def test_warn_duplicate_rule_names_no_duplicates_no_warning():
    """No warning should be emitted when all rule names are unique."""
    rows = [
        {"rule": "rule_a", "rule_type": "row_dq"},
        {"rule": "rule_b", "rule_type": "row_dq"},
        {"rule": "rule_c", "rule_type": "agg_dq"},
    ]
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        _warn_duplicate_rule_names(rows)
        mock_logger.warning.assert_not_called()


def test_warn_duplicate_rule_names_single_duplicate_warns():
    """A warning should be emitted once when one rule name is duplicated."""
    rows = [
        {"rule": "col1_not_null", "rule_type": "row_dq"},
        {"rule": "col1_not_null", "rule_type": "row_dq"},
        {"rule": "row_count", "rule_type": "agg_dq"},
    ]
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        _warn_duplicate_rule_names(rows)
        assert mock_logger.warning.call_count == 1
        mock_logger.warning.assert_called_once_with(
            "Duplicate rule name detected: '%s' appears %d times in the rules file. "
            "This will cause duplicate DQ checks and double-counting in statistics. "
            "Please ensure every rule has a unique name.",
            "col1_not_null",
            2,
        )


def test_warn_duplicate_rule_names_multiple_duplicates_warns_for_each():
    """A separate warning should be emitted for each duplicated rule name."""
    rows = [
        {"rule": "rule_a", "rule_type": "row_dq"},
        {"rule": "rule_a", "rule_type": "row_dq"},
        {"rule": "rule_b", "rule_type": "agg_dq"},
        {"rule": "rule_b", "rule_type": "agg_dq"},
        {"rule": "rule_b", "rule_type": "agg_dq"},
        {"rule": "rule_c", "rule_type": "row_dq"},
    ]
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        _warn_duplicate_rule_names(rows)
        assert mock_logger.warning.call_count == 2
        warned_names = [call.args[1] for call in mock_logger.warning.call_args_list]
        assert "rule_a" in warned_names
        assert "rule_b" in warned_names


def test_warn_duplicate_rule_names_count_is_correct():
    """The warning should report the correct count for each duplicate."""
    rows = [
        {"rule": "rule_b", "rule_type": "agg_dq"},
        {"rule": "rule_b", "rule_type": "agg_dq"},
        {"rule": "rule_b", "rule_type": "agg_dq"},
    ]
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        _warn_duplicate_rule_names(rows)
        call_args = mock_logger.warning.call_args
        # Third positional arg is the count
        assert call_args.args[2] == 3


def test_warn_duplicate_rule_names_empty_rows_no_warning():
    """No warning should be emitted for an empty rows list."""
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        _warn_duplicate_rule_names([])
        mock_logger.warning.assert_not_called()


# ── flatten_rules_list duplicate detection (integration) ─────────────


def test_flatten_rules_list_duplicate_rule_names_emits_warning():
    """flatten_rules_list should warn when the rules list contains duplicate names."""
    data = {
        "product_id": "prod1",
        "table_name": "db.table1",
        "rules": [
            {
                "rule": "col1_not_null",
                "rule_type": "row_dq",
                "expectation": "col1 IS NOT NULL",
            },
            {
                "rule": "col1_not_null",  # duplicate
                "rule_type": "row_dq",
                "expectation": "col1 IS NOT NULL",
            },
        ],
    }
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        rows = flatten_rules_list(data)

    # Both rules are still returned — warning is non-breaking
    assert len(rows) == 2
    mock_logger.warning.assert_called_once()
    assert "col1_not_null" in mock_logger.warning.call_args.args[1]


def test_flatten_rules_list_unique_rule_names_no_warning():
    """flatten_rules_list should NOT warn when all rule names are unique."""
    data = {
        "product_id": "prod1",
        "table_name": "db.table1",
        "rules": [
            {
                "rule": "col1_not_null",
                "rule_type": "row_dq",
                "expectation": "col1 IS NOT NULL",
            },
            {
                "rule": "col2_positive",
                "rule_type": "row_dq",
                "expectation": "col2 > 0",
            },
        ],
    }
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        rows = flatten_rules_list(data)

    assert len(rows) == 2
    mock_logger.warning.assert_not_called()


# ── cross-rule-type and edge case tests ──────────────────────────────


def test_warn_duplicate_rule_names_cross_rule_type():
    """Same rule name in different rule_types should still be flagged as duplicate."""
    rows = [
        {"rule": "check_null", "rule_type": "row_dq"},
        {"rule": "check_null", "rule_type": "agg_dq"},
        {"rule": "unique_rule", "rule_type": "query_dq"},
    ]
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        _warn_duplicate_rule_names(rows)
        assert mock_logger.warning.call_count == 1
        mock_logger.warning.assert_called_once_with(
            "Duplicate rule name detected: '%s' appears %d times in the rules file. "
            "This will cause duplicate DQ checks and double-counting in statistics. "
            "Please ensure every rule has a unique name.",
            "check_null",
            2,
        )


def test_warn_duplicate_rule_names_empty_names_skipped():
    """Empty rule names should not count as duplicates of each other."""
    rows = [
        {"rule": "", "rule_type": "row_dq"},
        {"rule": "", "rule_type": "row_dq"},
        {"rule": "valid_rule", "rule_type": "agg_dq"},
    ]
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        _warn_duplicate_rule_names(rows)
        # Should warn about empty names, but NOT about duplicates
        assert mock_logger.warning.call_count == 1
        assert "empty or missing" in mock_logger.warning.call_args.args[0]
        assert mock_logger.warning.call_args.args[1] == 2


def test_warn_duplicate_rule_names_missing_rule_key():
    """Rows missing the 'rule' key entirely should be treated as empty names."""
    rows = [
        {"rule_type": "row_dq"},
        {"rule": "valid_rule", "rule_type": "agg_dq"},
    ]
    with patch(f"{_FLATTEN_LOGGER}.logger") as mock_logger:
        _warn_duplicate_rule_names(rows)
        assert mock_logger.warning.call_count == 1
        assert "empty or missing" in mock_logger.warning.call_args.args[0]
