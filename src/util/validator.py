import re
import sys

from src.models.request import BlockCrawlerRequest

def validateArgLength():
    """Validates three args were passed in.

    Checks to ensure 3 arguments (api url, database link, and block range). Exits the program if not.
    """
    if(len(sys.argv) < 4):
        exit("you must provide a quicknode url, database link, and block range")

def validateURL(apiURL: str):
    """Validates url format.

    Checks if the URL passed in is in URL format. Exits the program if not.

    Args:
        apiURL: The url string.
    """
    #TODO: ensure url is a quicknode url, not just any url
    expression = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    if (not re.search(expression, apiURL)):
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

def validateBlockRange(blockRange: str) -> list:
    """Validates block range format.

    Checks if the block range is in proper format (number-number). Exits the program if not.

    Args:
        blockRange: The blockrange string.
    """
    expression = "^[0-9]+-[0-9]+$"
    if (not re.search(expression, blockRange)):
        exit("block range format is not correct")

def populateBlockRange(blockCrawlerRequest: BlockCrawlerRequest):
    blocks = blockCrawlerRequest.blockRange.split("-")
    blocks[0] = int(blocks[0])
    blocks[1] = int(blocks[1])

    blockCrawlerRequest.firstBlock = blocks[0]
    blockCrawlerRequest.lastBlock = blocks[1]

    return blocks

def validateArguments(blockCrawlerRequest: BlockCrawlerRequest):
    """Validates all arguments (api url, database url, and blockrange).

    Checks all arguments to ensure they are valid. Exits the program if not.

    Args:
        blockCrawlerRequest: a request object containing all the sysargs passed into the program
    """
    validateArgLength()
    validateURL(blockCrawlerRequest.endpoint)
    validatePostgresURL(blockCrawlerRequest.databaseURL)
    validateBlockRange(blockCrawlerRequest.blockRange)

def constructRequest() -> BlockCrawlerRequest:
    """Places sysargs in an object.

    Grabs sysargs and places them in an object. This does not validate the sysargs exist.

    Returns:
        blockCrawlerRequest: a request object containing all the sysargs passed into the program
    """
    url: str = sys.argv[1]
    sqliteDbFile: str = sys.argv[2]
    blockRange: str = sys.argv[3]
    return BlockCrawlerRequest(url, sqliteDbFile, blockRange)
