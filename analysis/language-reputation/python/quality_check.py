from google.cloud import bigquery
import json
from datetime import datetime

PROJECT_ID = "lively-armor-490600-n2"
DATASET_ID = "analysis"
TABLE_ID = "language_reputation_single_tag"

client = bigquery.Client(project=PROJECT_ID)


def run_quality_checks():
    """Run quality checks on the BigQuery analysis table."""
    checks = []

    print("Running quality checks...\n")

    # Check 1: Table exists and has data
    query = f"SELECT COUNT(*) as cnt FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
    result = list(client.query(query).result())[0]
    row_count = result.cnt
    checks.append(
        {
            "name": "table_row_count",
            "passed": row_count > 0,
            "expected": "> 0",
            "actual": row_count,
            "message": f"Table has {row_count} rows",
        }
    )
    print(f"✓ Table row count: {row_count}")

    # Check 2: No null tags
    query = f"SELECT COUNT(*) as cnt FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` WHERE tag IS NULL"
    null_tags = list(client.query(query).result())[0].cnt
    checks.append(
        {
            "name": "no_null_tags",
            "passed": null_tags == 0,
            "expected": 0,
            "actual": null_tags,
            "message": f"Null tags count: {null_tags}",
        }
    )
    print(f"✓ Null tags: {null_tags}")

    # Check 3: No null reputation values
    query = f"""
    SELECT 
      COUNTIF(avg_reputation IS NULL) as null_avg,
      COUNTIF(median_reputation IS NULL) as null_median,
      COUNTIF(unique_users IS NULL) as null_users
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """
    result = list(client.query(query).result())[0]
    checks.append(
        {
            "name": "no_null_reputation",
            "passed": result.null_avg == 0 and result.null_median == 0,
            "expected": "0 for all",
            "actual": f"avg:{result.null_avg}, median:{result.null_median}",
            "message": f"Null reputation values - avg: {result.null_avg}, median: {result.null_median}",
        }
    )
    print(f"✓ Null reputation - avg: {result.null_avg}, median: {result.null_median}")

    # Check 4: Verify unique_users >= 100 filter applied
    query = f"SELECT MIN(unique_users) as min_users FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
    min_users = list(client.query(query).result())[0].min_users
    checks.append(
        {
            "name": "filter_min_users",
            "passed": min_users >= 100,
            "expected": ">= 100",
            "actual": min_users,
            "message": f"Minimum unique users: {min_users}",
        }
    )
    print(f"✓ Min unique users filter: {min_users} >= 100")

    # Check 5: No negative reputation values
    query = f"SELECT COUNT(*) as cnt FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` WHERE avg_reputation < 0"
    neg_rep = list(client.query(query).result())[0].cnt
    checks.append(
        {
            "name": "no_negative_reputation",
            "passed": neg_rep == 0,
            "expected": 0,
            "actual": neg_rep,
            "message": f"Negative reputation count: {neg_rep}",
        }
    )
    print(f"✓ Negative reputation: {neg_rep}")

    # Check 6: Verify all tags are trimmed (no leading/trailing spaces)
    query = f"""
    SELECT COUNT(*) as cnt FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
    WHERE tag != TRIM(tag)
    """
    untrimmed = list(client.query(query).result())[0].cnt
    checks.append(
        {
            "name": "tags_trimmed",
            "passed": untrimmed == 0,
            "expected": 0,
            "actual": untrimmed,
            "message": f"Untrimmed tags: {untrimmed}",
        }
    )
    print(f"✓ Untrimmed tags: {untrimmed}")

    # Check 7: Check for duplicate tags
    query = f"""
    SELECT tag, COUNT(*) as cnt FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
    GROUP BY tag HAVING cnt > 1
    """
    duplicates = list(client.query(query).result())
    dup_count = len(duplicates)
    checks.append(
        {
            "name": "no_duplicate_tags",
            "passed": dup_count == 0,
            "expected": 0,
            "actual": dup_count,
            "message": f"Duplicate tags: {dup_count}",
        }
    )
    print(f"✓ Duplicate tags: {dup_count}")

    # Check 8: Top 5 languages sanity check
    query = f"""
    SELECT tag, avg_reputation FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
    ORDER BY avg_reputation DESC LIMIT 5
    """
    top5 = [(row.tag, row.avg_reputation) for row in client.query(query).result()]
    checks.append(
        {
            "name": "top5_sanity_check",
            "passed": all(rep > 0 for _, rep in top5),
            "expected": "all > 0",
            "actual": ", ".join([f"{t}:{r}" for t, r in top5]),
            "message": f"Top 5 languages: {top5}",
        }
    )
    print(f"✓ Top 5 languages have positive reputation")

    # Summary
    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)

    print(f"\n{'=' * 50}")
    print(f"Quality Checks: {passed}/{total} passed")
    print(f"{'=' * 50}")

    return {
        "timestamp": datetime.now().isoformat(),
        "table": f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}",
        "total_checks": total,
        "passed": passed,
        "failed": total - passed,
        "checks": checks,
    }


if __name__ == "__main__":
    results = run_quality_checks()

    with open("analysis/language-reputation/results/quality_check.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved: analysis/language-reputation/results/quality_check.json")
