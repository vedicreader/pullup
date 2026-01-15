# Pullup Quick Start Guide

Get started with Pullup in minutes!

## Installation

```bash
pip install git+https://github.com/Karthik777/pullup.git
```

## Your First Deployment

### 1. Initialize Pulumi

```bash
# Create a new directory
mkdir my-infra && cd my-infra

# Initialize Pulumi project
pulumi new python --name my-infra

# Login to Pulumi (or use local backend)
pulumi login  # or: pulumi login --local
```

### 2. Install Pullup

```bash
pip install git+https://github.com/Karthik777/pullup.git
```

### 3. Deploy Your First Resource

#### AWS S3 Bucket

Create `__main__.py`:

```python
import pulumi
from pullup import aws

# Create a secure S3 bucket
bucket = aws.storage(name="my-app-data")

# Export the bucket name
pulumi.export("bucket_name", bucket.id)
```

Configure AWS credentials and deploy:

```bash
# Set AWS credentials (if not already configured)
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"

# Deploy!
pulumi up
```

#### AWS VPC and Fargate

```python
from pullup import aws

# Create VPC with public/private subnets
network = aws.vpc(name="my-vpc")

# Deploy a containerized app
app = aws.fargate(
    name="my-app",
    image="nginx:latest",
    vpc_config=network,
    port=80
)
app.deploy()

# Export outputs
pulumi.export("vpc_id", network['vpc'].id)
```

#### Azure Storage

```python
from pullup import azure

# Create secure storage account
storage = azure.storage(location="eastus")

pulumi.export("storage_name", storage.name)
```

Configure Azure and deploy:

```bash
# Login to Azure
az login

# Deploy
pulumi up
```

#### GCP Cloud Run

```python
from pullup import gcp

# Deploy a Cloud Run service
service = gcp.cloudrun(
    name="hello-world",
    image="gcr.io/cloudrun/hello",
    location="us-central1"
)

pulumi.export("url", service.statuses[0].url)
```

Configure GCP and deploy:

```bash
# Set GCP project
pulumi config set gcp:project YOUR_PROJECT_ID

# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# Deploy
pulumi up
```

## Key Concepts

### Security by Default

All Pullup resources come with security best practices:

```python
# This bucket has:
# - Versioning enabled
# - Encryption at rest
# - Public access blocked
# - HTTPS required
bucket = aws.storage()
```

### Customization

Override defaults when needed:

```python
# Public bucket (use with caution!)
public_bucket = aws.storage(
    name="my-public-assets",
    public=True,
    versioning=False
)
```

### Composition

Combine resources easily:

```python
# Create VPC
network = aws.vpc()

# Use VPC in Fargate
app = aws.fargate(vpc_config=network)
app.deploy()
```

## Next Steps

- Check out [examples](examples/) for complete projects
- Read the [full documentation](https://Karthik777.github.io/pullup/)
- See [CONTRIBUTING.md](CONTRIBUTING.md) to extend Pullup
- Join discussions for questions

## Cleanup

When done, destroy resources:

```bash
pulumi destroy
pulumi stack rm dev
```

## Common Issues

### Import Errors

Make sure Pulumi providers are installed:

```bash
pip install pulumi pulumi-aws pulumi-azure pulumi-gcp
```

### Authentication Issues

- **AWS**: Configure `~/.aws/credentials` or environment variables
- **Azure**: Run `az login`
- **GCP**: Set `GOOGLE_APPLICATION_CREDENTIALS`

### Resource Naming

Some cloud providers have strict naming rules:
- AWS S3: globally unique, lowercase, no underscores
- Azure Storage: 3-24 chars, lowercase letters and numbers only
- GCP: project-specific naming rules

Pullup handles this automatically, but you can override with `name` parameter.

## Getting Help

- 📖 [Documentation](https://Karthik777.github.io/pullup/)
- 🐛 [Report Issues](https://github.com/Karthik777/pullup/issues)
- 💬 [Discussions](https://github.com/Karthik777/pullup/discussions)
