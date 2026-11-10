"The nbdev release step runs without an editor or a question, and waits for notes when there are none."
import asyncio, json, os
import pytest
from fastcore.all import Path
from pullup.project import Step
from pullup.pipeline import (Pipeline, PipelineError, Release, changelog_state, claim_unreleased,
    notes_step, project_version, quiet, write_changelog)

MARK = '<!-- do not remove -->\n'

def nbdev_root(tmp_path, version='0.2.0', changelog=None):
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path/'settings.ini').write_text(f'[DEFAULT]\nlib_name = demo\nnbs_path = nbs\nversion = {version}\n')
    if changelog is not None: (tmp_path/'CHANGELOG.md').write_text(changelog)
    return tmp_path

def fake_release(tmp_path):
    "A stand-in for nbdev-release-gh that records what it was given. It cannot reach the real one."
    bin = tmp_path/'fakebin'; bin.mkdir()
    exe = bin/'nbdev-release-gh'
    exe.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$OUT/args.txt"\nprintf "%s\\n" "$TERM" > "$OUT/term.txt"\n')
    exe.chmod(0o755)
    return bin/'python'

async def settle(p):
    for _ in range(200):
        if not p.active: return p.state()
        await asyncio.sleep(.05)
    raise AssertionError('never finished')

def test_the_version_comes_from_settings_ini_then_pyproject(tmp_path):
    assert project_version(nbdev_root(tmp_path/'a', '1.2.3')) == '1.2.3'
    (tmp_path/'b').mkdir(); (tmp_path/'b'/'pyproject.toml').write_text('[project]\nname = "x"\nversion = "4.5.6"\n')
    assert project_version(tmp_path/'b') == '4.5.6'
    assert project_version(tmp_path/'nothing') == ''

def test_an_entry_for_the_version_is_found(tmp_path):
    root = nbdev_root(tmp_path, changelog=f'# Release notes\n\n{MARK}\n## 0.2.0\n\n- new\n\n## 0.1.0\n\n- old\n')
    st = changelog_state(root)
    assert st['has'] and st['kind'] == 'version' and st['version'] == '0.2.0'

def test_a_filled_unreleased_section_counts_and_an_empty_one_does_not(tmp_path):
    root = nbdev_root(tmp_path, changelog=f'# Release notes\n\n{MARK}\n## Unreleased\n\n- new\n\n## 0.1.0\n\n- old\n')
    assert changelog_state(root)['kind'] == 'unreleased'
    (root/'CHANGELOG.md').write_text(f'# Release notes\n\n{MARK}\n## Unreleased\n\n\n## 0.1.0\n\n- old\n')
    assert not changelog_state(root)['has']

def test_a_missing_file_and_an_absent_version_have_no_entry(tmp_path):
    root = nbdev_root(tmp_path)
    st = changelog_state(root)
    assert not st['has'] and st['heading'] == '## 0.2.0' and st['version'] == '0.2.0'
    (root/'CHANGELOG.md').write_text(f'{MARK}\n## 0.1.0\n\n- old\n')
    assert not changelog_state(root)['has'], 'the first section is the old release, and nbdev would publish that'
    (root/'CHANGELOG.md').write_text(f'{MARK}\n## 0.2.0\n\n')
    assert not changelog_state(root)['has'], 'a heading with nothing under it is not notes'
    (root/'CHANGELOG.md').write_text(f'{MARK}\n## 0.2.01\n\n- other\n')
    assert not changelog_state(root)['has'], '0.2.01 is not 0.2.0'

def test_claiming_unreleased_renames_the_heading_only(tmp_path):
    root = nbdev_root(tmp_path, changelog=f'{MARK}\n## Unreleased\n\n- new\n\n## 0.1.0\n\n- old\n')
    assert claim_unreleased(root, '0.2.0') == root/'CHANGELOG.md'
    assert (root/'CHANGELOG.md').read_text() == f'{MARK}\n## 0.2.0\n\n- new\n\n## 0.1.0\n\n- old\n'
    assert claim_unreleased(root, '0.2.0') is None

def test_notes_go_after_nbdevs_marker_and_before_older_entries(tmp_path):
    root = nbdev_root(tmp_path, changelog=f'# Release notes\n\n{MARK}\n## 0.1.0\n\n- old\n')
    path = write_changelog(root, '0.2.0', '- new')
    assert path == root/'CHANGELOG.md'
    assert path.read_text() == f'# Release notes\n\n{MARK}\n## 0.2.0\n\n- new\n\n## 0.1.0\n\n- old\n'
    assert changelog_state(root)['has']

def test_notes_for_a_file_that_is_missing_or_has_no_marker(tmp_path):
    root = nbdev_root(tmp_path)
    assert write_changelog(root, '0.2.0', '- new').read_text() == f'# Release notes\n\n{MARK}\n## 0.2.0\n\n- new\n'
    other = tmp_path/'other'; other.mkdir()
    (other/'CHANGELOG.md').write_text('# Changes\n\n## Unreleased\n\n\n## 0.1.0\n\n- old\n')
    assert write_changelog(other, '0.2.0', '- new').read_text().startswith('# Changes\n\n## 0.2.0\n\n- new\n\n## ')
    bare = tmp_path/'bare'; bare.mkdir(); (bare/'CHANGELOG.md').write_text('# Changes\n')
    assert write_changelog(bare, '0.2.0', '- new').read_text() == '# Changes\n\n## 0.2.0\n\n- new\n'

