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
`Poetry`

### Installing

Run `poetry install` to get started.

### Testing

Run `pytest` to start the test suite.
