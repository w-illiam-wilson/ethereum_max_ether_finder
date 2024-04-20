from src.controllers.max_wei import getBlockWithMaxWeiTransacted
from src.controllers.populate_database import populateDatabase

def main():
    """Populates a database with blocks in the provided range.
    Then, finds the block in the provided range that has the most wei transacted and prints it
    """
    populateDatabase()
    print(getBlockWithMaxWeiTransacted())

if __name__ == '__main__':
    main()