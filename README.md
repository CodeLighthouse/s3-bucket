
# CodeLighthouse's Python AWS S3 Client

Welcome to CodeLighthouse's official documentation for our python AWS S3 client! If you're looking for guidance on how to install, configure, and use the S3 client, you're in the right place! 

The S3 Client is designed to provide many of the high-level functionalities of Amazon's botocore's S3 resource, without forcing users to decipher botocore's arcane documentation or deal with low-level configuration.

## Overview
Amazon Web Services' botocore API is extremely low-level, and it can be extremely difficult to work with. [AWS S3](https://aws.amazon.com/s3/) (Simple Storage Service) is not complicated - it's object storage. You can `GET`, `PUT`, `DELETE`, and `COPY` objects, with a few other functionalities. Simple, right? Yet for some reason, if you were to print botocore's documentation for the S3 service, you'd come out to about 525 printed pages. 

To develop with S3 faster, we wrote a Python package to abstract away a lot of the overhead and configuration that's required, so that you can focus on developing with S3 faster. Note that this package provides a high-level API that does not allow for some types of low-level management.

## Getting Started

### Installing with pip
Our S3 client is hosted on [PyPi](https://pypi.org/project/s3-bucket), so it couldn't be easier to install:

```
pip install s3-bucket
```

### Configuring the S3 Client
Once you've installed the S3 client, you'll need to configure it with your AWS access key ID and your AWS secret access key. We _strongly_ suggest _not_ hard-coding these values in your code, since doing so can create security vulnerabilities, and is bad practice. Instead, we recommend storing them in environment variables and using the `os` module to fetch them:

```python
import s3_bucket as S3
import os

# get your key data from environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# initialize the package
S3.init(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
```

## Using the S3 Client
The S3 Client API is designed to be logically similar to how AWS structures S3 buckets. Instead of using botocore's `Resource`, `Session`, `Client`, and `Object` APIs, there is one, simple API: the `Bucket` API. 

### The Bucket API

The `Bucket` API is simple, and provides most basic methods you'd want to use for an S3 bucket. Once you've initialized the S3 client with the keys as described in the previous section, you can initialize a `Bucket` object by passing it a bucket name:

```python
bucket = S3.Bucket('your bucket name')

#example
bucket = S3.Bucket('my-website-data')
```

Once you've done that, it's smooth sailing - you can use any of the following methods:

| Method                   | Description     | 
| :----------------------- | :-------------- |
| `bucket.get(key)` | returns a two-tuple containing the `bytes` of the object and a `Dict` containing the object's metadata |
| `bucket.put(key, data, metadata=metadata)` | upload `data` as an object with `key` as the object's key. `data` can be either a `str` type _or_ a `bytes` type. `metadata` is an optional argument that should be a `Dict` containing metadata to store with the object. |
|`bucket.delete(key)` | delete the object in the bucket specified by `key` |
|`bucket.upload_file(local_filepath, key)` | Upload the file specified by `local_filepath` to the bucket with `key` as the object's key. |
|`bucket.download_file(key, local_filepath)` | Download the object specified by `key` from the bucket and store it in the local file `local_filepath`. |

### Custom Exceptions

As I mentioned earlier, the way that botocore raises exceptions is somewhat arcane. Instead of raising different types of exceptions to indicate different types of problems, it throws one type of exception that contains properties that you must use to determine what went wrong. It's really obtuse, and a bad design pattern.

Instead of relying on your client code to decipher botocore's exceptions, I wrote custom exception classes that you can use to handle most common types of S3 errors. 

|Exception         | Cause | Properties |
| :--------------- | :-----| :--------- |
| `BucketException` | The `super` class for all other Bucket exceptions. Can be used to generically catch other exceptions raised by the API. | `bucket`, `message` |
| `NoSuchBucket` | Raised if you try to access a bucket that does not exist. |`bucket`, `key`, `message` | 
| `NoSuchKey` | Raised if you try to access an object that does not exist within an existing bucket. | `bucket`, `key`, `message` | 
| `BucketAccessDenied` | AWS denied access to the bucket you tried to access. It may not exist, or you may not have permission to access it. | `bucket`, `message` |
| `UnknownBucketException` | Botocore threw an exception which this client was not programmed to handle. | `bucket`, `error_code`, `error_message` |

To use these exceptions, you can do the following:
```python
try:
	bucket = S3.Bucket('my-bucket-name') 
	data, metadata = bucket.get('some key')
except S3.Exceptions.NoSuchBucket as e:
	# some error handling here
	pass
```

## Examples
Below we've provided some examples of common use cases for the S3 Client.

### Uploading and downloading files
This example shows how to upload and download files to/from your S3 bucket

```python
import s3_bucket as S3
import os

# get your key data from environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# initialize the package
S3.init(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

# initialize a bucket
my_bucket = S3.Bucket('my-bucket')

# UPLOAD A FILE
my_bucket.upload_file('/tmp/file_to_upload.txt', 'myfile.txt')
my_bucket.download_file('myfile.txt', '/tmp/destination_filename.txt')
```

### Storing and retrieving large blobs of text 
The reason that we originally built this client was to handle storing and retrieving large blobs of JSON data that were way to big to store in my database. The below example shows you how to do that.

```python

import s3_bucket as S3
import os

# get your key data from environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# initialize the package
S3.init(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

# initialize a bucket
my_bucket = S3.bucket('my-bucket')

# some json string
my_json_str = "{'a': 1, 'b': 2}" # an example json string

my_bucket.put('json_data_1', my_json_str)

data, metadata = my_bucket.get('json_data_1')

```