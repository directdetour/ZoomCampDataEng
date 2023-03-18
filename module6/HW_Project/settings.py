import pyspark.sql.types as T

# INPUT_DATA_PATH = '../../resources/rides.csv'
INPUT_DATA_PATH_FHV = 'fhv_tripdata_2019-01.csv'
INPUT_DATA_PATH_GREEN = 'green_tripdata_2019-01.csv'

BOOTSTRAP_SERVERS = 'localhost:9092'

# TOPIC_WINDOWED_VENDOR_ID_COUNT = 'vendor_counts_windowed'
TOPIC_WINDOWED_PICKUP_LOC_ID_COUNT = 'pickup_counts_windowed'


PRODUCE_TOPIC_RIDES_CSV = CONSUME_TOPIC_RIDES_CSV = 'rides_csv'

RIDE_SCHEMA = T.StructType(
    [T.StructField('pickup_datetime', T.TimestampType()),
     T.StructField('dropoff_datetime', T.TimestampType()),
     T.StructField("pickup_loc_id", T.IntegerType()),
     T.StructField("dropoff_loc_id", T.IntegerType())
     ])
