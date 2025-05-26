
-- Top 1 post per ID, with highest upvotes, then top 5 posts overall:
WITH top_posts AS (
  SELECT
    ARRAY_AGG(t ORDER BY ups DESC LIMIT 1)[OFFSET(0)] AS top_post
  FROM (
    SELECT id, selftext, title, upvote_ratio, ups, downs
    FROM `practical-bolt-460017-e3.reddit_dataset.reddit_data`
  ) t
  GROUP BY id
)

SELECT *
FROM top_posts
ORDER BY top_post.ups DESC
LIMIT 5;