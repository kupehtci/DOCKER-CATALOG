import os
import boto3
from botocore.exceptions import ClientError

S3_ENDPOINT = os.getenv("SEAWEEDFS_S3_URL", "http://localhost:8333")
ACCESS_KEY = os.getenv("SEAWEEDFS_ACCESS_KEY", "seaweedadmin")
SECRET_KEY = os.getenv("SEAWEEDFS_SECRET_KEY", "Admin123+")
BUCKET = "my-bucket"

s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="us-east-1",  # SeaweedFS generally accepts any region
)

def ensure_bucket(bucket: str) -> None:
    try:
        s3.head_bucket(Bucket=bucket)
    except ClientError:
        s3.create_bucket(Bucket=bucket)

def upload_file(local_path: str, object_key: str, content_type: str | None = None) -> str:
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    s3.upload_file(
        Filename=local_path,
        Bucket=BUCKET,
        Key=object_key,
        ExtraArgs=extra_args,
    )
    return f"{S3_ENDPOINT}/{BUCKET}/{object_key}"

if __name__ == "__main__":
    ensure_bucket(BUCKET)

    # Upload a local file
    url = upload_file(
        local_path="./example.jpg",
        object_key="example.jpg",
        content_type="image/jpg",
    )
    print("Uploaded to:", url)