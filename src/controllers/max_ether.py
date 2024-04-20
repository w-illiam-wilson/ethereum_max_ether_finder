from src.models.request import BlockCrawlerRequest
from src.models.response import BlockCrawlerResponse
from src.services.block_crawler.block_crawler_service import BlockCrawlerService
from src.util.validator import construct_request, parse_block_range, validate_arguments

def get_block_with_max_ether_transacted() -> BlockCrawlerResponse:
    """Validates the request, finds the block in the provided range that has the most ether transacted, and returns it

    Returns:
        BlockCrawlerResponse: a string response in the form of "Block with block number {block} transacted the most ether in the given block range with a total of {ether} ether transacted"
    """
    request: BlockCrawlerRequest = construct_request()
    validate_arguments(request)
    parse_block_range(request)

    print("Getting max ether in block range...")
    blockCrawlerService = BlockCrawlerService(request.quicknode_endpoint, request.database_url)
    return blockCrawlerService.get_block_with_max_ether(request.first_block, request.last_block)