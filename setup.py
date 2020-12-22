import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s3-bucket",
    version="1.1.0",
    author="CodeLighthouse",
    author_email="hello@codelighthouse.io",
    description="An easy to use client for S3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeLighthouse/s3-bucket",
    packages=setuptools.find_packages(),
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'boto3'
    ]
)