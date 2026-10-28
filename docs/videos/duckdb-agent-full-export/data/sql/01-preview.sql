SET autoinstall_known_extensions=false; SET autoload_known_extensions=false; SET threads=1; SET memory_limit='128MB'; CREATE TABLE parcels AS SELECT * FROM read_csv('input/parcels.csv',columns={'parcel_id':'VARCHAR','route':'VARCHAR','promised_days':'INTEGER','status':'VARCHAR','actual_days':'INTEGER'},header=true);
SELECT * FROM parcels ORDER BY parcel_id;
