# Rule Examples

This page provides a comprehensive reference of all data quality rule types supported by Spark-Expectations. Rules are organized by DQ level (Row, Aggregation, Query) and grouped by quality dimension tag.

## Row Data Quality Rules

Row-level rules are evaluated against each individual row. Rows that fail are flagged or filtered based on `action_if_failed`.

### Completeness

| Description | Category | Rule Expression |
|-------------|----------|-----------------|
| Expect column values are not null/empty | `null_validation` | `[col_name] is not null` |

### Uniqueness

| Description | Category | Rule Expression |
|-------------|----------|-----------------|
| Expect primary key values are unique | `primary_key_validation` | `count(*) over(partition by [pk_columns] order by 1) = 1` |
| Expect no duplicate rows (preserve one) | `complete_duplicate_validation` | `row_number() over(partition by [all_columns] order by 1) = 1` |

### Validity

| Description | Category | Rule Expression |
|-------------|----------|-----------------|
| Expect date values in correct format | `date_format_validation` | `to_date([date_col], '[format]') is not null` |
| Expect date values match regex | `date_format_validation_with_regex` | `[date_col] rlike '[regex]'` |
| Expect column value is date parseable | `expect_column_values_to_be_date_parseable` | `try_cast([date_col] as date)` |
| Expect values match a regex pattern | `expect_column_values_to_match_regex` | `[col_name] rlike '[regex]'` |
| Expect values do not match a regex | `expect_column_values_to_not_match_regex` | `[col_name] not rlike '[regex]'` |
| Expect values match one of several regex patterns | `expect_column_values_to_match_regex_list` | `[col] not rlike '[re1]' or [col] not rlike '[re2]'` |

### Accuracy

| Description | Category | Rule Expression |
|-------------|----------|-----------------|
| Expect values belong to a set | `expect_column_values_to_be_in_set` | `[col_name] in ([values])` |
| Expect values not in a set | `expect_column_values_to_be_not_in_set` | `[col_name] not in ([values])` |
| Expect values in a range | `expect_column_values_to_be_in_range` | `[col_name] between [min] and [max]` |
| Expect value lengths in a range | `expect_column_value_lengths_to_be_between` | `length([col_name]) between [min] and [max]` |
| Expect value lengths equal to a value | `expect_column_value_lengths_to_be_equal` | `length([col_name]) = [threshold]` |
| Expect values greater than threshold | `expect_column_value_to_be_greater_than` | `[col_name] > [threshold]` |
| Expect values less than threshold | `expect_column_value_to_be_lesser_than` | `[col_name] < [threshold]` |
| Expect values greater than or equal | `expect_column_value_greater_than_equal` | `[col_name] >= [threshold]` |
| Expect values less than or equal | `expect_column_value_lesser_than_equal` | `[col_name] <= [threshold]` |
| Expect column A > column B | `expect_column_pair_values_A_to_be_greater_than_B` | `[col_A] > [col_B]` |
| Expect column A < column B | `expect_column_pair_values_A_to_be_lesser_than_B` | `[col_A] < [col_B]` |
| Expect column A >= column B | `expect_column_A_to_be_greater_than_B` | `[col_A] >= [col_B]` |
| Expect column A <= column B | `expect_column_A_to_be_lesser_than_or_equals_B` | `[col_A] <= [col_B]` |
| Expect multi-column sum equals value | `expect_multicolumn_sum_to_equal` | `[col_1] + [col_2] + [col_3] = [threshold]` |
| Expect sum per category equals value | `expect_sum_of_value_in_subset_equal` | `sum([col]) over(partition by [cat_col] order by 1)` |
| Expect count per category equals value | `expect_count_of_value_in_subset_equal` | `count(*) over(partition by [cat_col] order by 1)` |
| Expect distinct count per category in range | `expect_distinct_value_in_subset_exceeds` | `count(distinct [col]) over(partition by [cat_col] order by 1)` |

## Aggregation Data Quality Rules

