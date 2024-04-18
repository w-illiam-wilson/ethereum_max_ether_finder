
from src.util.hex_converter import hexToInt
import sqlite3
from sqlite3 import Error, Connection, Cursor, Error
from urllib.parse import urlparse
import psycopg2

class SQLiteService:
    def __init__(self, databaseURL):
        self.databaseURL = databaseURL
        self.connection: Connection = None
        self.cursor: Cursor = None
        self.createConnection()

    def __del__(self):
        # body of destructor
        if self.connection:
            self.connection.close()

    def createConnection(self):
        urlParsed = urlparse(self.databaseURL)

        pg_connection_dict = {
            'dbname': urlParsed.hostname,
            'user': urlParsed.username,
            'password': urlParsed.password,
            'port': urlParsed.port,
            'host': urlParsed.scheme
        }

        print(pg_connection_dict)
        try:
            self.connection = psycopg2.connect(**pg_connection_dict)
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

            #integer may be too small, but sqlite only supports up to 64 bit integers
            weiValue = hexToInt(transaction["value"])
            executable = f'INSERT INTO blocks VALUES ({blockNumber}, {transactionIndex}, {weiValue})'
            try:
                self.cursor.execute(executable)
            except Error as e:
                if ("UNIQUE constraint failed" in e.args[0]):
                    #if the block is already in the database, that is ok, we don't want to error
                    continue
                else:
                    exit(e)
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