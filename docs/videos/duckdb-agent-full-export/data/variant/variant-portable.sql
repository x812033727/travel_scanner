-- Portable paths only; derived from the recorded SQL, not rerun during formal preparation.
SET autoinstall_known_extensions=false;
SET autoload_known_extensions=false;
SET threads=1;
SET memory_limit='128MB';
CREATE TABLE parcels AS
SELECT * FROM read_csv('input/parcels.csv',
  columns={'parcel_id':'VARCHAR','route':'VARCHAR',
           'promised_days':'INTEGER','status':'VARCHAR',
           'actual_days':'INTEGER'},header=true);

COPY (
 SELECT parcel_id,route,promised_days,actual_days,
        actual_days-promised_days AS days_late
 FROM parcels
 WHERE status='delivered' AND actual_days>=promised_days
 ORDER BY parcel_id
) TO 'variant/output/due-or-late.csv' (HEADER,DELIMITER ',');
SELECT count(*) AS due_or_late_rows
FROM read_csv('variant/output/due-or-late.csv');
