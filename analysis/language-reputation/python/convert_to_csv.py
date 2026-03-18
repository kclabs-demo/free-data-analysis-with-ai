import json
import csv

with open("analysis/language-reputation/results/results_single_tag.json", "r") as f:
    data = json.load(f)

results = data["results"]

with open("analysis/language-reputation/results/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "rank",
            "tag",
            "unique_users",
            "question_count",
            "avg_reputation",
            "median_reputation",
            "min_reputation",
            "max_reputation",
            "stddev_reputation",
        ]
    )
    for i, row in enumerate(results, 1):
        writer.writerow(
            [
                i,
                row["tag"],
                row["unique_users"],
                row["question_count"],
                row["avg_reputation"],
                row["median_reputation"],
                row["min_reputation"],
                row["max_reputation"],
                row["stddev_reputation"],
            ]
        )

print("Saved: analysis/language-reputation/results/results.csv")
