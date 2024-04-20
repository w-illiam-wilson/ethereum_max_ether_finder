
from src.util.hex_converter import hexToInt
from urllib.parse import urlparse
import psycopg2
from psycopg2 import Error

class PostgresService:
    """Service for interacting with Postgres.

    Attributes:
        database_url (str): The url to connect to the database
        connection: The connection to the database
        cursor: The cursor for interacting with the database
    """

    def __init__(self, database_url: str):
        self.database_url = database_url
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
        parsed_url = urlparse(self.database_url)

        username = parsed_url.username
        password = parsed_url.password
        database = parsed_url.path[1:]
        hostname = parsed_url.hostname
        port = parsed_url.port

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

        Creates a table with columns block_number, transaction_index, and wei_value.
        There can be multiple transactions in a block and each transaction has a wei value associated with it.
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS ethereum_blocks (
                    block_number INTEGER, 
                    transaction_index INTEGER, 
                    wei_value NUMERIC(128),
                    PRIMARY KEY (block_number, transaction_index)
                )""")
            self.connection.commit()
            print("Database table created if it didn't exist")
        except Error as e:
            exit(e)  

    def insertBlockIntoDatabase(self, block: object):
        """Adds a block into the database table

        Extracts the block number, and adds all transactions as rows to the database with an associated wei value.

        Args:
            block: The block retrieved from the api
        """
        
        block_number: int = hexToInt(block["number"])
        transactions: list = block["transactions"]

        for transaction in transactions:
            transaction_index = hexToInt(transaction["transactionIndex"])
            wei_value = hexToInt(transaction["value"])
            executable = f'''
                INSERT INTO ethereum_blocks
                VALUES ({block_number}, {transaction_index}, {wei_value})
                on conflict (block_number, transaction_index) do nothing
            '''
            self.cursor.execute(executable)

        self.connection.commit()

    def getBlockWithMaxWei(self, first_block: int, last_block: int) -> list:
        """Finds the block in the provided range with the most total wei transacted

        Args:
            first_block: The first block in the range (inclusive)
            last_block: The last block in the range (inclusive)
        
        Returns:
            (block_number, wei_transacted) for the block with the largest total wei transacted
        """
        self.cursor.execute(f"""
                SELECT
                    block_number, SUM(wei_value) as total_value
                FROM
                    ethereum_blocks
                WHERE block_number BETWEEN {first_block} AND {last_block}
                GROUP BY
                    block_number
                ORDER BY
                    total_value DESC
                LIMIT 1
            """)
        rows = self.cursor.fetchall()
        print(rows)
        return rows[0]