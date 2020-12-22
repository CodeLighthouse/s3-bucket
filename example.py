from s3_bucket import Bucket
import os

# get your key data from environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# initialize the package
Bucket.prepare(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

# initialize a bucket
my_bucket = Bucket('my-bucket')

# some json string
my_json_str = "{'a': 1, 'b': 2}" # an example json string

my_bucket.put('json_data_1', my_json_str)

data, metadata = my_bucket.get('json_data_1')