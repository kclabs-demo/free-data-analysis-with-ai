-- Exploration queries for Stack Overflow schema

-- 1. List all tables
SELECT table_name 
FROM `bigquery-public-data.stackoverflow.INFORMATION_SCHEMA.tables`
WHERE table_schema = '';

-- 2. Check users schema
SELECT column_name, data_type 
FROM `bigquery-public-data.stackoverflow.INFORMATION_SCHEMA.columns`
WHERE table_name = 'users';

-- 3. Check posts_questions schema
SELECT column_name, data_type 
FROM `bigquery-public-data.stackoverflow.INFORMATION_SCHEMA.columns`
WHERE table_name = 'posts_questions';

-- 4. Sample tags from posts_questions
SELECT DISTINCT tags 
FROM `bigquery-public-data.stackoverflow.posts_questions`
WHERE tags IS NOT NULL
LIMIT 5;

-- 5. Count users with reputation >= 100
SELECT COUNT(*) as user_count
FROM `bigquery-public-data.stackoverflow.users`
WHERE reputation >= 100;

-- 6. Sample exploded tags
SELECT tag, COUNT(*) as tag_count
FROM (
  SELECT TRIM(tag) as tag
  FROM `bigquery-public-data.stackoverflow.posts_questions`,
  UNNEST(SPLIT(tags, ',')) as tag
)
GROUP BY tag
ORDER BY tag_count DESC
LIMIT 20;
