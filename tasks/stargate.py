import eth_abi.packed
from web3 import Web3, Account
from typing import Optional
import time
import random

from client import Client
from data.config import WOOFI_ABI, private_key, STARGATE_ABI
from utils import read_json
from model import TokenAmount
from data.stargate_networks import Etherium, Network, Arbitrum
from models.stargate_networks import StargateNetwork
from models.database import Session
from adresses.symb_adresses import ethx_adress


class Stargate:
    maxPriorityFeePerGas = TokenAmount(0.0000000001557504446, wei=False)
    gasLimit = 150000
    slippage = 20  # %


    def __init__(self, client: Client):
        self.client = client

        arrival_network = self.client.network.name

        self.session = Session()
        arrival_network = self.session.query(StargateNetwork).filter(StargateNetwork.name == arrival_network)[0]

        self.stargate_address = Web3.to_checksum_address(arrival_network.poolNative)
        self.stargate_contract = self.client.w3.eth.contract(address=self.stargate_address, abi=read_json(STARGATE_ABI))

    def to_32byte_hex(self, val) -> str:
        return "0x" + "0"*24 + str(val)[2:]


    def stargate_bridge(self, dest_network: Network, amount: Optional[TokenAmount] = None):

        address = self.to_32byte_hex(self.client.address)
        min_recieved = Web3.to_wei(float(amount.Ether) * (100 - self.slippage) / 100, 'ether')


        sendParam = (
            dest_network.endpointId,
            address,
            amount.Wei,
            min_recieved,
            '0x',
            '0x',
            '0x01'
        )

        fee = self.stargate_contract.functions.quoteSend(
            sendParam,
            False
        ).call()

        tx = self.stargate_contract.functions.send(
            sendParam,
            fee,
            self.client.address
        ).build_transaction({
            'from': self.client.address,
            'gas': self.gasLimit,
            "maxPriorityFeePerGas": self.maxPriorityFeePerGas.Wei,
        })

        value = amount.Wei + fee[0] ####

        return self.client.send_transaction(
            to=self.stargate_address,
            data=tx['data'],
            max_priority_fee_per_gas=self.client.get_random_custom_prior_fee().Wei,
            value=value
        )


    def stargate_bridge_modular(self, amount: TokenAmount, dest_network_name: str):
        sendParam = self.get_sendParam(amount=amount, dest_network_name=dest_network_name)
        fee = self.get_fee(sendParam)
        tx = self.get_tx(sendParam=sendParam, fee=fee)

        value = amount.Wei + fee[0]

        return self.client.send_transaction(
            to=self.stargate_address,
            data=tx['data'],
            max_priority_fee_per_gas=self.client.get_random_custom_prior_fee().Wei,
            value=value
        )

    def get_tx(self, sendParam: tuple, fee: tuple):
        tx = self.stargate_contract.functions.send(
            sendParam,
            fee,
            self.client.address
        ).build_transaction({
            'from': self.client.address,
            'gas': self.gasLimit,
            "maxPriorityFeePerGas": self.maxPriorityFeePerGas.Wei,
        })

        return tx

    def get_sendParam(self, amount: TokenAmount, dest_network_name: str) -> tuple:
        dest_network = self.session.query(StargateNetwork).filter(StargateNetwork.name == dest_network_name)[0]
        address = self.to_32byte_hex(self.client.address)
        min_recieved = Web3.to_wei(float(amount.Ether) * (100 - self.slippage) / 100, 'ether')

        sendParam = (
            dest_network.endpointId,
            address,
            amount.Wei,
            min_recieved,
            '0x',
            '0x',
            '0x01'
        )

        return sendParam

    def get_fee(self, sendParam: tuple) -> tuple:
        fee = self.stargate_contract.functions.quoteSend(
            sendParam,
            False
        ).call()

        return fee

    def bridge_to_arb(self):
        amount = TokenAmount(0.0001, wei=False)
        return self.stargate_bridge(Arbitrum, amount)

    def bridge_max_eth_to_network(self, dest_network_name: str):
        amount = self.client.w3.eth.get_balance(self.client.address)
        sendParam = self.get_sendParam(TokenAmount(amount, wei=True), dest_network_name)
        fee = self.get_fee(sendParam=sendParam)
        tx = self.get_tx(sendParam=sendParam, fee=fee)

        max_fee_per_gas = self.client.get_max_fee_per_gas()
        tx_cost = tx['gas'] * max_fee_per_gas

        amount = amount - fee[0] - tx_cost

        return self.stargate_bridge_modular(amount=TokenAmount(amount, wei=True), dest_network_name=dest_network_name)
