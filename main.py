from src.controllers.max_wei import getBlockWithMaxWeiTransacted
from src.controllers.populate_database import populateDatabase

def main():
    """Populates a database with blocks in the provided range.
    Then, finds the block in the provided range that has the most wei transacted and prints it in the form of 
    "Block with block number {block} transacted the most wei in the given block range with a total of {wei} wei transacted"
    See README for how to pass sysargs in.
    """
    populateDatabase()
    print(getBlockWithMaxWeiTransacted())

if __name__ == '__main__':
    main()