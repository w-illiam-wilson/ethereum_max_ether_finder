# ethereum_max_wei_finder
## Installation
`poetry install`

## Running
poetry run python main.py https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ test.sqlite3 18908800-18909050

## TODO
change database backing; sqlite only supports 64 bit ints and wei can be up to 128