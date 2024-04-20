import re
import sys

from src.models.request import BlockCrawlerRequest

def validate_arg_length():
    """Validates three args were passed in.

    Checks to ensure 3 arguments (api endpoint, database link, and block range). Exits the program if not.
    """
    if(len(sys.argv) < 4):
        exit("you must provide a quicknode url, postgres database link, and block range")

def validate_quicknode_endpoint(quicknode_endpoint: str):
    """Validates quicknode url format.

    Checks if the URL passed in is in URL format. Exits the program if not.

    Args:
        quicknode_endpoint: The QuickNode url string.
    """
    #TODO: ensure url is a quicknode url, not just any url
    expression = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    if (not re.search(expression, quicknode_endpoint)):
        exit("URL is not formatted correctly")

def validate_postgres_url(database_url: str):
    """Validates database url format.

    Checks if the database url passed in is in proper postgres format. Exits the program if not.

    Args:
        database_url: The url string.
    """
    expression = "^postgres:\/\/.+@.+:[0-9]+\/.+$"
    if (not re.search(expression, database_url)):
        exit("database url must be in the format `postgres://{user}@{host}:{port}/{database_name}`")

def validate_block_range(block_range: str):
    """Validates block range format.

    Checks if the block range is in proper format (number-number). Exits the program if not.

    Args:
        block_range: The blockrange string.
    """
    expression = "^[0-9]+-[0-9]+$"
    if (not re.search(expression, block_range)):
        exit("block range format is not correct")

def parse_block_range(block_crawler_request: BlockCrawlerRequest):
    """Parses the block range and places the first and last block into request object as int.

    Args:
        block_crawler_request: The request that contains solely the endpoint, block range (not parsed), and database url.
    """
    blocks = block_crawler_request.block_range.split("-")
    blocks[0] = int(blocks[0])
    blocks[1] = int(blocks[1])

    if (blocks[1] < blocks[0]):
        exit("second block number must be greater than or equal to the first")

    block_crawler_request.first_block = blocks[0]
    block_crawler_request.last_block = blocks[1]

    return blocks

def validate_arguments(block_crawler_request: BlockCrawlerRequest):
    """Validates all arguments (api url, database url, and blockrange).

    Checks all arguments to ensure they are valid. Exits the program if not.

    Args:
        block_crawler_request: a request object containing all the sysargs passed into the program
    """
    validate_quicknode_endpoint(block_crawler_request.quicknode_endpoint)
    validate_postgres_url(block_crawler_request.database_url)
    validate_block_range(block_crawler_request.block_range)

def construct_request() -> BlockCrawlerRequest:
    """Validates sysargs length and places sysargs in an object.

    Grabs sysargs and places them in an object.

    Returns:
        block_crawler_request: a request object containing all the sysargs passed into the program
    """
    validate_arg_length()
    quicknode_endpoint: str = sys.argv[1]
    database_url: str = sys.argv[2]
    block_range: str = sys.argv[3]
    return BlockCrawlerRequest(quicknode_endpoint, database_url, block_range)
