# ethereum_max_ether_finder
This project performs blockchain indexing to find the block that has the most transacted ether in a given block range.

## Setup
I use python 3.8.11

`brew install python@3.8.11`

### Setup Postgres database
For macOS - Follow instructions for getting setup [here](https://postgresapp.com)

Your postgres URL will be in the format:
`postgres://{user}@{host}:{port}/{databaseName}`

Ensure your postgres instance is running.

Also, in a terminal, run `brew install postgresql` otherwise the poetry install below will fail.

### Packages
Install [poetry](https://python-poetry.org/docs/)

In `ethereum_max_ether_finder` folder, run `poetry install`

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
(base) williamwilson@Williams-MacBook-Pro-9 ethereum_max_ether_finder % poetry run python main.py \https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ \
postgres://williamwilson@localhost:5433/williamwilson \
18908800-18909050
Populating database...
Database connection created
Database table created if it didn't exist
Populating table...
100%|█████████████████████████████████████████████████████████████| 251/251 [00:49<00:00,  5.08it/s]
Database connection closed
Getting max ether in block range...
Database connection created
Database connection closed
Block with block number 18909040 transacted the most ether in the given block range with a total of 1539.772311888001651587 ether transacted
```

## Documentation
To generate documentation, run `poetry run pdoc --html ./ --force`

This seems to fail on some machines, so the most recent documentation is in the `html` folder.

## Decisions
* Postgrese is used as wei can technically reach 128 bits and when adding the wei of a block together, having only 64 bits can cause integer overflow
* I chose to make the database table have wei instead of ether to align more closely with the api in case any granular operations need to be added in the future. Then, I do a conversion to ether in the block crawler service.
* The table data storing the blocks is never deleted. Ideally, this should save time in querying a block range that has already been initialized. I didn't add functionality to do this yet, though.
* I used a controller-service pattern. The main service is the block crawler service and it relies on two subservices (ethereum api service and a service to interact with a postgres database). The controllers, invoked through main.py for now but could be transformmed into an API controller itself, are separated into one that populates the database with block info and one that queries that block info.

## TODO
* Creating a DTO for blocks
* Adding types for connection, cursor, all paramaters
* Adding parallelization to requests/populating database
* More specific error handling - validating QuickNode URLs, validating if block number exists, validating if there are transactions (early blocks have no transactions and my code doesn't handle that)
* Implementing a logger - logging levels instead of just print; we should be debug logging "Database connection closed" for instance