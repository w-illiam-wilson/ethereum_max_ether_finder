import requests
import json

from src.util.hex_converter import hexToInt

class QuickNodeEthereumAPIService:
    """Service for interacting with QuickNode Ethereum Mainnet API.

    Attributes:
        endpoint (str): The endpoint for quickNode api
    """

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def getCurrentBlockNumber(self):
        """Get the most recent block added to the ethereum chain

        Returns:
            block number (int): The current block number in integer format
        """
        payload = json.dumps({
            "method": "eth_blockNumber",
            "params": [],
            "id": 1,
            "jsonrpc": "2.0"
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.endpoint, headers=headers, data=payload)
        hex_of_block_number = response.json()["result"]
        return hexToInt(hex_of_block_number)

    def getBlock(self, block: int):
        """Get the most recent block added to the ethereum chain

        Args:
            block (int): of block requested

        Returns:
            block: the block requested with attributes like number, transactions (list) 
        """
        #QuickNode expects hex of block number
        hex_of_block_number = hex(block)

        payload = json.dumps({
            "method": "eth_getBlockByNumber",
            "params": [
                hex_of_block_number,
                True
            ],
            "id": 1,
            "jsonrpc": "2.0"
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.endpoint, headers=headers, data=payload)
        #it would be better if we could create a DTO here
        return response.json()