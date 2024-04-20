from src.controllers.max_ether import get_block_with_max_ether_transacted
from src.controllers.populate_database import populate_database

def main():
    """Populates a database with blocks in the provided range.
    Then, finds the block in the provided range that has the most ether transacted and prints it in the form of 
    "Block with block number {block} transacted the most ether in the given block range with a total of {ether} ether transacted"
    See README for how to pass sysargs in.
    """
    populate_database()
    print(get_block_with_max_ether_transacted())

if __name__ == '__main__':
    main()