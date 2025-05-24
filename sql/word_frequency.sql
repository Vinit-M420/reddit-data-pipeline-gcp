WITH words AS (
  SELECT
    LOWER(word) AS word
  FROM
    `practical-bolt-460017-e3`.`reddit_dataset`.`reddit_data`,
    UNNEST(SPLIT(LOWER(selftext), ' ')) AS word
  WHERE
    word != '' AND word IS NOT NULL
)

SELECT
  word, LENGTH(word) as word_len,
  COUNT(*) AS frequency
FROM
  words
WHERE LENGTH(word) > 5
GROUP BY
  word
ORDER BY
  frequency DESC
--LIMIT 50
;