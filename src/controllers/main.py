import sys
from src.models.request import BlockCrawlerRequest
from src.services.block_crawler.block_crawler_service import BlockCrawlerService
from src.util.validator import validateAndTransformParameters

def main():
    url: str = sys.argv[1]
    sqliteDbFile: str = sys.argv[2]
    blockRange: str = sys.argv[3]
    request = BlockCrawlerRequest(url, sqliteDbFile, blockRange)
    validateAndTransformParameters(request)

    blockCrawlerService = BlockCrawlerService(request.url, request.databaseFile)
    blockCrawlerService.populateDatabase(request.firstBlock, request.lastBlock)

if __name__ == '__main__':
    main()