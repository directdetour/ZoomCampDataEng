Question 1: What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)
*
61635151
61635418
61666551
41856543

```
SELECT COUNT(*) FROM `dtc-de-course-375819.dbt_myoung.fact_trips`
  WHERE EXTRACT(YEAR FROM pickup_datetime) IN (2019,2020)) --61602984


SELECT COUNT(*) FROM `dtc-de-course-375819.production.fact_trips`
  WHERE EXTRACT(YEAR FROM pickup_datetime) IN (2019,2020) 
  --61602986

```


Question 2: What is the distribution between service type filtering by years 2019 and 2020 data as done in the videos . (Yellow/Green)
*
89.9/10.1
94/6
76.3/23.7
99.1/0.9

```
89.8/10.2
```

Question 3: What is the count of records in the model stg_fhv_tripdata after running all models with the test run variable disabled
*
4208599
44384899
57084899
42084899

```
SELECT COUNT(*) FROM `dtc-de-course-375819.production.stg_fhv_tripdata` 
--58159517
```


Question 4: What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled
*
22676490
36678853
22676253
29565253

```
SELECT COUNT(*) FROM `dtc-de-course-375819.production.fact_fhv_trips` 
--25644161
```

Question 5: What is the month with the biggest amount of rides after building a tile for the fact_fhv_trips table
*
March
April
January
December

```
January  
```
[Looker Report PDF: FHV_Trip_Analysis](FHV_Trip_Analysis.pdf)


Your code (link to GitHub or other public code-hosting website). Remember: no code - no scores!
*
Add only one link please. It should be a valid URL starting with "https://"
Learning in public links

```
https://github.com/directdetour/ZoomCampDataEng/tree/main/module4

https://github.com/directdetour/dbt-zoomdata


```

Links to social media posts where you share your progress with others (LinkedIn, Twitter, etc). Use #dezoomcamp tag. The scores for this part will be capped at 7 point. Please make sure the posts are valid URLs starting with "https://"

```
https://twitter.com/ymatty/status/1625278646972735488
https://twitter.com/ymatty/status/1625925276264693798
https://twitter.com/ymatty/status/1625997130866237444
https://twitter.com/ymatty/status/1626361783718903808
https://twitter.com/ymatty/status/1626719584379375617

```
How much time (in hours) did you spend on watching lectures and reading?
Please, write here integer or float number (with 'dot' delimiter) without any extra symbols
```
6
```

How much time (in hours) did you spend on homework?
Please, write here integer or float number (with 'dot' delimiter) without any extra symbols
```
4 
```

Did you have any problems? Do you have any comments or feedback?
```
YES, Too many hours spent trying to get the homework answers to line up to the options. Looking at slack I was not alone!
```