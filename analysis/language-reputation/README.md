# Programming Language vs Stack Overflow Reputation Analysis

## Overview

This analysis explores the relationship between programming language choice and developer success on Stack Overflow, using user **reputation as a proxy for salary/expertise**.

## Data Source

- **Dataset**: `bigquery-public-data.stackoverflow`
- **Project**: `lively-armor-490600-n2`
- **BigQuery Table**: `analysis.language_reputation_single_tag`

## Schema Analysis

### Source Tables

| Table | Rows | Description |
|-------|------|-------------|
| users | 18,712,212 | User profiles with reputation |
| posts_questions | 23,020,127 | Questions with tags |
| posts_answers | 44,873,232 | Answers to questions |
| tags | 63,653 | Tag metadata |

### Key Columns Used

| Table | Column | Type | Notes |
|-------|--------|------|-------|
| users | reputation | INTEGER | **Proxy for salary/success** |
| users | id | INTEGER | Primary key |
| posts_questions | owner_user_id | INTEGER | Links to users |
| posts_questions | tags | STRING | Pipe-separated ("\|") |

### Important Note

**Stack Overflow uses "|" (pipe) as tag separator, not commas.**

## Methodology

1. Filter questions to those with **exactly 1 tag** (single-tag questions)
2. Join with users table on `owner_user_id`
3. Filter users with `reputation >= 100`
4. Require **minimum 100 unique users** per language tag
5. Aggregate: avg/median reputation per language

## Quality Checks

| Check | Status |
|-------|--------|
| Table row count > 0 | ✓ Passed (893 rows) |
| No null tags | ✓ Passed |
| No null reputation values | ✓ Passed |
| Filter min users >= 100 | ✓ Passed |
| No negative reputation | ✓ Passed |
| Tags trimmed | ✓ Passed |
| No duplicate tags | ✓ Passed |
| Top 5 sanity check | ✓ Passed |

**Quality Checks: 8/8 passed**

## Results: Top 50 Tags by Average Reputation

| Rank | Language/Tag | Unique Users | Questions | Avg Reputation | Median Reputation |
|------|---------------|--------------|-----------|----------------|-------------------|
| 1 | open-source | 100 | 104 | 28,117.73 | 5,873 |
| 2 | filemaker | 134 | 222 | 27,097.54 | 1,732 |
| 3 | scons | 166 | 246 | 24,491.55 | 3,198 |
| 4 | user-interface | 174 | 185 | 24,190.96 | 9,540 |
| 5 | coding-style | 157 | 161 | 23,864.83 | 5,752 |
| 6 | mercurial | 983 | 1,368 | 22,853.75 | 5,359 |
| 7 | language-agnostic | 546 | 592 | 22,680.10 | 6,237 |
| 8 | fonts | 102 | 103 | 22,047.80 | 1,618 |
| 9 | unicode | 163 | 171 | 21,662.70 | 4,391 |
| 10 | version-control | 268 | 276 | 21,497.80 | 5,494 |
| 11 | terminology | 142 | 150 | 21,323.44 | 6,019 |
| 12 | naming-conventions | 105 | 108 | 21,030.45 | 5,868 |
| 13 | nunit | 124 | 137 | 20,028.80 | 4,847 |
| 14 | project-management | 152 | 157 | 19,681.77 | 5,880 |
| 15 | gnu-make | 133 | 166 | 19,588.88 | 1,707 |
| 16 | maven-2 | 224 | 297 | 19,299.25 | 5,443 |
| 17 | fish | 158 | 216 | 18,792.28 | 4,203 |
| 18 | programming-languages | 294 | 306 | 18,619.92 | 5,116 |
| 19 | visual-studio-2008 | 406 | 489 | 17,890.66 | 5,374 |
| 20 | testing | 176 | 188 | 17,812.43 | 2,498 |
| 21 | elisp | 105 | 144 | 17,739.10 | 3,639 |
| 22 | licensing | 103 | 105 | 17,361.18 | 4,548 |
| 23 | url | 137 | 138 | 16,697.51 | 3,254 |
| 24 | nuget | 345 | 390 | 16,415.68 | 4,769 |
| 25 | unit-testing | 327 | 346 | 16,332.99 | 4,857 |
| 26 | svn | 2,165 | 2,620 | 16,224.93 | 3,812 |
| 27 | .net | 1,380 | 1,767 | 16,198.27 | 4,119 |
| 28 | security | 313 | 329 | 15,983.90 | 2,913 |
| 29 | http | 376 | 406 | 15,784.80 | 2,912 |
| 30 | zsh | 288 | 367 | 15,742.16 | 3,714 |
| 31 | database-design | 641 | 720 | 15,738.53 | 2,755 |
| 32 | linq-to-sql | 480 | 679 | 15,654.77 | 4,619 |
| 33 | msbuild | 575 | 733 | 15,623.89 | 4,730 |
| 34 | winapi | 558 | 799 | 15,604.48 | 2,136 |
| 35 | nhibernate | 710 | 1,159 | 15,350.02 | 3,905 |
| 36 | gdb | 373 | 479 | 15,215.38 | 2,633 |
| 37 | email | 167 | 170 | 14,872.16 | 2,105 |
| 38 | coffeescript | 435 | 542 | 14,846.46 | 4,825 |
| 39 | resharper | 215 | 242 | 14,837.58 | 5,056 |
| 40 | emacs | 1,172 | 1,929 | 14,651.73 | 3,890 |
| 41 | vim | 4,088 | 6,763 | 14,380.73 | 3,317 |
| 42 | windbg | 162 | 244 | 14,164.07 | 2,953 |
| 43 | sbt | 377 | 553 | 13,815.44 | 3,875 |
| 44 | web-services | 257 | 274 | 13,521.09 | 2,938 |
| 45 | git | 13,787 | 20,292 | 13,485.98 | 3,267 |
| 46 | cookies | 147 | 153 | 13,230.11 | 1,884 |
| 47 | memcached | 125 | 139 | 13,154.91 | 3,866 |
| 48 | cocoa-touch | 118 | 198 | 13,142.79 | 4,311 |
| 49 | netbeans | 329 | 358 | 13,141.60 | 2,485 |
| 50 | floating-point | 110 | 116 | 13,090.71 | 1,657 |

## Key Findings

- **Top tags by reputation** include concepts like "open-source", "user-interface", and "version-control" - not just programming languages
- Popular languages like **git** (13,487 avg rep), **.net** (16,198 avg rep), and **vim** (14,381 avg rep) appear in the results
- The analysis uses **single-tag questions only**, which limits the dataset but ensures clean language attribution

## Limitations

- **No actual salary data** - using Stack Overflow reputation as a proxy
- Single-tag filter excludes many questions (most have multiple tags)
- Reputation doesn't perfectly correlate with salary (experts may not answer many questions)

## Files in This Analysis

```
analysis/language-reputation/
├── sql/
│   ├── exploration.sql
│   └── create_table.sql
├── python/
│   ├── analyze.py
│   ├── analyze_single_tag.py
│   └── quality_check.py
├── results/
│   ├── results.json
│   ├── results_single_tag.json
│   ├── results.md
│   ├── results_single_tag.md
│   └── quality_check.json
└── README.md
```
