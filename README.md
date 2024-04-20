# ethereum_max_wei_finder
## Setup
### Setup Postgres database
For macOS - Follow instructions for getting setup [here](https://postgresapp.com)

Your postgres URL will be in the format:
`postgres://{user}@{host}:{port}/{databaseName}`

Ensure your postgres instance is running.
### Packages
Install [poetry](https://python-poetry.org/docs/)

`poetry install`

### Generate QuickNode endpoint
Generate a [quicknode endpoint](https://www.quicknode.com/core-api)

## Running

### Run block crawler
`poetry run python main.py {quickNode endpoint} {postgresURL} {firstBlock}-{secondBlock}`

ex.
```
poetry run python main.py \
https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ \
postgres://williamwilson@localhost:5433/williamwilson \
18908800-18909050
```

ex log response for this command:
```
(base) williamwilson@Williams-MacBook-Pro-9 ethereum_max_wei_finder % poetry run python main.py \
https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ \
postgres://williamwilson@localhost:5433/williamwilson \
18908800-18909050
Populating database...
Database connection created
Database table created if it didn't exist
Populating table...
100%|█████████████████████████████████████████████████████████████████████████| 251/251 [00:45<00:00,  5.48it/s]
Database connection closed
Getting max wei in block range...
Database connection created
[(18909040, Decimal('1539772311888001651587'))]
Database connection closed
Block with block number 18909040 transacted the most wei in the given block range with a total of 1539772311888001651587 wei transacted
```

## Documentation
To generate documentation, run `poetry run pdoc --html ./ --force`

## Decisions
* Postgrese is used as wei can technically reach 128 bits and when adding the wei of a block together, having only 64 bits can cause integer overflow
* The table data storing the blocks is never deleted. Ideally, this should save time in querying a block range that has already been initialized. I didn't add functionality to do this yet, though.
* I used a controller-service pattern. The main service is the block crawler service and it relies on two subservices (ethereum api service and a service to interact with a postgres database). The controllers, invoked through main.py for now but could be transformmed into an API controller itself, are separated into one that populates the database with block info and one that queries that block info.

## TODO
* Creating a DTO for blocks
* Adding types for connection, cursor, all paramaters
* More specific error handling - validating QuickNode URLs
* Implementing a logger - logging levels instead of just print