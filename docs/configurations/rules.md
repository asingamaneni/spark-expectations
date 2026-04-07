# Data Quality Rule Types

This page provides a comprehensive reference of all supported data quality rule types in spark-expectations, organized by rule category.

---

## Row Data Quality Expectations

Row-level rules are evaluated against each individual row in the dataset. Rows that fail these rules are handled according to the configured `action_if_failed` setting (`drop`, `ignore`, or `fail`).

### Null & Completeness Checks

| Description | Category | Tag | Expectation |
|:------------|:---------|:----|:------------|
| Column values should not be null/empty | `null_validation` | completeness | `[col_name] is not null` |

### Uniqueness Checks

| Description | Category | Tag | Expectation |
|:------------|:---------|:----|:------------|
| Primary key values are unique | `primary_key_validation` | uniqueness | `count(*) over(partition by [pk_cols] order by 1) = 1` |
| No complete duplicate rows (preserves one) | `complete_duplicate_validation` | uniqueness | `row_number() over(partition by [all_cols] order by 1) = 1` |

### Date & Format Validation

| Description | Category | Tag | Expectation |
|:------------|:---------|:----|:------------|
| Date values are in the correct format | `date_format_validation` | validity | `to_date([date_col], '[format]') is not null` |
| Date values match format via regex | `date_format_validation_with_regex` | validity | `[date_col] rlike '[regex]'` |
| Column value is date-parseable | `expect_column_values_to_be_date_parseable` | validity | `try_cast([date_col] as date)` |
| Values match a regex pattern | `expect_column_values_to_match_regex` | validity | `[col_name] rlike '[regex]'` |
| Values do not match a regex pattern | `expect_column_values_to_not_match_regex` | validity | `[col_name] not rlike '[regex]'` |
| Values match one of multiple regex patterns | `expect_column_values_to_match_regex_list` | validity | `[col] not rlike '[r1]' or [col] not rlike '[r2]'` |

### Value Range & Set Checks

| Description | Category | Tag | Expectation |
|:------------|:---------|:----|:------------|
| Values belong to a specified set | `expect_column_values_to_be_in_set` | accuracy | `[col_name] in ([values])` |
| Values do not belong to a specified set | `expect_column_values_to_be_not_in_set` | accuracy | `[col_name] not in ([values])` |
| Values fall within a defined range | `expect_column_values_to_be_in_range` | accuracy | `[col_name] between [min] and [max]` |
| Value lengths are within a range | `expect_column_value_lengths_to_be_between` | accuracy | `length([col_name]) between [min] and [max]` |
| Value lengths equal a certain value | `expect_column_value_lengths_to_be_equal` | accuracy | `length([col_name]) = [threshold]` |

### Comparison Checks

| Description | Category | Tag | Expectation |
|:------------|:---------|:----|:------------|
| Value exceeds a threshold | `expect_column_value_to_be_greater_than` | accuracy | `[col_name] > [threshold]` |
| Value is below a threshold | `expect_column_value_to_be_lesser_than` | accuracy | `[col_name] < [threshold]` |
| Value is greater than or equal to threshold | `expect_column_value_greater_than_equal` | accuracy | `[col_name] >= [threshold]` |
| Value is less than or equal to threshold | `expect_column_value_lesser_than_equal` | accuracy | `[col_name] <= [threshold]` |
| Column A values greater than column B | `expect_column_pair_values_A_to_be_greater_than_B` | accuracy | `[col_A] > [col_B]` |
| Column A values less than column B | `expect_column_pair_values_A_to_be_lesser_than_B` | accuracy | `[col_A] < [col_B]` |
| Column A >= column B | `expect_column_A_to_be_greater_than_B` | accuracy | `[col_A] >= [col_B]` |
| Column A <= column B | `expect_column_A_to_be_lesser_than_or_equals_B` | accuracy | `[col_A] <= [col_B]` |

### Multi-Column & Windowed Checks

| Description | Category | Tag | Expectation |
|:------------|:---------|:----|:------------|
| Sum across columns equals a value | `expect_multicolumn_sum_to_equal` | accuracy | `[col_1] + [col_2] + [col_3] = [value]` |
| Sum per category equals a value | `expect_sum_of_value_in_subset_equal` | accuracy | `sum([col]) over(partition by [cat] order by 1)` |
| Count per category equals a value | `expect_count_of_value_in_subset_equal` | accuracy | `count(*) over(partition by [cat] order by 1)` |
| Distinct values per category exceeds range | `expect_distinct_value_in_subset_exceeds` | accuracy | `count(distinct [col]) over(partition by [cat] order by 1)` |

---

## Aggregation Data Quality Expectations

Aggregation rules operate on the entire dataset and evaluate aggregate metrics such as sums, counts, averages, and statistical measures.

| Description | Category | Tag | Expectation |
|:------------|:---------|:----|:------------|
| Distinct values in column are in a given list | `expect_column_distinct_values_to_be_in_set` | accuracy | `array_intersect(collect_list(distinct [col]), Array($vals)) = Array($vals)` |
| Mean value within a range | `expect_column_mean_to_be_between` | consistency | `avg([col]) between [low] and [high]` |
| Median value within a range | `expect_column_median_to_be_between` | consistency | `percentile_approx([col], 0.5) between [low] and [high]` |
| Standard deviation within a range | `expect_column_stdev_to_be_between` | consistency | `stddev([col]) between [low] and [high]` |
| Unique value count within a range | `expect_column_unique_value_count_to_be_between` | accuracy | `count(distinct [col]) between [low] and [high]` |
| Max value within a range | `expect_column_max_to_be_between` | accuracy | `max([col]) between [low] and [high]` |
| Min value within a range | `expect_column_min_to_be_between` | accuracy | `min([col]) between [low] and [high]` |
| Row count within a range | `expect_row_count_to_be_between` | accuracy | `count(*) between [low] and [high]` |
| Row count in range (using comparison) | `expect_row_count_to_be_in_range` | accuracy | `count(*) > [low] and count(*) < [high]` |

---

## Query Data Quality Expectations

Query-level rules use subqueries to validate data across tables or complex conditions that cannot be expressed as single-row or simple aggregate checks.

| Description | Category | Tag | Expectation |
|:------------|:---------|:----|:------------|
| Distinct values exceed threshold | `expect_column_distinct_values_greater_than_threshold_value` | accuracy | `(select count(distinct [col]) from [tbl]) > [val]` |
| Row counts match between two tables | `expect_count_between_two_table_same` | consistency | `(select count(*) from [tbl_a]) = (select count(*) from [tbl_b])` |
| Median value within a range | `expect_column_median_to_be_between` | consistency | `(select percentile_approx([col], 0.5) from [tbl]) between [low] and [high]` |
| Standard deviation within a range | `expect_column_stdev_to_be_between` | consistency | `(select stddev([col]) from [tbl]) between [low] and [high]` |
| Unique value count within a range | `expect_column_unique_value_count_to_be_between` | accuracy | `(select count(distinct [col]) from [tbl]) between [low] and [high]` |
| Max value within a range | `expect_column_max_to_be_between` | accuracy | `(select max([col]) from [tbl]) between [low] and [high]` |
| Min value within a range | `expect_column_min_to_be_between` | accuracy | `(select min([col]) from [tbl]) between [low] and [high]` |
| Referential integrity check | `expect_referential_integrity` | accuracy | `(select count(*) from (select * from [tbl_a] left join [tbl_b] on [cond] where [tbl_b.col] is null)) < 100` |
| Cross-table comparison with delimiter | `customer_missing_count_threshold` | validity | Uses `@` delimiter to compose multi-subquery expectations with aliased template variables |
