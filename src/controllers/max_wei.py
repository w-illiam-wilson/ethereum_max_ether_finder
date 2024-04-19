from src.models.request import BlockCrawlerRequest
from src.services.block_crawler.block_crawler_service import BlockCrawlerService
from src.util.validator import constructRequest, populateBlockRange, validateArguments

def getBlockWithMaxWeiTransacted():
    """Finds the block in the provided range that has the most wei transacted and prints it
    """
    print("Getting max wei in block range...")
    request: BlockCrawlerRequest = constructRequest()
    validateArguments(request)
    populateBlockRange(request)

    blockCrawlerService = BlockCrawlerService(request.endpoint, request.databaseURL)
    print(blockCrawlerService.getBlockWithMaxWei(request.firstBlock, request.lastBlock))