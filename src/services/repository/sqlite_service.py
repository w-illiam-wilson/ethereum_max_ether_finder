
from src.util.hex_converter import hexToInt
import sqlite3
from sqlite3 import Error, Connection, Cursor, Error

class SQLiteService:
    def __init__(self, databaseFile):
        self.databaseFile = databaseFile
        self.connection: Connection = None
        self.cursor: Cursor = None
        self.createConnection()

    def __del__(self):
        # body of destructor
        if self.connection:
            self.connection.close()

    def createConnection(self):
        """ create a database connection to a SQLite database """
        try:
            self.connection = sqlite3.connect(self.databaseFile)
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
                    weiValue INTEGER,
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
                    blockNumber, MAX(weiValue)
                FROM
                    blocks
                GROUP BY blockNumber
                """)
        rows = self.cursor.fetchall()
        return rows