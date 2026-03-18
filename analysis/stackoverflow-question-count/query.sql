-- Query to count total questions in Stack Overflow public dataset
-- Dataset: bigquery-public-data.stackoverflow.posts_questions

SELECT 
  COUNT(*) as total_questions
FROM `bigquery-public-data.stackoverflow.posts_questions`
