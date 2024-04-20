from tqdm import tqdm

from src.models.response import BlockCrawlerResponse
from src.services.sources.ethereum_api.quicknode_ethereum_service import QuickNodeEthereumAPIService
from src.services.sources.database.postgres_service import PostgresService
from src.util.wei_converter import wei_to_ether

class BlockCrawlerService:
    """Service for crawling blocks and finding largest ether transactions

    Attributes:
        quicknode_api_service: The service for interacting with the ethereum blockchain
        postgres_service: The service for interacting with the postgres database
    """
    def __init__(self, quicknode_endpoint: str, database_url: str):
        self.quicknode_api_service = QuickNodeEthereumAPIService(quicknode_endpoint)
        self.postgres_service = PostgresService(database_url)

    def populate_database(self, first_block: int, last_block: int):
        """Adds blocks from first_block number to last_block number inclusively to a database

        Args:
            first_block: The first block in the range (inclusive)
            last_block: The last block in the range (inclusive)
        """
        self.postgres_service.create_ethereum_blocks_table()
        #would be nice to parallelize but we don't place a limit on range of blocks so we would need to manage threads carefully
        print("Populating table...")
        for block_number in tqdm(range(first_block, last_block + 1)):
            block = self.quicknode_api_service.get_block(block_number)
            self.postgres_service.insert_block_into_database(block)

    def get_block_with_max_ether(self, first_block: int, last_block: int) -> BlockCrawlerResponse:
        """Queries the database to find the block with the most transacted ether

        Args:
            first_block: The first block in the range (inclusive)
            last_block: The last block in the range (inclusive)

        Returns:
            BlockCrawlerResponse: an object holding a block number and the ether the block transacted
        """
        block, total_ether_value = self.postgres_service.get_block_with_max_wei(first_block, last_block)
        return BlockCrawlerResponse(block, wei_to_ether(total_ether_value))