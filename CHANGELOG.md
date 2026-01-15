# Release notes

<!-- do not remove -->

## 0.0.2

### Major Features

This release introduces the complete Pullup package - a functional wrapper over Pulumi for deploying infrastructure.

#### Core Features
- Fastcore-based functional design following fastai coding style
- Security-first approach with best practices as defaults
- Minimal configuration with practical defaults
- Support for AWS, Azure, GCP, and Hetzner Cloud

#### AWS Module (`pullup.aws`)
- `storage()`: S3 bucket with versioning, encryption, and blocked public access
- `vpc()`: VPC with public/private subnets, NAT gateway, and routing
- `fargate()`: ECS Fargate deployment with Docker build/push support

#### Azure Module (`pullup.azure`)
- `storage()`: Storage Account with HTTPS-only, encryption, and TLS 1.2+
- `vnet()`: Virtual Network with subnet management
- `container()`: Container Instance deployment

#### GCP Module (`pullup.gcp`)
- `storage()`: Cloud Storage with versioning and public access prevention
- `network()`: VPC Network with custom subnet support
- `cloudrun()`: Cloud Run service deployment

#### Hetzner Module (`pullup.hetzner`)
- `volume()`: Block storage volumes
- `network()`: Private networks
- `server()`: Server instances

#### Documentation & Examples
- Comprehensive README with usage examples
- Example Pulumi programs for each cloud provider
- Contributing guide for developers
- Full test suite

#### Security
- All resources include security best practices by default
- Encryption at rest and in transit
- Blocked public access by default
- Versioning enabled where applicable
- Minimal permissions
- Secure network configurations


## 0.0.1
Initial skeleton for pullup


