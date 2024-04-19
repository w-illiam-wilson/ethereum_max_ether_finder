
from src.util.hex_converter import hexToInt
from urllib.parse import urlparse
import psycopg2
from psycopg2 import Error

class PostgresService:
    """Service for interacting with Postgres.

    Attributes:
        databaseURL (str): The url to connect to the database
        connection: The connection to the database
        cursor: The cursor for interacting with the database
    """

    def __init__(self, databaseURL):
        self.databaseURL = databaseURL
        self.connection = None
        self.cursor = None
        self.createConnection()

    def __del__(self):
        """Closes the database connection
        """
        if self.connection:
            self.connection.close()
            print("Database connection closed")

    def createConnection(self):
        """Creates the connection to the database.

        Parses the databaseURL passed in to the object into host, username, port, database and connects to it.
        """
        urlParsed = urlparse(self.databaseURL)

        username = urlParsed.username
        password = urlParsed.password
        database = urlParsed.path[1:]
        hostname = urlParsed.hostname
        port = urlParsed.port

        try:
            self.connection = psycopg2.connect(
                database = database,
                user = username,
                password = password,
                host = hostname,
                port = port
            )
            self.cursor = self.connection.cursor()
            print("Database connection created")
        except Error as e:
            exit(e)  

    def createTable(self):
        """Creates the table for storing ethereum blocks

        Creates a table with columns blockNumber, transactionIndex, and weiValue.
        There can be multiple transactions in a block and each transaction has a wei value associated with it.
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS blocks (
                    blockNumber INTEGER, 
                    transactionIndex INTEGER, 
                    weiValue NUMERIC(128),
                    PRIMARY KEY (blockNumber, transactionIndex)
                )""")
            self.connection.commit()
            print("Database table created if it didn't exist")
        except Error as e:
            exit(e)  

    def insertBlockIntoDatabase(self, block):
        """Adds a block into the database table

        Extracts the block number, and adds all transactions as rows to the database with an associated wei value.

        Args:
            block: The block retrieved from the api
        """
        blockNumber: int = hexToInt(block["number"])
        transactions: list = block["transactions"]

        for transaction in transactions:
            transactionIndex = hexToInt(transaction["transactionIndex"])
            weiValue = hexToInt(transaction["value"])
            executable = f'''
                INSERT INTO blocks
                VALUES ({blockNumber}, {transactionIndex}, {weiValue})
                on conflict (blockNumber, transactionIndex) do nothing
            '''
            self.cursor.execute(executable)

        self.connection.commit()

    def getBlockWithMaxWei(self, firstBlock: int, lastBlock: int):
        """Finds the block in the provided range with the most total wei transacted

        Args:
            firstBlock: The first block in the range (inclusive)
            lastBlock: The last block in the range (inclusive)
        
        Returns:
            (blockNumber, weiTransacted) for the block with the largest total wei transacted
        """
        self.cursor.execute(f"""
                SELECT
                    blockNumber, SUM(weiValue) as totalValue
                FROM
                    blocks
                WHERE blockNumber BETWEEN {firstBlock} AND {lastBlock}
                GROUP BY
                    blockNumber
                ORDER BY
                    totalValue DESC
                LIMIT 1
            """)
        rows = self.cursor.fetchall()
        return rows