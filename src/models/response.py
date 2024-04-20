class BlockCrawlerResponse:
  def __init__(self, block, total_wei_value):
    self.block = block
    self.total_wei_value = total_wei_value

  def __str__(self):
        return f'Block with block number {self.block} transacted the most wei in the given block range with a total of {self.total_wei_value} wei transacted'