"""GCP Cloud Run deployment example"""
import pulumi
from pullup import gcp

# Create Cloud Run service
service = gcp.cloudrun(
    name="my-service",
    image="gcr.io/cloudrun/hello",
    location="us-central1"
)

# Export service URL
pulumi.export("service_url", service.statuses[0].url)
