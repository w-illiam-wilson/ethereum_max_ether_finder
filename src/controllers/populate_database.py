from src.models.request import BlockCrawlerRequest
from src.services.block_crawler.block_crawler_service import BlockCrawlerService
from src.util.validator import constructRequest, populateBlockRange, validateArguments

def populateDatabase():
    print("Populating database...")
    request: BlockCrawlerRequest = constructRequest()
    validateArguments(request)
    populateBlockRange(request)

    blockCrawlerService = BlockCrawlerService(request.url, request.databaseFile)
    blockCrawlerService.populateDatabase(request.firstBlock, request.lastBlock)