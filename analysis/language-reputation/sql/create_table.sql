-- Create aggregated table: average reputation by programming language tag
-- Filters: users with reputation >= 100

CREATE OR REPLACE TABLE `lively-armor-490600-n2.analysis.language_reputation_by_tag` AS
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
  FROM `bigquery-public-data.stackoverflow.posts_questions`,
  UNNEST(SPLIT(tags, ',')) as tag
  INNER JOIN `bigquery-public-data.stackoverflow.users` u 
    ON owner_user_id = u.id
  WHERE u.reputation >= 100
    AND owner_user_id IS NOT NULL
)
GROUP BY tag
HAVING unique_users >= 100
ORDER BY avg_reputation DESC;
