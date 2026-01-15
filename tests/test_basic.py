"""Basic tests for pullup modules"""
import pytest


def test_imports():
    """Test that all modules can be imported"""
    from pullup import aws, azure, gcp, hetzner, core
    assert aws is not None
    assert azure is not None
    assert gcp is not None
    assert hetzner is not None
    assert core is not None


def test_aws_exports():
    """Test AWS module exports"""
    from pullup import aws
    assert hasattr(aws, 'storage')
    assert hasattr(aws, 'vpc')
    assert hasattr(aws, 'fargate')
    assert hasattr(aws, 'Fargate')


def test_azure_exports():
    """Test Azure module exports"""
    from pullup import azure
    assert hasattr(azure, 'storage')
    assert hasattr(azure, 'vnet')
    assert hasattr(azure, 'container')


def test_gcp_exports():
    """Test GCP module exports"""
    from pullup import gcp
    assert hasattr(gcp, 'storage')
    assert hasattr(gcp, 'network')
    assert hasattr(gcp, 'cloudrun')


def test_hetzner_exports():
    """Test Hetzner module exports"""
    from pullup import hetzner
    assert hasattr(hetzner, 'volume')
    assert hasattr(hetzner, 'network')
    assert hasattr(hetzner, 'server')


def test_core_exports():
    """Test core module exports"""
    from pullup import core
    assert hasattr(core, 'get_stack_name')
    assert hasattr(core, 'get_project_name')
    assert hasattr(core, 'export')


def test_aws_storage_function():
    """Test AWS storage function signature"""
    from pullup import aws
    import inspect
    sig = inspect.signature(aws.storage)
    params = list(sig.parameters.keys())
    assert 'name' in params
    assert 'versioning' in params
    assert 'encryption' in params
    assert 'public' in params


def test_azure_storage_function():
    """Test Azure storage function signature"""
    from pullup import azure
    import inspect
    sig = inspect.signature(azure.storage)
    params = list(sig.parameters.keys())
    assert 'name' in params
    assert 'resource_group' in params
    assert 'location' in params


def test_gcp_storage_function():
    """Test GCP storage function signature"""
    from pullup import gcp
    import inspect
    sig = inspect.signature(gcp.storage)
    params = list(sig.parameters.keys())
    assert 'name' in params
    assert 'location' in params
    assert 'versioning' in params


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
