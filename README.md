# ethereum_max_wei_finder
## Installation
`brew install postgresql`

`poetry install`

## Running

### Start database
For macOS - Follow instructions for getting setup [here](https://postgresapp.com)

Your postgres URL will be in the format:
`postgres://{user}@{host}:{port}/{databaseName}`

Ensure your postgres instance is running.

### Run block crawler
`poetry run python main.py https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ {postgresURL} 18908800-18909050`

ex. `poetry run python main.py https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ postgres://williamwilson@localhost:5433/williamwilson 18908800-18909050`

### Documentation
To generate documentation, run `poetry run pdoc --html src`

## TODO
change database backing; sqlite only supports 64 bit ints and wei can be up to 128