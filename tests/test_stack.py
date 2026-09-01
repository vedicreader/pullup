"Which of your own packages raised, and where to open it."
from pullup.stack import blame, frames, checkout_for, survey

TB = '''Traceback (most recent call last):
  File "/x/.venv/lib/python3.12/site-packages/nbdev/cli.py", line 10, in main
    run()
  File "/x/.venv/lib/python3.12/site-packages/gheasy/repo.py", line 42, in push
    raise GitError("no upstream")
GitError: no upstream
'''

def test_the_deepest_package_of_yours_is_the_one_blamed():
    "The top of the traceback is whoever called; the bottom is whoever actually raised."
    r = blame(TB, family=['nbdev', 'gheasy'])
    assert r['package'] == 'gheasy' and r['line'] == 42 and r['fn'] == 'push'
    assert r['error'] == 'GitError: no upstream'

def test_a_traceback_with_none_of_your_packages_in_it_still_reports_the_error():
    "A failure in somebody else's code is not a failure to describe."
    r = blame(TB, family=['pullup'])
    assert r['package'] == '' and r['error'] == 'GitError: no upstream'

def test_nothing_at_all_is_answered_with_blanks_not_an_exception():
    assert blame('')['package'] == '' and blame(None)['error'] == ''

def test_frames_reads_a_traceback_in_the_order_the_terminal_printed_it():
    got = frames(TB)
    assert [f['fn'] for f in got] == ['main', 'push'] and got[0]['line'] == 10

def test_an_open_checkout_is_matched_by_what_is_inside_it_not_by_its_folder_name(tmp_path):
    "A repository called `gheasy-fork` still holds the `gheasy` package, and that is what counts."
    root = tmp_path/'gheasy-fork'; (root/'gheasy').mkdir(parents=True)
    (root/'gheasy'/'__init__.py').write_text('')
    assert checkout_for('gheasy', [tmp_path]) == ''
    assert checkout_for('gheasy', [root]) == str(root)
    assert checkout_for('nothere', [root]) == ''

def test_a_src_layout_checkout_is_found_too(tmp_path):
    root = tmp_path/'thing'; (root/'src'/'thing').mkdir(parents=True)
    (root/'src'/'thing'/'__init__.py').write_text('')
    assert checkout_for('thing', [root]) == str(root)

def test_the_blamed_file_is_reopened_in_your_checkout_when_you_have_one(tmp_path):
    """Site-packages is a copy. Pointing an editor at it means editing something a reinstall
    discards, so the checkout wins where the same file exists in it."""
    root = tmp_path/'gheasy'; (root/'gheasy').mkdir(parents=True)
    (root/'gheasy'/'__init__.py').write_text('')
    (root/'gheasy'/'repo.py').write_text('')
    r = blame(TB, checkouts=[root], family=['gheasy'])
    assert r['open'] == str(root/'gheasy'/'repo.py') and r['checkout'] == str(root)
    assert r['file'].startswith('/x/'), 'and the traceback still says where it actually ran'

def test_survey_answers_for_a_package_that_is_not_installed():
    row = next(r for r in survey(family=['definitely_not_installed_xyz']))
    assert row['installed'] is False and row['source'] == '' and row['version'] == ''
