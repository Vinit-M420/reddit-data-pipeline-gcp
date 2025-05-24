
SELECT id, selftext, title, upvote_ratio
FROM
  `practical-bolt-460017-e3`.`reddit_dataset`.`reddit_data` 
  order by upvote_ratio DESC
  LIMIT 5;