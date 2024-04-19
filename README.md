# ethereum_max_wei_finder
## Setup
### Setup Postgres database
For macOS - Follow instructions for getting setup [here](https://postgresapp.com)

Your postgres URL will be in the format:
`postgres://{user}@{host}:{port}/{databaseName}`

Ensure your postgres instance is running.
### Packages
`brew install postgresql`

`poetry install`

### Generate QuickNode endpoint
Generate a [quicknode endpoint](https://www.quicknode.com/core-api)

## Running

### Run block crawler
`poetry run python main.py {quickNode endpoint} {postgresURL} {firstBlock}-{secondBlock}`

ex. `poetry run python main.py https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ postgres://williamwilson@localhost:5433/williamwilson 18908800-18909050`

## Documentation
To generate documentation, run `poetry run pdoc --html ./ --force`

## Decisions
* Postgrese is used as wei can technically reach 128 bits and when adding the wei of a block together, having only 64 bits can cause integer overflow
* The table data storing the blocks is never deleted. Ideally, this should save time in querying a block range that has already been initialized. I didn't add functionality to do this yet, though.
* I used a controller-service pattern. The main service is the block crawler service and it relies on two subservices (ethereum api service and a service to interact with a postgres database). The controllers, invoked through main.py for now but could be transformmed into an API controller itself, are separated into one that populates the database with block info and one that queries that block info.