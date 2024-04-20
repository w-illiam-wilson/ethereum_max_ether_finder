import re
import sys

from src.models.request import BlockCrawlerRequest

def validateArgLength():
    """Validates three args were passed in.

    Checks to ensure 3 arguments (api endpoint, database link, and block range). Exits the program if not.
    """
    if(len(sys.argv) < 4):
        exit("you must provide a quicknode url, database link, and block range")

def validateURL(endpoint: str):
    """Validates url format.

    Checks if the URL passed in is in URL format. Exits the program if not.

    Args:
        endpoint: The url string.
    """
    #TODO: ensure url is a quicknode url, not just any url
    expression = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    if (not re.search(expression, endpoint)):
        exit("URL is not correct")

def validatePostgresURL(database: str):
    """Validates database url format.

    Checks if the database url passed in is in proper postgres format. Exits the program if not.

    Args:
        database: The url string.
    """
    expression = "^postgres:\/\/.+@.+:[0-9]+\/.+$"
    if (not re.search(expression, database)):
        exit("database url must be in the format `postgres://{user}@{host}:{port}/{databaseName}`")

def validateBlockRange(block_range: str) -> list:
    """Validates block range format.

    Checks if the block range is in proper format (number-number). Exits the program if not.

    Args:
        block_range: The blockrange string.
    """
    expression = "^[0-9]+-[0-9]+$"
    if (not re.search(expression, block_range)):
        exit("block range format is not correct")

def populateBlockRange(block_crawler_request: BlockCrawlerRequest):
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

def validateArguments(block_crawler_request: BlockCrawlerRequest):
    """Validates all arguments (api url, database url, and blockrange).

    Checks all arguments to ensure they are valid. Exits the program if not.

    Args:
        block_crawler_request: a request object containing all the sysargs passed into the program
    """
    validateArgLength()
    validateURL(block_crawler_request.endpoint)
    validatePostgresURL(block_crawler_request.database_url)
    validateBlockRange(block_crawler_request.block_range)

def constructRequest() -> BlockCrawlerRequest:
    """Places sysargs in an object.

    Grabs sysargs and places them in an object. This does not validate the sysargs exist.

    Returns:
        block_crawler_request: a request object containing all the sysargs passed into the program
    """
    endpoint: str = sys.argv[1]
    database_url: str = sys.argv[2]
    block_range: str = sys.argv[3]
    return BlockCrawlerRequest(endpoint, database_url, block_range)
