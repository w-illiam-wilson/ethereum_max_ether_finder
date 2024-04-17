import re
import sys

from src.models.request import BlockCrawlerRequest

def checkURL(url: str):
    expression = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    if (not re.search(expression, url)):
        exit("URL is not correct")

def checkDbFile(fileName: str):
    expression = ".+.sqlite3$"
    if (not re.search(expression, fileName)):
        exit("file format is not correct")

def validateAndGetBlockRange(blockRange: str) -> list:
    expression = "^[0-9]+-[0-9]+$"
    if (not re.search(expression, blockRange)):
        exit("block range format is not correct")
    blocks = blockRange.split("-")
    blocks[0] = int(blocks[0])
    blocks[1] = int(blocks[1])
    if(blocks[1] < blocks[0]):
        exit("second block number must be greater than or equal to first block number")
    return blocks

def validateAndTransformParameters(blockCrawlerRequest: BlockCrawlerRequest):
    checkURL(blockCrawlerRequest.url)
    checkDbFile(blockCrawlerRequest.databaseFile)
    blocks = validateAndGetBlockRange(blockCrawlerRequest.blockRange)

    blockCrawlerRequest.firstBlock = blocks[0]
    blockCrawlerRequest.lastBlock = blocks[1]

def validateArgLength():
    if(len(sys.argv) < 4):
        exit("you must provide url, database file, and block range")
