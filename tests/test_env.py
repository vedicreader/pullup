"The environment a project's commands run in."
import os
from pathlib import Path
import pytest
from pullup.env import BUNDLE_ONLY, EnvStore, clean_env, env_value, strip_bundle, venv_env
from pullup.deploy import Deploy
from pullup.drive import Drive

def test_outside_a_bundle_the_environment_is_handed_back_untouched():
    "A caller that claimed nothing about an environment still claims nothing."
    given = {'PYTHONHOME': '/somewhere', 'PATH': '/bin'}
    assert strip_bundle(dict(given), frozen=False) == given

def test_inside_one_the_hosts_interpreter_redirection_is_dropped():
    """py2app points PYTHONHOME at the bundle. A child that keeps it imports the bundle's standard
    library under another interpreter and dies somewhere that names nothing to do with the cause."""
    out = strip_bundle({n: 'x' for n in BUNDLE_ONLY} | {'PATH': '/bin'}, frozen=True)
    assert not (set(out) & set(BUNDLE_ONLY)) and out['PATH'] == '/bin'
    assert out['PYTHONUTF8'] == '1'

def test_naming_an_interpreter_puts_its_environment_in_front(tmp_path):
    venv = tmp_path/'.venv'; (venv/'bin').mkdir(parents=True)
    py = venv/'bin'/'python'; py.write_text('')
    env = venv_env(py, env={'PATH': '/usr/bin', 'UV_PROJECT_ENVIRONMENT': '/elsewhere'})
    assert env['VIRTUAL_ENV'] == str(venv)
    assert env['PATH'].startswith(str(venv/'bin') + os.pathsep)
    assert 'UV_PROJECT_ENVIRONMENT' not in env, 'it is read where the process ends up, not here'
    assert 'PYTHONHOME' not in env

def test_naming_no_interpreter_still_gives_a_usable_environment():
    assert venv_env(None, env={'PATH': '/bin'}) == {'PATH': '/bin'}
    assert 'PATH' in venv_env()

def test_a_value_that_cannot_be_read_falls_back_rather_than_raising():
    "A missing dockeasy is a reason to use the default, not to fail the step that wanted it."
    class Broken:
        def get(self, key, secret=False): raise RuntimeError('no store here')
    assert env_value(Broken(), 'ANYTHING', 'fallback') == 'fallback'
    assert env_value(Broken(), 'ANYTHING') == ''

def test_a_store_with_no_dockeasy_says_which_extra_installs_it():
    with pytest.raises(Exception, match='pullup'):
        EnvStore().get('SOMETHING') if not _dockeasy_installed() else pytest.skip('dockeasy is here')

def _dockeasy_installed():
    from importlib.util import find_spec
    try: return find_spec('dockeasy') is not None
    except (ImportError, ValueError): return False

def test_every_pipeline_kind_writes_under_the_directory_it_was_given(tmp_path):
    "Three kinds, one rule: the caller names the folder, and nothing writes outside it."
    for kind, name in ((Deploy, 'deploy.json'), (Drive, 'drive.json')):
        p = kind(tmp_path, dir='.somewhere')
        assert p.path == tmp_path/'.somewhere'/name
