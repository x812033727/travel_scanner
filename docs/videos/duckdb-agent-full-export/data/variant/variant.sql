.read demo/setup.sql
COPY (
 SELECT parcel_id,route,promised_days,actual_days,
        actual_days-promised_days AS days_late
 FROM parcels
 WHERE status='delivered' AND actual_days>=promised_days
 ORDER BY parcel_id
) TO 'demo/output/due-or-late.csv' (HEADER,DELIMITER ',');
SELECT count(*) AS due_or_late_rows
FROM read_csv('demo/output/due-or-late.csv');
