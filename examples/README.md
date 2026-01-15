# Pullup Examples

This directory contains example Pulumi programs using the Pullup library.

## Prerequisites

1. Install Pullup:
```bash
pip install -e ..
```

2. Configure Pulumi:
```bash
# Login to Pulumi
pulumi login

# Or use local backend
pulumi login --local
```

3. Configure cloud provider credentials:
- AWS: Configure AWS CLI or set environment variables
- Azure: Run `az login` or set environment variables
- GCP: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

## Examples

### AWS S3 Bucket

Simple S3 bucket with security defaults (versioning, encryption, blocked public access).

```bash
cd aws-s3
pulumi stack init dev
pulumi up
```

### AWS Fargate

VPC with public/private subnets and Fargate service deployment.

```bash
cd aws-fargate
pulumi stack init dev
pulumi up
```

### Azure Storage

Storage Account with security best practices.

```bash
cd azure-storage
pulumi stack init dev
pulumi config set azure-native:location eastus
pulumi up
```

### GCP Cloud Run

Cloud Run service deployment.

```bash
cd gcp-cloudrun
pulumi stack init dev
pulumi config set gcp:project YOUR_PROJECT_ID
pulumi up
```

## Cleanup

To destroy the infrastructure:

```bash
pulumi destroy
pulumi stack rm dev
```

## Learn More

- [Pullup Documentation](https://Karthik777.github.io/pullup/)
- [Pulumi Documentation](https://www.pulumi.com/docs/)