Aggregation rules evaluate the entire dataset as a whole (e.g., column statistics, row counts). They run before and/or after row-level DQ.

| Description | Rule Type | Tag | Rule Expression |
|-------------|-----------|-----|-----------------|
| Expect distinct values in a given list | `expect_column_distinct_values_to_be_in_set` | accuracy | `array_intersect(collect_list(distinct [col]), Array($values)) = Array($values)` |
| Expect column mean in range | `expect_column_mean_to_be_between` | consistency | `avg([col_name]) between [lo] and [hi]` |
| Expect column median in range | `expect_column_median_to_be_between` | consistency | `percentile_approx([col], 0.5) between [lo] and [hi]` |
| Expect column std dev in range | `expect_column_stdev_to_be_between` | consistency | `stddev([col_name]) between [lo] and [hi]` |
| Expect unique value count in range | `expect_column_unique_value_count_to_be_between` | accuracy | `count(distinct [col_name]) between [lo] and [hi]` |
| Expect column max in range | `expect_column_max_to_be_between` | accuracy | `max([col_name]) between [lo] and [hi]` |
| Expect column min in range | `expect_column_min_to_be_between` | accuracy | `min([col_name]) between [lo] and [hi]` |
| Expect row count in range (between) | `expect_row_count_to_be_between` | accuracy | `count(*) between [lo] and [hi]` |
| Expect row count in range (comparison) | `expect_row_count_to_be_in_range` | accuracy | `count(*) > [lo] and count(*) < [hi]` |

## Query Data Quality Rules

Query-level rules execute arbitrary SQL subqueries, enabling cross-table validation and complex assertions.

| Description | Rule Type | Tag | Rule Expression |
|-------------|-----------|-----|-----------------|
| Expect distinct count above threshold | `expect_column_distinct_values_greater_than_threshold_value` | accuracy | `(select count(distinct [col]) from [table]) > [threshold]` |
| Expect row counts match between tables | `expect_count_between_two_table_same` | consistency | `(select count(*) from [tbl_a]) = (select count(*) from [tbl_b])` |
| Expect column median in range | `expect_column_median_to_be_between` | consistency | `(select percentile_approx([col], 0.5) from [tbl]) between [lo] and [hi]` |
| Expect column std dev in range | `expect_column_stdev_to_be_between` | consistency | `(select stddev([col]) from [tbl]) between [lo] and [hi]` |
| Expect unique value count in range | `expect_column_unique_value_count_to_be_between` | accuracy | `(select count(distinct [col]) from [tbl]) between [lo] and [hi]` |
| Expect column max in range | `expect_column_max_to_be_between` | accuracy | `(select max([col]) from [tbl]) between [lo] and [hi]` |
| Expect column min in range | `expect_column_min_to_be_between` | accuracy | `(select min([col]) from [tbl]) between [lo] and [hi]` |
| Expect referential integrity | `expect_referential_integrity_between_two_table_should_be_less_than_100` | accuracy | `(select * from [tbl_a] left join [tbl_b] on [cond] where [tbl_b.col] is null) select count(*) from referential_check) < 100` |

### Cross-Table Comparison with Delimiters

For complex cross-table comparisons, use the `@` delimiter (configurable via the `query_dq_delimiter` attribute in the rules table) to define multiple subqueries within a single rule expression. Aliases within curly braces are resolved at compile time.

**Example:** Compare source and target table counts:

```sql
((select count(*) from ({source_f1}) a join ({source_f2}) b on a.customer_id = b.customer_id)
 - (select count(*) from ({target_f1}) a join ({target_f2}) b on source_column = target_column))
 > ({target_f3})
@source_f1@select column, count(*) from source_tbl group by column
@source_f2@select column2, count(*) from table2 group by column2
@target_f1@select column, count(*) from target_tbl group by column
@target_f2@select column2, count(*) from target_tbl2 group by column2
@target_f3@select count(*) from source_tbl
```
