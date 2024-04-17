import requests
import json

from src.util.hex_converter import hexToInt

class EthereumMainnetService:
    def __init__(self, url):
        self.url = url

    def getCurrentBlockNumber(self):
        payload = json.dumps({
            "method": "eth_blockNumber",
            "params": [],
            "id": 1,
            "jsonrpc": "2.0"
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        hexOfBlockNumber = response.json()["result"]
        return hexToInt(hexOfBlockNumber)

    def getBlock(self, block: int):
        #QuickNode expects hex of block number
        hexOfBlockNumber = hex(block)

        payload = json.dumps({
            "method": "eth_getBlockByNumber",
            "params": [
                hexOfBlockNumber,
                True
            ],
            "id": 1,
            "jsonrpc": "2.0"
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        #it would be better if we could create a DTO here
        return response.json()