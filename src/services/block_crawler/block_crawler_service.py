from tqdm import tqdm
from src.services.api.quicknode_ethereum_service import QuickNodeEthereumAPIService
from src.services.database.postgres_service import PostgresService

class BlockCrawlerService:
    """Service for crawling blocks and finding largest wei transactions

    Attributes:
        quickNodeAPIService: The service for interacting with the ethereum blockchain
        postgresService: The service for interacting with the postgres database
    """
    def __init__(self, url, databaseFile):
        self.quickNodeAPIService = QuickNodeEthereumAPIService(url)
        self.postgresService = PostgresService(databaseFile)

    def populateDatabase(self, firstBlock: int, lastBlock: int):
        """Adds blocks from firstBlock number to lastBlock number inclusively to a database

        Args:
            firstBlock: The first block in the range (inclusive)
            lastBlock: The last block in the range (inclusive)
        """
        self.postgresService.createTable()
        #would be nice to parallelize but we don't place a limit on range of blocks so we would need to manage threads carefully
        for blockNumber in tqdm(range(firstBlock, lastBlock + 1)):
            block = self.quickNodeAPIService.getBlock(blockNumber)["result"]
            self.postgresService.insertBlockIntoDatabase(block)

    def getBlockWithMaxWei(self, firstBlock: int, lastBlock: int):
        """Queries the database to find the block with the most transacted wei

        Returns:
            (blockNumber, weiTransacted) for the block with the largest total wei transacted
        """
        return self.postgresService.getBlockWithMaxWei(firstBlock, lastBlock)