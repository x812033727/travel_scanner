-- Author intentionally misspelled actual_days; not claimed AI-generated error.
SET autoinstall_known_extensions=false; SET autoload_known_extensions=false; SET threads=1; SET memory_limit='128MB'; CREATE TABLE parcels AS SELECT * FROM read_csv('input/parcels.csv',columns={'parcel_id':'VARCHAR','route':'VARCHAR','promised_days':'INTEGER','status':'VARCHAR','actual_days':'INTEGER'},header=true);
SELECT parcel_id, actual_day FROM parcels LIMIT 1;
