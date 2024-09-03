from web3 import Web3
from data.config import ETHX_ABI, ETHX_SYMB_ABI, Balancer_ABI, OSETH_SYMB_ABI, RETH_POOL_ABI

from client import Client
from data.config import private_key
from model import Etherium
from utils import read_json


client = Client(private_key=private_key, network=Etherium)

ethx_abi = read_json(ETHX_ABI)
ethx_adress = Web3.to_checksum_address('0xcf5ea1b38380f6af39068375516daf40ed70d299')
ethx_contract = client.w3.eth.contract(abi=ethx_abi, address=ethx_adress)

ethx_symb_address = Web3.to_checksum_address('0xBdea8e677F9f7C294A4556005c640Ee505bE6925')
ethx_symb_contract = client.w3.eth.contract(abi=read_json(ETHX_SYMB_ABI), address=ethx_symb_address)

balancer_address = Web3.to_checksum_address('0xBA12222222228d8Ba445958a75a0704d566BF2C8')
balancer_contract = client.w3.eth.contract(abi=read_json(Balancer_ABI), address=balancer_address)

osEth_token_address = Web3.to_checksum_address('0xf1C9acDc66974dFB6dEcB12aA385b9cD01190E38')

oseth_symb_address = Web3.to_checksum_address('0x52cB8A621610Cc3cCf498A1981A8ae7AD6B8AB2a')
oseth_symb_contract = client.w3.eth.contract(abi=read_json(OSETH_SYMB_ABI), address=oseth_symb_address)

rEth_pool_adress = Web3.to_checksum_address('0x16D5A408e807db8eF7c578279BEeEe6b228f1c1C')
rEth_pool_contract = client.w3.eth.contract(abi=read_json(RETH_POOL_ABI), address=rEth_pool_adress)

rEth_token_address = Web3.to_checksum_address('0xae78736Cd615f374D3085123A210448E74Fc6393')

rEth_symb_address = Web3.to_checksum_address('0x03bf48b8a1b37fbead1ecabcf15b98b924ffa5ac')
rEth_symb_contract = client.w3.eth.contract(abi=read_json(ETHX_SYMB_ABI), address=rEth_token_address)