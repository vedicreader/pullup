# Release notes

<!-- do not remove -->

## 0.0.8

- The nbdev release flow runs `nbdev-prepare`, `nbdev-bump-version`, `nbdev-release-gh` and `nbdev-pypi`, the commands nbdev 3 installs; the underscore names it ran do not exist there
- The `rust` and `go` workflow presets give their jobs the ids `rust` and `go`, the ids gheasy's builders use, so `needs` reaches them; both were `build`
- The generated `deploy.py` keeps the Cloudflare tunnel on `nuke` unless given `--tunnel`, has a `rollback [tag]` subcommand, and after a deploy waits for the site and purges Cloudflare's cache for the host in `after_deploy`; it needs vpseasy 0.0.23
- The generated `setup.py` pushes no key whose value is empty or the text `None`
- `Deploy.target` also reads each key in lower case, such as `server_name`

## 0.0.7

- `nbdev_job` runs `nbdev-test`, then `nbdev-clean` and `git diff --exit-code`. It ran `nbdev_test` and
  `nbdev_clean --check_all`, which nbdev 3 does not have, so every generated workflow failed.

## 0.0.6
release

## 0.0.5
pullup github, infra workflows

## 0.0.4

- `pullup.env.use_extra` names the extra every message about the cloud half tells the reader to
  install, so a host that ships that half under its own name says so once.
- `pullup.deploy.use_generator` names the tool the generated `setup.py` and `deploy.py` credit.
- `pullup.wfbuild.use_spec_dir` names the directory a workflow's spec is kept in, and `spec_path`,
  `load_spec` and `save_spec` take it as a trailing argument. `Workflows` writes where it says.
- `blame` finds the exception line in an indented tail, such as a traceback nested in pytest's
  output, instead of reporting an empty error.


## 0.0.2




## 0.0.1
Initial skeleton for pullup
