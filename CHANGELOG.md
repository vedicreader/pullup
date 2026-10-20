# Release notes

<!-- do not remove -->

## 0.0.11

- `gh auth status` gets `/dev/null` as stdin, so it cannot read or change the terminal the app was started from.

## 0.0.10

- Needs vpseasy 0.0.26, cfeasy 0.0.8 and dockeasy 0.0.11: `after_deploy` in the generated `deploy.py` gets vpseasy 0.0.25's `wait_http`, which verifies through the system trust store, so a TLS-inspecting proxy no longer makes it fail; the floor was 0.0.24, which a resolver could still pick
- The generated `deploy.py rollback prev` undoes the last deploy or rollback, and a rollback no longer orphans the newest build

## 0.0.9

- `gheasy_core` is public, for hosts that drive gheasy through pullup; `_gheasy` remains as an alias
- Workflows read YAML through gheasy's public `yaml_instance`, without the fallback to the underscored name
- `EnvStore.unset` reads dockeasy's public `FASTOPS_ENV`
- Needs dockeasy 0.0.10, vpseasy 0.0.24 (which the generated `deploy.py` uses) and cfeasy 0.0.6

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
