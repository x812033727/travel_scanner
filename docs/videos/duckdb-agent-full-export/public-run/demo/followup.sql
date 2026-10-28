.read demo/setup.sql
DESCRIBE parcels;
SELECT status,count(*) AS records
FROM parcels GROUP BY status ORDER BY status;
SELECT route,count(*) AS delivered_late
FROM parcels
WHERE status='delivered' AND actual_days>promised_days
GROUP BY route ORDER BY route;
COPY (
 SELECT parcel_id,route,promised_days,actual_days,
        actual_days-promised_days AS days_late
 FROM parcels
 WHERE status='delivered' AND actual_days>promised_days
 ORDER BY parcel_id
) TO 'demo/output/late-followup.csv' (HEADER,DELIMITER ',');
COPY (
 SELECT parcel_id,route,promised_days,actual_days,
        actual_days-promised_days AS days_late
 FROM parcels
 WHERE status='delivered' AND actual_days>promised_days
 ORDER BY parcel_id
) TO 'demo/output/late-followup.parquet' (FORMAT PARQUET);
SELECT count(*) AS exported_rows
FROM read_csv('demo/output/late-followup.csv');
