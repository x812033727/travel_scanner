SET autoinstall_known_extensions=false;
SET autoload_known_extensions=false;
COPY (
 SELECT * FROM 'demo/output/late-followup.parquet'
 ORDER BY parcel_id
) TO 'demo/output/parquet-readback.csv' (HEADER,DELIMITER ',');
