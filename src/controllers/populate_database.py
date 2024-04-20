from src.models.request import BlockCrawlerRequest
from src.services.block_crawler.block_crawler_service import BlockCrawlerService
from src.util.validator import construct_request, parse_block_range, validate_arguments

def populate_database():
    """Validates the request and populates a database with blocks in the provided range
    """
    request: BlockCrawlerRequest = construct_request()
    validate_arguments(request)
    parse_block_range(request)

    print("Populating database...")
    block_crawler_service = BlockCrawlerService(request.quicknode_endpoint, request.database_url)
    block_crawler_service.populate_database(request.first_block, request.last_block)