def test_writing_the_same_notes_twice_changes_nothing_and_new_notes_replace(tmp_path):
    root = nbdev_root(tmp_path, changelog=f'# Release notes\n\n{MARK}\n## 0.1.0\n\n- old\n')
    first = write_changelog(root, '0.2.0', '- new').read_text()
    assert write_changelog(root, '0.2.0', '- new').read_text() == first
    again = write_changelog(root, '0.2.0', '- better').read_text()
    assert '- better' in again and '- new' not in again and again.count('## 0.2.0') == 1 and '- old' in again

def test_empty_notes_and_a_missing_version_are_refused(tmp_path):
    root = nbdev_root(tmp_path)
    with pytest.raises(PipelineError, match='empty'): write_changelog(root, '0.2.0', '  \n ')
    with pytest.raises(PipelineError, match='no version'): write_changelog(root, '', '- x')
    assert not (root/'CHANGELOG.md').exists()

def test_only_the_bare_nbdev_command_is_rewritten(tmp_path):
    assert notes_step(Step('gh', 'x', 'nbdev-release-gh')) and notes_step(Step('gh', 'x', ' nbdev_release_gh '))
    assert not notes_step(Step('gh', 'x', 'nbdev-release-gh --token abc'))
    assert not notes_step(Step('gh', 'x', 'nbdev-release-gh', argv=['nbdev-release-gh']))
    assert not notes_step(Step('gh', 'x', 'ship-gh --no_changelog --no_editor --yes'))
    assert quiet('nbdev-release-gh') == 'nbdev-release-gh --no-changelog --no-editor --yes'

async def test_with_an_entry_the_step_runs_with_the_three_flags_and_a_terminal_type(tmp_path, monkeypatch):
    root = nbdev_root(tmp_path/'proj')
    write_changelog(root, '0.2.0', '- new')
    monkeypatch.delenv('TERM', raising=False); monkeypatch.setenv('OUT', str(tmp_path))
    r = Release(root, python=fake_release(tmp_path), dir='.pullup')
    await r.start('gh', auto=False)
    st = await settle(r)
    row = next(x for x in st['steps'] if x['id'] == 'gh')
    assert row['status'] == 'passed' and st['notes'] is None
    assert (tmp_path/'args.txt').read_text().split() == ['--no-changelog', '--no-editor', '--yes']
    assert (tmp_path/'term.txt').read_text().strip() == 'xterm-256color'
    assert row['cmd'] == 'nbdev-release-gh', 'the plan keeps the command the person reads'
    assert '--no-editor' in r.tail()

async def test_a_filled_unreleased_section_is_renamed_before_the_step_runs(tmp_path, monkeypatch):
    (tmp_path/'proj').mkdir()
    root = nbdev_root(tmp_path/'proj', changelog=f'{MARK}\n## Unreleased\n\n- new\n')
    monkeypatch.setenv('OUT', str(tmp_path))
    r = Release(root, python=fake_release(tmp_path))
    await r.start('gh', auto=False); await settle(r)
    assert '## 0.2.0' in (root/'CHANGELOG.md').read_text() and 'Unreleased' not in (root/'CHANGELOG.md').read_text()

async def test_with_no_entry_the_step_does_not_run_and_says_what_it_needs(tmp_path, monkeypatch):
    (tmp_path/'proj').mkdir()
    root = nbdev_root(tmp_path/'proj', changelog=f'{MARK}\n## 0.1.0\n\n- old\n')
    monkeypatch.setenv('OUT', str(tmp_path))
    r = Release(root, python=fake_release(tmp_path))
    st = await r.start('gh', auto=True)
    assert not (tmp_path/'args.txt').exists(), 'nothing ran'
    row = next(x for x in st['steps'] if x['id'] == 'gh')
    assert row['status'] == 'needs_notes' and not st['running'] and st['failed'] == ''
    assert st['notes']['version'] == '0.2.0' and st['notes']['heading'] == '## 0.2.0'
    assert next(x for x in st['steps'] if x['id'] == 'pypi')['status'] == 'pending'
    write_changelog(root, '0.2.0', '- new')
    await r.start('gh', auto=False)
    await settle(r)
    assert r.state()['notes'] is None and (tmp_path/'args.txt').exists(), 'a retry looks at the file again'

async def test_skipping_a_step_that_waits_for_notes_still_works(tmp_path):
    (tmp_path/'proj').mkdir()
    r = Release(nbdev_root(tmp_path/'proj'))
    await r.start('gh', auto=False)
    assert r.state()['notes']
    st = r.skip('gh')
    assert next(x for x in st['steps'] if x['id'] == 'gh')['status'] == 'skipped' and st['notes'] is None

async def test_a_release_json_override_is_left_as_written(tmp_path, monkeypatch):
    (tmp_path/'proj').mkdir()
    root = nbdev_root(tmp_path/'proj')
    (root/'.pullup').mkdir()
    (root/'.pullup'/'release.json').write_text(json.dumps({'steps': [
        {'id': 'gh', 'label': 'mine', 'cmd': 'nbdev-release-gh --token abc'}]}))
    monkeypatch.setenv('OUT', str(tmp_path))
    r = Release(root, python=fake_release(tmp_path))
    await r.start('gh', auto=False); await settle(r)
    assert (tmp_path/'args.txt').read_text().split() == ['--token', 'abc'], 'no flags added, no notes asked for'
    assert r.state()['notes'] is None

async def test_every_pipeline_step_gets_a_terminal_type(tmp_path, monkeypatch):
    monkeypatch.delenv('TERM', raising=False)
    p = Pipeline(tmp_path, dir='.p')
    assert p._env()['TERM'] == 'xterm-256color'
    monkeypatch.setenv('TERM', 'dumb')
    assert p._env()['TERM'] == 'xterm-256color'
    monkeypatch.setenv('TERM', 'screen')
    assert p._env()['TERM'] == 'screen', 'a real value stays'
