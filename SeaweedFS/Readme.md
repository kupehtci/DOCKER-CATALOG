# SeaweedFS

**SeaweedFS** is an open source, distributed storage system designed to store and serve billions of files quickly exposing a S3 compatible object storage, a POSIX filesystem and Iceberg/HDFS-compatible data storage. 

Allows horizontal scaling by adding volume servers. 

## Docker Compose

It starts 5 containers SeaweedFS that together maintain the service, as it consist on:
* Control plane (`master`): Port 9333
  * The `master` coordinates the cluster and knows where volumes are located.
* Data (`volume`): Port 8080
  * The `volume` service stores the actual binary data.
* Metadata (`filer`): Port 8888
  * The `filer` provides filesystem-like metadata and path management
* S3 API (`s3`): Port 8333
  * the `s3` service exposes an AWS S3-compatible API for clients such as AWS SDKs, AWS CLI, `rclone`, `s3cmd` or Boto3.
* Admin UI (`admin`): Port 12535
  * The `admin` service provides a web panel for cluster topology, volumes, file browser, S3 buckets/users and maintenance tasks.

## Project structure

```text
.
├── docker-compose.yml
├── s3.json
└── data/
    ├── master/
    ├── volume/
    └── filer/
```

* `docker-compose.yml`: defines the SeaweedFS services.
* `s3.json`: defines S3 users, credentials and bucket permissions.
* `data/`: persistent storage used by the `master`, `volume` and `filer` services.

### Python example

Under `example_upload` you can find `UploadToS3.py` python file that uploads the example image into `my-bucket` and in case it doesn´t exists, create the bucket. 

## Configuration

Create a `s3.json` file with the S3 identities and permissions:

```json
{
  "identities": [
    {
      "name": "admin",
      "credentials": [
        {
          "accessKey": "seaweedadmin",
          "secretKey": "CHANGE_ME_ADMIN_SECRET"
        }
      ],
      "actions": ["Admin"]
    },
    {
      "name": "app",
      "credentials": [
        {
          "accessKey": "myapp",
          "secretKey": "CHANGE_ME_APP_SECRET"
        }
      ],
      "actions": [
        "Read:imagenes",
        "Write:imagenes"
      ]
    }
  ]
}
```

> **Important:** Replace the access keys and secret keys before deploying. Do not commit real credentials to source control.

The `admin` identity has full administrative permissions. The `app` identity can only read and write objects inside the `imagenes` bucket.

## Deployment

Create the required data directories:

```bash
mkdir -p data/master data/volume data/filer data/admin
```

Create a `.env` file with the admin panel credentials (see `.env.example`):

```bash
cp .env.example .env
# edit SEAWEED_ADMIN_PASSWORD
```

Start the stack:

```bash
docker compose up -d
```

Check the status:

```bash
docker compose ps
```

Follow the S3 gateway logs:

```bash
docker compose logs -f s3
```

Once running, the S3 endpoint is available at:

```text
http://localhost:8333
```

The admin panel is available at `http://localhost:12535` (login with `SEAWEED_ADMIN_USER` / `SEAWEED_ADMIN_PASSWORD`).

## Usage

### Create a bucket

Using the AWS CLI:

```bash
export AWS_ACCESS_KEY_ID=seaweedadmin
export AWS_SECRET_ACCESS_KEY='CHANGE_ME_ADMIN_SECRET'
export AWS_DEFAULT_REGION=us-east-1

aws --endpoint-url http://localhost:8333 s3 mb s3://imagenes
```

### Upload a file

```bash
aws --endpoint-url http://localhost:8333 s3 cp \
  ./photo.jpg \
  s3://imagenes/products/photo.jpg
```

### List objects

```bash
aws --endpoint-url http://localhost:8333 s3 ls s3://imagenes --recursive
```

### Download a file

```bash
aws --endpoint-url http://localhost:8333 s3 cp \
  s3://imagenes/products/photo.jpg \
  ./downloaded-photo.jpg
```

## Using `mc`

Alternatively, use the MinIO Client (`mc`):

```bash
mc alias set seaweed \
  http://localhost:8333 \
  seaweedadmin \
  'CHANGE_ME_ADMIN_SECRET'

mc mb seaweed/imagenes
mc cp ./photo.jpg seaweed/imagenes/products/photo.jpg
mc ls --recursive seaweed/imagenes
```

## .NET example

```csharp
using Amazon.S3;
using Amazon.S3.Model;
using Amazon.Runtime;

var s3Client = new AmazonS3Client(
    new BasicAWSCredentials("myapp", "CHANGE_ME_APP_SECRET"),
    new AmazonS3Config
    {
        ServiceURL = "http://localhost:8333",
        ForcePathStyle = true
    });

await using var stream = File.OpenRead("photo.jpg");

await s3Client.PutObjectAsync(new PutObjectRequest
{
    BucketName = "imagenes",
    Key = $"products/{Guid.NewGuid()}.jpg",
    InputStream = stream,
    ContentType = "image/jpeg"
});
```

`ForcePathStyle = true` is required for path-style S3 requests against a local SeaweedFS endpoint.

## Persistence

The Docker Compose file uses bind mounts to persist data on the host:

```yaml
volumes:
  - ./data/master:/data
  - ./data/volume:/data
  - ./data/filer:/data
```

Running `docker compose down` stops and removes the containers but preserves the data in the `data/` directory.

To stop the stack:

```bash
docker compose down
```

To remove containers and delete the local data directories manually:

```bash
docker compose down
rm -rf ./data
```

## Scaling notes

This Compose file is intended for a **single-node deployment**. It uses:

```text
-defaultReplicaPlacement=000
```

This means objects are stored without replication, which is acceptable for local development but not for production.

For a production deployment:

* Run multiple `volume` servers.
* Use a replication placement such as `010` or `100`.
* Run an odd number of `master` nodes for Raft quorum.
* Use persistent volumes backed by reliable storage.
* Put the S3 gateway behind a reverse proxy or load balancer with TLS.
* Restrict access to `master`, `volume` and `filer` ports.

## Security recommendations

* Do not expose the `master`, `volume` or `filer` ports publicly.
* Publish only the S3 API port (`8333`) through a reverse proxy.
* Enable TLS at the reverse proxy or ingress layer.
* Use separate S3 identities with least-privilege permissions.
* Store credentials in Docker secrets, Kubernetes Secrets, Vault or another secret manager.
* Enable backups for the `filer` metadata and `volume` data directories.

## Useful commands

```bash
# Start all services
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f master
docker compose logs -f volume
docker compose logs -f filer
docker compose logs -f s3
docker compose logs -f admin

# Restart a single service
docker compose restart s3

# Stop all services
docker compose down
```
