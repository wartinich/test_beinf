import boto3

s3 = boto3.client(
    's3',
    endpoint_url="http://localstack:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)


def upload_file_to_s3(text: str, filename: str) -> str:
    """
    Uploads a file to S3
    :param text: Text to upload
    :param filename: Filename to use
    :return: S3 URL
    """
    bucket_name = "test-bucket"

    create_bucket_if_not_exists(bucket_name)

    s3.put_object(Bucket=bucket_name, Key=filename, Body=text.encode())

    return f"http://localhost:4566/{bucket_name}/{filename}"


def create_bucket_if_not_exists(bucket_name: str):
    """
    Creates a bucket if it doesn't exist
    :param bucket_name: Name of the bucket
    """
    existing_buckets = s3.list_buckets()
    if any(bucket["Name"] == bucket_name for bucket in existing_buckets.get("Buckets", [])):
        print(f"Bucket '{bucket_name}' already exists.")
    else:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")
