# flightless-pylint-plugin

Custom Pylint Rules from Flightless Ops

## Usage

In your `.pylintrc` add or update the following areas:

```ini
load-plugins=flightless_pylint_plugin

[MESSAGES CONTROL]
enable=no-pytest-skip,
       no-direct-settings-import,
       no-conditionals-in-test,
```

## Development

### Requirements

`Python >= 3.12`
`Invoke`
`Poetry`

### Installing

Run `poetry install` to get started.

### Using Invoke

The following command will show you current available options:

```bash
invoke --list
```

As of writing, the following commands can be used as listed:

```bash
  invoke flake8   # Runs flake8 on the project.
  invoke pylint   # Runs pylint on the project.
  invoke mypy     # Runs mypy on the project.
  invoke lint     # Runs flake8 pylint and mypy on the project in sequence.
  invoke test     # Runs pytest on the project.
  invoke coverage # Runs pytest on the project + coverage reports.
  invoke build    # Builds the project.
  invoke publish  # Will publish the project pending you have configured poetry to be able to.
```
