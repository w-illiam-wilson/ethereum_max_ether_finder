class BlockCrawlerRequest:
  def __init__(self, quicknode_endpoint: str, database_url: str, block_range: str):
    self.quicknode_endpoint = quicknode_endpoint
    self.database_url = database_url
    self.block_range = block_range
    self.first_block = None
    self.last_block = None