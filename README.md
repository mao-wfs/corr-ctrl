# corr-ctrl
Scripts for controlling the MAO correlator


## Installation

```shell
git clone https://github.com/mao-wfs/corr-ctrl.git
cd corr-ctrl
poetry install
```

## Usage

### corr-ctrl

```shell
poetry run bin/corr-ctrl <flags>
```

See the help (`poetry run bin/corr-ctrl --help`) for more details.

## Environment variables

These environment variables must be set before using the scripts.

Name | Description
--- | ---
`CORDATA_DEST` | IP address for receiving data in a client
`CORDATA_SRC` | IP address for sending data in the correlator
`CORDATA_PATH` | Path of the `cordata` command in a client
