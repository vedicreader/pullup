# Release notes

<!-- do not remove -->

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
