from src.models.request import BlockCrawlerRequest
from src.models.response import BlockCrawlerResponse
from src.services.block_crawler.block_crawler_service import BlockCrawlerService
from src.util.validator import constructRequest, populateBlockRange, validateArguments

def getBlockWithMaxWeiTransacted() -> BlockCrawlerResponse:
    """Validates the request, finds the block in the provided range that has the most wei transacted and returns it

    Returns:
        BlockCrawlerResponse: a string response in the form of "Block with block number {block} transacted the most wei in the given block range with a total of {wei} wei transacted"
    """
    request: BlockCrawlerRequest = constructRequest()
    validateArguments(request)
    populateBlockRange(request)

    print("Getting max wei in block range...")
    blockCrawlerService = BlockCrawlerService(request.endpoint, request.database_url)
    return blockCrawlerService.getBlockWithMaxWei(request.first_block, request.last_block)