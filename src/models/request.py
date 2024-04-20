class BlockCrawlerRequest:
  def __init__(self, endpoint, database_url, block_range):
    self.endpoint = endpoint
    self.database_url = database_url
    self.block_range = block_range
    self.first_block = None
    self.last_block = None