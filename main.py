from web3.middleware import geth_poa_middleware

from client import Client
from data.config import private_key
from model import Etherium, Optimism, Arbitrum
from model import TokenAmount
from tasks.symbiotic import Symbiotic
from tasks.stargate import Stargate
import time


client = Client(private_key=private_key, network=Etherium)
client_op = Client(private_key=private_key, network=Arbitrum)
symb = Symbiotic(client=client)

stg = Stargate(client=client_op)


'''tx = symb.make_random_deposit_to_symb()'''


tx = stg.bridge_max_eth_to_network('optimism')
res = stg.client.verif_tx(tx_hash=tx)
print(res)

