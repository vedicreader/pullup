#!/usr/bin/env python3
"""
Example usage of the pullup fast.ai-style Pulumi wrapper.

This demonstrates how to use pullup to manage infrastructure without CLI interaction.
"""

from pullup.core import PulumiStack, quick_stack, create_secure_tags, SecurityDefaults
import pulumi


def example_infrastructure():
    """
    Example Pulumi program that defines infrastructure.
    
    In a real scenario, this would create actual cloud resources.
    For this example, we export some outputs.
    
    Example of real infrastructure code (commented out):
    
    # AWS S3 Bucket with security defaults:
    # import pulumi_aws as aws
    # bucket = aws.s3.Bucket("my-bucket",
    #     server_side_encryption_configuration={
    #         "rule": {
    #             "apply_server_side_encryption_by_default": {
    #                 "sse_algorithm": "AES256",
    #             },
    #         },
    #     },
    #     versioning={"enabled": True},
    #     tags=create_secure_tags("prod", "platform-team")
    # )
    # pulumi.export("bucket_name", bucket.id)
    
    # Azure Storage Account with security:
    # import pulumi_azure as azure
    # storage = azure.storage.Account("storage",
    #     resource_group_name="my-rg",
    #     account_tier="Standard",
    #     account_replication_type="GRS",
    #     enable_https_traffic_only=True,
    #     min_tls_version="TLS1_2",
    #     tags=create_secure_tags("prod", "platform-team")
    # )
    # pulumi.export("storage_name", storage.name)
    
    # GCP Cloud Storage Bucket:
    # import pulumi_gcp as gcp
    # bucket = gcp.storage.Bucket("my-bucket",
    #     location="US",
    #     uniform_bucket_level_access=True,
    #     versioning={"enabled": True},
    #     labels=create_secure_tags("prod", "platform-team")
    # )
    # pulumi.export("bucket_url", bucket.url)
    """
    
    # Export some example outputs
    pulumi.export("message", "Infrastructure created successfully!")
    pulumi.export("environment", "development")
    pulumi.export("tags", create_secure_tags("dev", "example-team"))
    pulumi.export("security_settings", SecurityDefaults.storage_encryption())


def example_1_basic_stack():
    """Example 1: Create a stack using the fluent API"""
    print("=" * 60)
    print("Example 1: Basic Stack Creation (Fluent API)")
    print("=" * 60)
    
    # Create and configure a stack with method chaining
    stack = (PulumiStack("dev-example", "pullup-demo")
             .login()
             .setup(example_infrastructure)
             .create_or_select())
    
    print(f"✓ Stack created: {stack.stack_name}")
    print(f"✓ Project: {stack.project_name}")
    print(f"✓ Backend: {stack.backend_url}")
    print()
    
    return stack


def example_2_quick_stack():
    """Example 2: Use the quick_stack helper"""
    print("=" * 60)
    print("Example 2: Quick Stack Helper")
    print("=" * 60)
    
    # Even simpler - one function call
    stack = quick_stack(
        stack_name="quick-example",
        program=example_infrastructure,
        project_name="pullup-demo",
        config={
            "aws:region": "us-west-2",
            "environment": "development"
        },
        auto_deploy=False  # Set to True to deploy immediately
    )
    
    print(f"✓ Quick stack created: {stack.stack_name}")
    print()
    
    return stack


def example_3_security_features():
    """Example 3: Security-first features"""
    print("=" * 60)
    print("Example 3: Security Features")
    print("=" * 60)
    
    # 1. Security tags
    tags = create_secure_tags(
        environment="production",
        owner="platform-team",
        CostCenter="engineering",
        Compliance="SOC2"
    )
    print("Security Tags:")
    for key, value in tags.items():
        print(f"  {key}: {value}")
    print()
    
    # 2. Security defaults
    print("Security Defaults:")
    defaults = SecurityDefaults.all_defaults()
    for category, settings in defaults.items():
        print(f"\n  {category.upper()}:")
        for key, value in settings.items():
            print(f"    ✓ {key}: {value}")
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("PULLUP: Fast.ai-style Pulumi Wrapper Examples")
    print("=" * 60)
    print()
    
    # Example 1: Basic stack creation
    stack1 = example_1_basic_stack()
    
    # Example 2: Quick stack
    stack2 = example_2_quick_stack()
    
    # Example 3: Security features
    example_3_security_features()
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print("✓ All examples completed successfully!")
    print("\nKey Features Demonstrated:")
    print("  • Pythonic API (no CLI required)")
    print("  • Fluent method chaining")
    print("  • Quick helper functions")
    print("  • Automatic security defaults")
    print("  • Standardized tagging")
    print("  • Local file backend (no cloud setup needed)")
    print()
    print("Next Steps:")
    print("  • Use stack.preview() to see changes")
    print("  • Use stack.up() to deploy infrastructure")
    print("  • Use stack.get_outputs() to retrieve outputs")
    print("  • Use stack.destroy() to tear down resources")
    print()


if __name__ == "__main__":
    main()
