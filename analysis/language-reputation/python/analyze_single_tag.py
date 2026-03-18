from google.cloud import bigquery
import json
from datetime import datetime

PROJECT_ID = "lively-armor-490600-n2"
DATASET_ID = "analysis"
TABLE_ID = "language_reputation_single_tag"

client = bigquery.Client(project=PROJECT_ID)

create_table_sql = """
CREATE OR REPLACE TABLE `{project}.{dataset}.{table}` AS
SELECT 
  tag,
  COUNT(DISTINCT owner_user_id) as unique_users,
  COUNT(*) as question_count,
  AVG(user_reputation) as avg_reputation,
  APPROX_QUANTILES(user_reputation, 100)[OFFSET(50)] as median_reputation,
  MIN(user_reputation) as min_reputation,
  MAX(user_reputation) as max_reputation,
  STDDEV(user_reputation) as stddev_reputation
FROM (
  SELECT 
    TRIM(tag) as tag,
    owner_user_id,
    u.reputation as user_reputation
  FROM `bigquery-public-data.stackoverflow.posts_questions` q
  CROSS JOIN UNNEST(SPLIT(q.tags, '|')) as tag
  INNER JOIN `bigquery-public-data.stackoverflow.users` u 
    ON q.owner_user_id = u.id
  WHERE u.reputation >= 100
    AND q.owner_user_id IS NOT NULL
    AND (LENGTH(q.tags) - LENGTH(REPLACE(q.tags, '|', ''))) = 0
)
GROUP BY tag
HAVING unique_users >= 100
ORDER BY avg_reputation DESC
""".format(project=PROJECT_ID, dataset=DATASET_ID, table=TABLE_ID)

print("Creating single-tag aggregated table in BigQuery...")
job = client.query(create_table_sql)
job.result()
print(f"Table created: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")

print("\nFetching results...")
query = f"""
SELECT 
  tag,
  unique_users,
  question_count,
  ROUND(avg_reputation, 2) as avg_reputation,
  median_reputation,
  min_reputation,
  max_reputation,
  ROUND(stddev_reputation, 2) as stddev_reputation
FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
ORDER BY avg_reputation DESC
LIMIT 50
"""

results = client.query(query).result()
rows = list(results)

print(f"Retrieved {len(rows)} languages")

data = []
for row in rows:
    data.append(
        {
            "tag": row.tag,
            "unique_users": row.unique_users,
            "question_count": row.question_count,
            "avg_reputation": row.avg_reputation,
            "median_reputation": row.median_reputation,
            "min_reputation": row.min_reputation,
            "max_reputation": row.max_reputation,
            "stddev_reputation": row.stddev_reputation,
        }
    )

output_json = {
    "generated_at": datetime.now().isoformat(),
    "filter": "users.reputation >= 100",
    "min_unique_users": 100,
    "tag_type": "single_tag_only",
    "total_languages": len(data),
    "results": data,
}

with open("analysis/language-reputation/results_single_tag.json", "w") as f:
    json.dump(output_json, f, indent=2)
print("Saved: analysis/language-reputation/results_single_tag.json")

markdown = """# Programming Language vs Stack Overflow Reputation Analysis

## Methodology
- **Data Source**: Stack Overflow public BigQuery dataset
- **Proxy Metric**: User reputation (as salary/success proxy)
- **Filter**: Users with reputation >= 100
- **Minimum Users**: 100 per language tag
- **Tag Type**: Single tags only (questions with exactly 1 tag)
- **Note**: Stack Overflow uses "|" (pipe) as tag separator

## Top 50 Languages by Average Reputation

| Rank | Language | Unique Users | Questions | Avg Reputation | Median Reputation |
|------|----------|---------------|-----------|----------------|-------------------|
"""

for i, row in enumerate(data, 1):
    markdown += f"| {i} | {row['tag']} | {row['unique_users']:,} | {row['question_count']:,} | {row['avg_reputation']:,.2f} | {row['median_reputation']:,} |\n"

markdown += f"""
## Summary
- **Total Languages Analyzed**: {len(data)}
- **Generated**: {output_json["generated_at"]}
- **Note**: Higher reputation may correlate with expertise/salary but is not a direct measure
"""

with open("analysis/language-reputation/results_single_tag.md", "w") as f:
    f.write(markdown)
print("Saved: analysis/language-reputation/results_single_tag.md")

print("\nDone!")
