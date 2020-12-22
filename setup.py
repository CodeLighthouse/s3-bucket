import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CodeLighthouse_S",
    version="1.0.0",
    author="CodeLighthouse",
    author_email="hello@codelighthouse.io",
    description="CodeLighthouse's AWS S3 client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeLighthouse/aws-s3-client",
    packages=setuptools.find_packages(),
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'botocore',
        'boto3'
    ]
)