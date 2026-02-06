-- iceberg.bronze."data" definition

CREATE TABLE iceberg.bronze.data (
   timestamp timestamp(6) with time zone,
   session_id varchar,
   msisdn varchar,
   apn varchar,
   session_duration_seconds integer,
   bytes_uploaded bigint,
   bytes_downloaded bigint,
   cell_id varchar,
   region varchar,
   session_end_reason varchar,
   charging_amount decimal(10, 2),
   ingestion_date date
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/bronze/data',
   partitioning = ARRAY['day(timestamp)']
);




-- iceberg.bronze.sms definition

CREATE TABLE iceberg.bronze.sms (
   timestamp timestamp(6) with time zone,
   sms_id varchar,
   sender_msisdn varchar,
   receiver_msisdn varchar,
   sms_type varchar,
   message_length integer,
   cell_id varchar,
   region varchar,
   delivery_status varchar,
   charging_amount decimal(10, 2),
   ingestion_date date
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/bronze/sms',
   partitioning = ARRAY['day(timestamp)']
);





-- iceberg.bronze.voice definition

CREATE TABLE iceberg.bronze.voice (
   timestamp timestamp(6) with time zone,
   call_id varchar,
   caller_msisdn varchar,
   callee_msisdn varchar,
   call_type varchar,
   duration_seconds integer,
   cell_id varchar,
   region varchar,
   termination_reason varchar,
   charging_amount decimal(10, 2),
   ingestion_date date
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/bronze/voice',
   partitioning = ARRAY['day(timestamp)']
);




-- iceberg.silver."data" definition

CREATE TABLE iceberg.silver.data (
   timestamp timestamp(6) with time zone,
   session_id varchar,
   session_date date,
   session_hour integer,
   msisdn varchar,
   apn varchar,
   session_duration_seconds integer,
   bytes_uploaded bigint,
   bytes_downloaded bigint,
   session_end_reason varchar,
   cell_id varchar,
   region varchar,
   charging_amount decimal(10, 2),
   ingestion_date date
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/silver/data'
);





-- iceberg.silver.sms definition

CREATE TABLE iceberg.silver.sms (
   timestamp timestamp(6) with time zone,
   sms_date date,
   sms_hour integer,
   sms_id varchar,
   sender_msisdn varchar,
   receiver_msisdn varchar,
   sms_type varchar,
   message_length integer,
   delivery_status varchar,
   cell_id varchar,
   region varchar,
   charging_amount decimal(10, 2),
   ingestion_date date
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/silver/sms'
);





-- iceberg.silver.voice definition

CREATE TABLE iceberg.silver.voice (
   timestamp timestamp(6) with time zone,
   call_date date,
   call_hour integer,
   call_id varchar,
   caller_msisdn varchar,
   callee_msisdn varchar,
   call_type varchar,
   duration_seconds integer,
   duration_minutes double,
   termination_reason varchar,
   call_status varchar,
   region varchar,
   cell_id varchar,
   charging_amount decimal(10, 2),
   ingestion_date date
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/silver/voice'
);






-- iceberg.gold.data_daily_global_kpis definition

CREATE TABLE iceberg.gold.data_daily_global_kpis (
   session_date date,
   total_sessions bigint,
   total_active_sessions bigint,
   average_session_duration_sec double,
   average_session_duration_terminated_sec double,
   total_bytes_uploaded bigint,
   total_bytes_downloaded bigint,
   total_revenue decimal(20, 2),
   average_session_duration_minutes double,
   total_bytes bigint,
   total_data_volume_gb double,
   average_throughput_per_session double
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/gold/data_daily_global_kpis'
);




-- iceberg.gold.data_daily_tower_kpis definition

CREATE TABLE iceberg.gold.data_daily_tower_kpis (
   session_date date,
   session_hour integer,
   cell_id varchar,
   total_sessions bigint,
   total_active_sessions bigint,
   total_bytes_uploaded bigint,
   total_bytes_downloaded bigint,
   total_revenue decimal(20, 2),
   total_bytes bigint,
   total_data_volume_gb double
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/gold/data_daily_tower_kpis'
);






-- iceberg.gold.sms_daily_global_kpis definition

CREATE TABLE iceberg.gold.sms_daily_global_kpis (
   sms_date date,
   total_sms bigint,
   total_delivered_sms bigint,
   total_failed_sms bigint,
   total_revenue decimal(20, 2),
   total_subscribers_sending_sms bigint,
   total_subscribers_receiving_sms bigint
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/gold/sms_daily_global_kpis'
);






-- iceberg.gold.sms_daily_tower_kpis definition

CREATE TABLE iceberg.gold.sms_daily_tower_kpis (
   sms_date date,
   sms_hour integer,
   cell_id varchar,
   total_sms bigint,
   total_delivered_sms bigint,
   total_failed_sms bigint,
   total_revenue decimal(20, 2),
   total_subscribers_sending_sms bigint,
   total_subscribers_receiving_sms bigint
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/gold/sms_daily_tower_kpis'
);





-- iceberg.gold.voice_daily_global_kpis definition

CREATE TABLE iceberg.gold.voice_daily_global_kpis (
   call_date date,
   total_number_calls bigint,
   total_call_duration bigint,
   average_call_duration double,
   average_call_duration_success double,
   total_call_success bigint,
   total_call_failed bigint,
   total_revenue decimal(20, 2),
   total_duration_of_minutes double
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/gold/voice_daily_global_kpis'
);




-- iceberg.gold.voice_daily_tower_kpis definition

CREATE TABLE iceberg.gold.voice_daily_tower_kpis (
   call_date date,
   call_hour integer,
   cell_id varchar,
   total_number_calls bigint,
   total_call_duration bigint,
   total_call_success bigint,
   total_call_failed bigint,
   total_revenue decimal(20, 2)
)
WITH (
   compression_codec = 'ZSTD',
   format = 'PARQUET',
   format_version = 2,
   location = 's3://warehouse/gold/voice_daily_tower_kpis'
);