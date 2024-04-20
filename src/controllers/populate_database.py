from src.models.request import BlockCrawlerRequest
from src.services.block_crawler.block_crawler_service import BlockCrawlerService
from src.util.validator import constructRequest, populateBlockRange, validateArguments

def populateDatabase():
    """Populates a database with blocks in the provided range
    """
    print("Populating database...")
    request: BlockCrawlerRequest = constructRequest()
    validateArguments(request)
    populateBlockRange(request)

    block_crawler_service = BlockCrawlerService(request.endpoint, request.database_url)
    block_crawler_service.populateDatabase(request.first_block, request.last_block)