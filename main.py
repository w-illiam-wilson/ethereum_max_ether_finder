from src.controllers.max_wei import getMaxWei
from src.controllers.populate_database import populateDatabase

def main():
    populateDatabase()
    getMaxWei()

if __name__ == '__main__':
    main()