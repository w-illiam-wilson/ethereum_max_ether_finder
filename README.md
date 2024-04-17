# ethereum_max_wei_finder
## Installation
`brew install postgresql`

`poetry install`

## Running

### Start database
`initdb ./database`

`pg_ctl -D ./database -l logfile start`

### Run block crawler
poetry run python main.py https://magical-thrumming-needle.quiknode.pro/f43cee9d3c566de8afb1e03e948fc3dcaab7462b/ {url of db} 18908800-18909050

## TODO
change database backing; sqlite only supports 64 bit ints and wei can be up to 128