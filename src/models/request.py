class BlockCrawlerRequest:
  def __init__(self, endpoint, databaseFile, blockRange):
    self.endpoint = endpoint
    self.databaseURL = databaseFile
    self.blockRange = blockRange
    self.firstBlock = None
    self.lastBlock = None