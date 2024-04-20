from decimal import Decimal
from web3 import Web3

def wei_to_ether(wei: Decimal) -> int:
    """Converts wei to ether

    Args:
        wei: The wei value

    Returns:
        wei converted to ether
    """
    return Web3.from_wei(wei, 'ether')