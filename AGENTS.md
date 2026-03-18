# AGENTS.md

> IMPORTANT: Everything in this repo is public-facing, so do not place any sensitive info here and make sure to distinguish between what should be internal-facing info (e.g. secrets, PII, recording guides/scripts), and public-facing info (instructions, how-to guides, actual code utilized). If there is information that Claude Code needs across sessions but should not be published, put it in the `.internal/` folder which is ignored by git per the `.gitignore`.

## Project Context

This is a public demo repository for a KC Labs AI YouTube video on free data analysis with AI.

## Code Standards

- Keep tutorials beginner-friendly
- Include inline comments explaining key concepts
- Use clear, descriptive variable names
- Test all code before committing

## Directory Structure

```
├── .internal/              # Internal-only files (not published)
├── analysis/               # Data analysis projects
│   ├── language-reputation/     # Language vs SO reputation analysis
│   └── stackoverflow-question-count/  # Dataset scale verification
├── example_workflow/
│   └── AGENTS.md           # Sample AGENTS.md for viewers
├── images/                 # Diagrams (Excalidraw + PNG)
├── instructions/
│   └── setup_guide.md      # Condensed 8-step setup guide
├── AGENTS.md               # This file
└── README.md               # Public guide
```

## Analysis Project Structure

All analysis projects should follow this structure:

```
analysis/<project-name>/
├── sql/
│   ├── exploration.sql    # Schema discovery queries
│   └── create_table.sql  # Table creation queries
├── python/
│   ├── analyze.py        # Main analysis script
│   └── quality_check.py  # Data quality validation
├── results/
│   ├── results.json      # Raw results (JSON)
│   ├── results.md        # Formatted results (Markdown)
│   └── quality_check.json  # QC report
└── README.md             # Combined project documentation
```

### Quality Check Requirements

All analysis projects must include:
- Row count validation
- Null check verification
- Filter/application confirmation
- Data integrity checks

## Commands

Coming soon...

## GCP Access

- **gcloud CLI**: Available at `/opt/homebrew/bin/gcloud`
- **bq CLI**: Available at `/opt/homebrew/bin/bq`
- **Project**: `lively-armor-490600-n2` (My Project 80907)
- **Auth**: User is authenticated via `gcloud auth login`

### BigQuery CLI Cheat Sheet

```bash
# Always specify project_id to avoid "Access Denied" errors on default project
bq --project_id=lively-armor-490600-n2 query --use_legacy_sql=false "SELECT ..."

# List tables in a public dataset
bq ls bigquery-public-data:stackoverflow

# Query public dataset (use backticks for full path)
bq --project_id=lively-armor-490600-n2 query --use_legacy_sql=false \
  "SELECT COUNT(*) FROM \`bigquery-public-data.stackoverflow.posts_questions\`"
```

Key notes:
- Always use `--project_id=lively-armor-490600-n2` to avoid permission errors on default project
- Use `--use_legacy_sql=false` for standard SQL (recommended)
- Public datasets are accessed via `bigquery-public-data.<dataset>.<table>`
