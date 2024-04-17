class BlockCrawlerRequest:
  def __init__(self, url, databaseFile, blockRange):
    self.url = url
    self.databaseFile = databaseFile
    self.blockRange = blockRange
    self.firstBlock = None
    self.lastBlock = None