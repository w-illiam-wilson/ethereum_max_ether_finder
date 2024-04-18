import re
import sys

from src.models.request import BlockCrawlerRequest

def validateURL(url: str):
    expression = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    if (not re.search(expression, url)):
        exit("URL is not correct")

def validateDatabaseURL(database: str):
    expression = "^postgres:\/\/.+@.+:[0-9]+\/.+$"
    if (not re.search(expression, database)):
        exit("database url must be in the format `postgres://{user}@{host}:{port}/{databaseName}`")

def validateBlockRange(blockRange: str) -> list:
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
    validateArgLength()
    validateURL(blockCrawlerRequest.url)
    validateDatabaseURL(blockCrawlerRequest.databaseURL)
    validateBlockRange(blockCrawlerRequest.blockRange)

def constructRequest() -> BlockCrawlerRequest:
    url: str = sys.argv[1]
    sqliteDbFile: str = sys.argv[2]
    blockRange: str = sys.argv[3]
    return BlockCrawlerRequest(url, sqliteDbFile, blockRange)
    

def validateArgLength():
    if(len(sys.argv) < 4):
        exit("you must provide url, database file, and block range")
