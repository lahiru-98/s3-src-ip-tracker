SELECT
  eventtime,
  eventname,
  sourceipaddress,
  useridentity.username,
  requestparameters['bucketName'] as bucketName
FROM
 "aws:cloudtrail"."3e069a99-d2dd-4189-b361-ed8c30852262"
WHERE
  sourceIPAddress LIKE '175.157.28.253'  
  AND eventName IN ('GetObject', 'PutObject', 'ListBucket') 
  AND eventtime >= (current_timestamp - interval '1' hour)
ORDER BY
  eventTime DESC;