from src.models.request import BlockCrawlerRequest
from src.services.block_crawler.block_crawler_service import BlockCrawlerService
from src.util.validator import constructRequest, populateBlockRange, validateArguments

def populateDatabase():
    """Validates the request, populates a database with blocks in the provided range
    """
    request: BlockCrawlerRequest = constructRequest()
    validateArguments(request)
    populateBlockRange(request)

    print("Populating database...")
    block_crawler_service = BlockCrawlerService(request.endpoint, request.database_url)
    block_crawler_service.populateDatabase(request.first_block, request.last_block)