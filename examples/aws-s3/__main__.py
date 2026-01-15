"""AWS S3 bucket with security defaults example"""
import pulumi
from pullup import aws

# Create an S3 bucket with all security best practices
bucket = aws.storage(name="my-secure-bucket")

# Export the bucket name
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
