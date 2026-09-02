"What kind of project a folder holds, and the steps that follow from it."
import pytest
from pullup.project import (Project, Step, app_project, default_steps, fastship_project,
                            maturin_project, nbdev_project, release_flow, rust_project)

def test_an_nbdev_project_is_recognised_by_either_file_it_keeps_its_config_in(tmp_path):
    "nbdev 2 writes settings.ini; a migrated project writes `[tool.nbdev]` instead."
    assert not nbdev_project(tmp_path)
    (tmp_path/'settings.ini').write_text('[DEFAULT]\nlib_name = x\nnbs_path = nbs\n')
    assert nbdev_project(tmp_path) and release_flow(tmp_path) == 'nbdev'
    (tmp_path/'settings.ini').unlink()
    (tmp_path/'pyproject.toml').write_text('[project]\nname = "x"\n\n[tool.nbdev]\n')
    assert nbdev_project(tmp_path), 'a migrated project is still an nbdev project'

def test_a_settings_ini_that_is_not_nbdevs_does_not_claim_the_folder(tmp_path):
    "`[DEFAULT]` alone is any old ini file; nbdev's has its paths in it."
    (tmp_path/'settings.ini').write_text('[DEFAULT]\ncolour = blue\n')
    assert not nbdev_project(tmp_path)

def test_rust_is_asked_before_fastship_because_a_maturin_crate_has_a_pyproject_too(tmp_path):
    """The fastship flow would `ship-pypi` a wheel only the runners can build, so a crate that is
    also a Python package has to be recognised as the crate it is."""
    (tmp_path/'Cargo.toml').write_text('[package]\nname = "x"\n')
    assert rust_project(tmp_path) and release_flow(tmp_path) == 'crate'
    (tmp_path/'pyproject.toml').write_text('[build-system]\nbuild-backend = "maturin"\n')
    assert maturin_project(tmp_path) and release_flow(tmp_path) == 'maturin'
    assert fastship_project(tmp_path), 'it does have a pyproject; the order is what decides'

def test_a_plain_folder_and_a_plain_package_get_the_flows_that_fit_them(tmp_path):
    assert release_flow(tmp_path) == 'plain'
    (tmp_path/'pyproject.toml').write_text('[project]\nname = "x"\n')
    assert release_flow(tmp_path) == 'fastship'

def test_the_app_bundle_lands_after_the_last_publish_and_before_the_bump(tmp_path):
    """`nbdev_bump_version` raises the version for the next cycle, so a bundle built after it
    carries a version nothing was released under."""
    (tmp_path/'settings.ini').write_text('[DEFAULT]\nlib_name = x\nnbs_path = nbs\n')
    assert [s.id for s in default_steps(tmp_path)] == ['prepare', 'bump', 'gh', 'pypi']
    (tmp_path/'setup_app.py').write_text('')
    (tmp_path/'tools').mkdir(); (tmp_path/'tools'/'build_release.py').write_text('')
    assert app_project(tmp_path)
    ids = [s.id for s in default_steps(tmp_path)]
    assert ids == ['prepare', 'bump', 'gh', 'pypi', 'app', 'assets']
    assert ids.index('app') > ids.index('pypi')

def test_a_project_says_what_it_is_without_the_caller_asking_five_questions(tmp_path):
    (tmp_path/'pyproject.toml').write_text('[project]\nname = "x"\n')
    p = Project(tmp_path)
    assert p.kind == 'fastship' and not p.packages_an_app
    assert [s.id for s in p.steps()] == ['test', 'changelog', 'gh', 'pypi', 'bump']
    assert p.dict()['kind'] == 'fastship' and p.dict()['steps'][0]['cmd'].startswith('python -m pytest')

def test_a_caller_can_bring_its_own_flow(tmp_path):
    "`FLOWS` is data, so a project kind pullup does not ship a plan for is still reachable."
    mine = {'plain': [Step('only', 'the one step', 'true', 'nothing else runs')]}
    assert [s.id for s in default_steps(tmp_path, flows=mine)] == ['only']
