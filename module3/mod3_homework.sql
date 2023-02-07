--Question 1: What is count for fhv vehicle records for year 2019?
SELECT COUNT(1) FROM `dtc-de-course-375819.dezoommodule3.fhv_tripdata_external`;


--Question 2: What is the estimated amount of data that will be read when you execute your query on the External Table and the Materialized Table?
SELECT COUNT(DISTINCT(Affiliated_base_number)) FROM `dtc-de-course-375819.dezoommodule3.fhv_tripdata_external`;

SELECT COUNT(DISTINCT(Affiliated_base_number)) FROM `dtc-de-course-375819.dezoommodule3.fhv_tripdata_non_partitioned`;


--Question 3: How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
SELECT COUNT(1) 
FROM `dtc-de-course-375819.dezoommodule3.fhv_tripdata_non_partitioned`
WHERE PUlocationID IS NULL AND DOlocationID IS NULL
;

--Question 4: What is the best strategy to make an optimized table in Big Query if your query will always filter by pickup_datetime and order by affiliated_base_number?

--Question 5:  
-- Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 
-- 03/01/2019 and 03/31/2019 (inclusive)
-- Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table 
-- you created for question 4 and note the estimated bytes processed. What are these values? 

SELECT DISTINCT(Affiliated_base_number) 
--FROM `dtc-de-course-375819.dezoommodule3.fhv_tripdata_non_partitioned`
FROM `dtc-de-course-375819.dezoommodule3.fhv_tripdata_partitioned`
WHERE pickup_datetime >= timestamp('2019-03-01') AND pickup_datetime < timestamp('2019-04-01')
;

-- Question 6: Where is the data stored in the External Table you created?

-- Question 7: It is best practice in Big Query to always cluster your data.
