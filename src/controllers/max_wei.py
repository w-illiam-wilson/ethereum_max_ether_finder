from src.models.request import BlockCrawlerRequest
from src.services.block_crawler.block_crawler_service import BlockCrawlerService
from src.util.validator import constructRequest, populateBlockRange, validateArguments

def getMaxWei():
    print("Getting max wei in block range...")
    request: BlockCrawlerRequest = constructRequest()
    validateArguments(request)
    populateBlockRange(request)

    blockCrawlerService = BlockCrawlerService(request.url, request.databaseFile)
    print(blockCrawlerService.getBlockWithMaxWei(request.firstBlock, request.lastBlock))