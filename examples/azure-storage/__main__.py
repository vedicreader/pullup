"""Azure Storage Account example"""
import pulumi
from pullup import azure

# Create storage account with security defaults
storage = azure.storage(location="eastus")

# Export the storage account name
pulumi.export("storage_account_name", storage.name)
pulumi.export("storage_account_id", storage.id)
