
from src.util.hex_converter import hexToInt
from urllib.parse import urlparse
import psycopg2
from psycopg2 import Error

class PostgresService:
    def __init__(self, databaseURL):
        self.databaseURL = databaseURL
        self.connection = None
        self.cursor = None
        self.createConnection()

    def __del__(self):
        # body of destructor
        if self.connection:
            self.connection.close()
            print("Database connection closed")

    def createConnection(self):
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
        # insert into sqlite database
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

    def getBlockWithMaxWei(self, firstBlock, lastBlock):
        ##TODO: fix this query, read problem again
        self.cursor.execute("""
                SELECT
                    blockNumber, SUM(weiValue) as totalValue
                FROM
                    blocks
                GROUP BY
                    blockNumber
                ORDER BY
                    totalValue DESC
                LIMIT 1
            """)
        rows = self.cursor.fetchall()
        return rows