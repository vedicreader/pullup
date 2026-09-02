"The plan, the state, and a step that actually runs on a pty."
import asyncio, json
import pytest
from pullup.project import Step
from pullup.pipeline import Pipeline, PipelineError, resolve_script, uv_argv

class Steps(Pipeline):
    "A pipeline whose plan is given rather than sniffed from the folder."
    plan = ()
    @classmethod
    def defaults(cls, root): return list(cls.plan)

def mk(tmp_path, steps, **kw):
    Steps.plan = steps
    return Steps(tmp_path, **kw)

def test_the_plan_is_written_where_the_caller_says_and_nowhere_else(tmp_path):
    "A package that wrote into a directory named after one of its callers would be one to fork."
    p = mk(tmp_path, [Step('a', 'a', 'true')], dir='.mine')
    assert p.path == tmp_path/'.mine'/'pipeline.json'
    p.save([{'id': 'b', 'label': 'b', 'cmd': 'false'}])
    assert json.loads(p.path.read_text())['steps'][0]['cmd'] == 'false'
    assert [s.id for s in Steps(tmp_path, dir='.mine').steps] == ['b'], 'and it is read back'
    assert not (tmp_path/'.leela').exists() and not (tmp_path/'.pullup').exists()

def test_a_plan_with_no_command_in_it_is_refused(tmp_path):
    p = mk(tmp_path, [Step('a', 'a', 'true')])
    with pytest.raises(PipelineError, match='at least one step'): p.save([{'id': 'x', 'cmd': '  '}])
    with pytest.raises(PipelineError, match='at least one step'): p.save([])

def test_an_unreadable_plan_falls_back_to_the_default_rather_than_raising(tmp_path):
    "A half-written file is a reason to offer the default plan, not to make the panel unopenable."
    (tmp_path/'.pullup').mkdir()
    (tmp_path/'.pullup'/'pipeline.json').write_text('{ not json')
    assert [s.id for s in mk(tmp_path, [Step('a', 'a', 'true')]).steps] == ['a']

def test_the_state_says_what_ran_what_is_running_and_what_is_still_wanted(tmp_path):
    p = mk(tmp_path, [Step('a', 'a', 'true'), Step('b', 'b', 'true', needs=['NOPE_NOT_SET'])])
    st = p.state()
    assert st['kind'] == 'pipeline' and not st['configured'] and not st['running']
    assert [r['status'] for r in st['steps']] == ['pending', 'pending']
    assert st['needs'] == ['NOPE_NOT_SET'] and st['steps'][1]['missing'] == ['NOPE_NOT_SET']
    assert not st['done'] and st['failed'] == ''
    p.skip('a'); p.skip('b')
    assert p.state()['done'], 'skipped counts as done: it is a decision, not a gap'
    p.reset()
    assert [r['status'] for r in p.state()['steps']] == ['pending', 'pending']

def test_an_unknown_step_is_named_rather_than_silently_skipped(tmp_path):
    p = mk(tmp_path, [Step('a', 'a', 'true')])
    with pytest.raises(PipelineError, match='unknown pipeline step: zzz'): p.step('zzz')

async def test_a_passing_run_walks_the_plan_and_a_failing_one_stops_it(tmp_path):
    """Auto-advance is what makes a release one button. It has to stop at the first failure, or a
    project would publish from a tree whose tests never passed."""
    p = mk(tmp_path, [Step('one', 'one', 'echo first'),
                      Step('two', 'two', 'sh -c "exit 3"'),
                      Step('three', 'three', 'echo never')])
    await p.start()
    for _ in range(200):
        if p.state()['failed']: break
        await asyncio.sleep(.05)
    st = p.state()
    assert st['failed'] == 'two'
    got = {r['id']: (r['status'], r['code']) for r in st['steps']}
    assert got['one'] == ('passed', 0) and got['two'] == ('failed', 3)
    assert got['three'][0] == 'pending', 'the step after a failure must not have run'
    assert 'first' in p.tail() and 'never' not in p.tail()
    assert '❯ echo first' in p.tail(), 'the transcript says which command produced what'

async def test_a_viewer_that_joins_late_is_primed_with_what_it_missed(tmp_path):
    "A browser attaching after a step has scrolled by should still see it."
    p = mk(tmp_path, [Step('one', 'one', 'echo hello-from-the-past')])
    await p.start()
    for _ in range(200):
        if p.state()['steps'][0]['status'] == 'passed': break
        await asyncio.sleep(.05)
    q = p.subscribe()
    assert b'hello-from-the-past' in q.get_nowait()
    p.unsubscribe(q)

async def test_a_second_start_is_refused_while_one_is_running(tmp_path):
    p = mk(tmp_path, [Step('slow', 'slow', 'sleep 5')])
    await p.start()
    with pytest.raises(PipelineError, match='is still running'): await p.start()
    with pytest.raises(PipelineError, match='is still running'): p.reset()
    p.stop()
    assert p.state()['steps'][0]['status'] == 'failed' and not p.state()['running']

async def test_a_step_with_no_command_says_so_instead_of_spawning_a_shell(tmp_path):
    p = mk(tmp_path, [Step('empty', 'empty', '   ')])
    with pytest.raises(PipelineError, match='no command to run'): await p.start()

def test_a_hyphenated_command_is_found_under_either_spelling(tmp_path):
    "nbdev installs `nbdev_export`; the plan spells it `nbdev-export`. Both have to resolve."
    bindir = tmp_path/'bin'; bindir.mkdir()
    (bindir/'my_tool').write_text('#!/bin/sh\n'); (bindir/'my_tool').chmod(0o755)
    argv = resolve_script(['my-tool', '--flag'], python=bindir/'python')
    assert argv[0].endswith('my_tool') and argv[1] == '--flag'
    assert resolve_script(['definitely-not-here'])[0] == 'definitely-not-here', 'unfound is unchanged'

def test_uv_only_claims_a_project_it_actually_owns(tmp_path):
    assert uv_argv(tmp_path, ['pytest']) is None, 'no lock, so not uv'
