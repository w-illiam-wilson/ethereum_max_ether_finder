from tqdm import tqdm
from src.services.ethereum.ethereum_service import EthereumMainnetService
from src.services.repository.sqlite_service import SQLiteService

class BlockCrawlerService:
    def __init__(self, url, databaseFile):
        self.ethereumService = EthereumMainnetService(url)
        self.sqLiteService = SQLiteService(databaseFile)

    def populateDatabase(self, firstBlock: int, lastBlock: int):
        self.sqLiteService.createTable()
        #would be nice to parallelize but we don't place a limit on range of blocks so we would need to manage threads carefully
        for blockNumber in tqdm(range(firstBlock, lastBlock + 1)):
            block = self.ethereumService.getBlock(blockNumber)["result"]
            self.sqLiteService.insertBlockIntoDatabase(block)

    def getMaxWei(self, firstBlock: int, lastBlock: int):
        return self.sqLiteService.getMaxWei(firstBlock, lastBlock)