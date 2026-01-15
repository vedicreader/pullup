"""AWS VPC and Fargate deployment example"""
import pulumi
from pullup import aws

# Create VPC with public/private subnets
network = aws.vpc(name="my-vpc", azs=2)

# Create Fargate cluster from Docker image
cluster = aws.fargate(
    name="my-app",
    image="nginx:latest",
    vpc_config=network,
    port=80
)

# Deploy the cluster
cluster.deploy()

# Export outputs
pulumi.export("vpc_id", network['vpc'].id)
pulumi.export("public_subnets", [s.id for s in network['public_subnets']])
