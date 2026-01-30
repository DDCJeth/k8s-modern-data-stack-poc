
CREATE NAMESPACE IF NOT EXISTS cdr;

CREATE TABLE IF NOT EXISTS cdr.voice_logs (
    `timestamp`            TIMESTAMP,
    call_id                STRING,
    caller_msisdn           STRING,
    callee_msisdn           STRING,
    call_type               STRING,
    duration_seconds        INT,
    cell_id                 STRING,
    region                  STRING,
    termination_reason      STRING,
    charging_amount         DECIMAL(10,2),
    ingestion_date          DATE
)
USING iceberg
PARTITIONED BY (days(`timestamp`));



CREATE TABLE IF NOT EXISTS cdr.sms_logs (
    `timestamp`        TIMESTAMP,
    sms_id             STRING,
    sender_msisdn       STRING,
    receiver_msisdn     STRING,
    sms_type            STRING,
    message_length      INT,
    cell_id             STRING,
    region              STRING,
    delivery_status     STRING,
    charging_amount     DECIMAL(10,2),
    ingestion_date      DATE
)
USING iceberg
PARTITIONED BY (days(`timestamp`));




CREATE TABLE IF NOT EXISTS cdr.data_logs (
    `timestamp`                 TIMESTAMP,
    session_id                  STRING,
    msisdn                      STRING,
    apn                         STRING,
    session_duration_seconds    INT,
    bytes_uploaded              BIGINT,
    bytes_downloaded            BIGINT,
    cell_id                     STRING,
    region                      STRING,
    session_end_reason          STRING,
    charging_amount             DECIMAL(10,2),
    ingestion_date              DATE
)
USING iceberg
PARTITIONED BY (days(`timestamp`));