

-- Query public available table
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;


-- Creating external table referring to gcs path
-- CREATE OR REPLACE EXTERNAL TABLE `taxi-rides-ny.nytaxi.external_yellow_tripdata`
-- OPTIONS (
--   format = 'CSV',
--   uris = ['gs://nyc-tl-data/trip data/yellow_tripdata_2019-*.csv', 'gs://nyc-tl-data/trip data/yellow_tripdata_2020-*.csv']
-- );

CREATE OR REPLACE EXTERNAL TABLE `dtc-de-course-375819.dezoommodule3.fhv_tripdata_external`
OPTIONS (
    format = 'CSV',
    uris = ['gs://de_module3_bucket/fhv_tripdata_2019-*.csv.gz']
);


-- Check yello trip data
--SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata limit 10;
SELECT * FROM dtc-de-course-375819.dezoommodule3.fhv_tripdata_external limit 10;


-- Create a non partitioned table from external table
-- CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_non_partitoned AS
-- SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
CREATE OR REPLACE TABLE dtc-de-course-375819.dezoommodule3.fhv_tripdata_non_partitioned AS
SELECT * FROM dtc-de-course-375819.dezoommodule3.fhv_tripdata_external;


-- Create a partitioned table from external table

CREATE OR REPLACE TABLE dtc-de-course-375819.dezoommodule3.fhv_tripdata_partitioned
PARTITION BY 
  DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS
SELECT * FROM dtc-de-course-375819.dezoommodule3.fhv_tripdata_external;

-- CREATE OR REPLACE TABLE dtc-de-course-375819.dezoommodule3.fhv_tripdata_partitioned_a
-- CLUSTER BY 
--   pickup_datetime, Affiliated_base_number AS
-- SELECT * FROM dtc-de-course-375819.dezoommodule3.fhv_tripdata_external;

-- CREATE OR REPLACE TABLE dtc-de-course-375819.dezoommodule3.fhv_tripdata_partitioned_c
-- PARTITION BY 
--   DATE(pickup_datetime), Affiliated_base_number AS
-- SELECT * FROM dtc-de-course-375819.dezoommodule3.fhv_tripdata_external;

-- CREATE OR REPLACE TABLE dtc-de-course-375819.dezoommodule3.fhv_tripdata_partitioned_d
-- PARTITION BY Affiliated_base_number   
-- CLUSTER BY pickup_datetime AS
-- SELECT * FROM dtc-de-course-375819.dezoommodule3.fhv_tripdata_external;


/*
-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_non_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY total_rows DESC;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitoned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;

-- Query scans 1.1 GB
SELECT count(*) as trips
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;

-- Query scans 864.5 MB
SELECT count(*) as trips
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitoned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;

*/