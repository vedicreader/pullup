"Reading a GitHub Actions workflow without running one."
from pullup.workflows import Workflows, levels

def test_jobs_are_arranged_into_the_rows_a_graph_is_drawn_in():
    "Everything that can start now, then what follows it, by longest path."
    jobs = [{'id': 'build', 'needs': []}, {'id': 'test', 'needs': ['build']},
            {'id': 'lint', 'needs': []}, {'id': 'ship', 'needs': ['test', 'lint']}]
    assert levels(jobs) == [['build', 'lint'], ['test'], ['ship']]

def test_a_job_needing_something_that_is_not_there_still_gets_a_row():
    "A workflow naming a job it does not define is a workflow you have to be able to look at."
    assert levels([{'id': 'a', 'needs': ['ghost']}]) == [['a']]

def test_a_cycle_is_drawn_rather_than_hung_on():
    got = levels([{'id': 'a', 'needs': ['b']}, {'id': 'b', 'needs': ['a']}])
    assert got and sorted(sum(got, [])) == ['a', 'b']

def test_a_repository_with_no_workflows_reads_as_empty_not_as_an_error(tmp_path):
    w = Workflows(tmp_path)
    assert w.files() == [] and w.parsed() == []

def test_one_workflow_is_read_into_its_triggers_jobs_and_rows(tmp_path):
    d = tmp_path/'.github'/'workflows'; d.mkdir(parents=True)
    (d/'ci.yml').write_text('''name: CI
on:
  push:
    branches: [main]
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: test
        run: pytest -q
  ship:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo ship
''')
    row = Workflows(tmp_path).parse(d/'ci.yml')
    assert row['error'] == '' and row['name'] == 'CI'
    assert row['dispatchable'], 'a dispatchable workflow is one you can start from a button'
    assert {t['event'] for t in row['triggers']} == {'push', 'workflow_dispatch'}
    assert [j['id'] for j in row['jobs']] == ['build', 'ship']
    assert row['jobs'][1]['needs'] == ['build'] and row['levels'] == [['build'], ['ship']]
    assert [s['name'] for s in row['jobs'][0]['steps']] == ['actions/checkout@v4', 'test']

def test_a_file_that_is_not_a_workflow_reports_why_rather_than_raising(tmp_path):
    d = tmp_path/'.github'/'workflows'; d.mkdir(parents=True)
    (d/'nope.yml').write_text('just a string\n')
    assert Workflows(tmp_path).parse(d/'nope.yml')['error'] == 'this file is not a workflow'

def test_broken_yaml_is_an_error_on_the_row_not_an_exception(tmp_path):
    d = tmp_path/'.github'/'workflows'; d.mkdir(parents=True)
    (d/'bad.yml').write_text('name: [unclosed\n')
    row = Workflows(tmp_path).parse(d/'bad.yml')
    assert row['error'] and row['jobs'] == []
