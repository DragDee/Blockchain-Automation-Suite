import eth_abi.packed
from web3 import Web3, Account
from typing import Optional
import time
import random

from client import Client
from data.config import WOOFI_ABI, private_key
from utils import read_json
from model import TokenAmount

from adresses.symb_adresses import ethx_adress, ethx_contract, ethx_symb_address, ethx_symb_contract, \
    balancer_contract, osEth_token_address, oseth_symb_address, oseth_symb_contract, rEth_pool_adress,\
    rEth_pool_contract, rEth_token_address, rEth_symb_address, rEth_symb_contract,  balancer_address


class Symbiotic:
    maxPriorityFeePerGas = TokenAmount(0.0000000001557504446, wei=False)
    gasLimit = 150000

    ethx_token_address = Web3.to_checksum_address('0xA35b1B31Ce002FBF2058D22F30f95D405200A15b')


    diaposone = (5, 10)
    slippage = 0.05
    time_out = 1000

    def __init__(self, client: Client):
        self.client = client

    def get_random_custom_prior_fee(self) -> TokenAmount:
        fee_adon_diaposon = [0.05, 0.1]

        fee_adon_part = random.uniform(*fee_adon_diaposon)
        PriorityFee = float(self.maxPriorityFeePerGas.Ether) * (1 + fee_adon_part)
        PriorityFee = TokenAmount(PriorityFee, wei=False)

        return PriorityFee

    def get_amount(self) -> TokenAmount:
        random_procent = random.randint(*Symbiotic.diaposone) / 100
        balance = self.client.w3.eth.get_balance(self.client.address)
        balance = float(self.client.w3.from_wei(balance, 'ether')) * random_procent

        return TokenAmount(balance, wei=False)

    def make_random_deposit_to_symb(self):
        random_id = random.randint(0, 2)

        if random_id == 0:
            return self.ethx_to_symb()
        elif random_id == 1:
            return self.oseth_to_symb()
        else:
            return self.rEth_to_symb()

    def token_to_symb(self, token_address, symb_pool_address, symb_pool_contract, get_token_func,
                      amount: Optional[TokenAmount] = None):

        deposit_function_selector = '0x47e7ef24'

        tx1 = get_token_func(amount)
        if not self.client.verif_tx(tx_hash=tx1):
            return False

        token_balance = self.client.balance_of(token_address)
        self.client.approve_interface(token_address, symb_pool_address, amount=token_balance)

        print(f'Starting deposit {token_balance.Ether} tokens to SYMBIOTIC')

        tx_params = (
            self.client.address,
            token_balance.Wei
        )

        func = symb_pool_contract.get_function_by_selector(deposit_function_selector)
        tx = func(*tx_params).build_transaction({
            'from': self.client.address,
            'gas': Symbiotic.gasLimit,
            "maxPriorityFeePerGas": Symbiotic.maxPriorityFeePerGas.Wei,
        })

        return self.client.send_transaction(
            to=symb_pool_address,
            data=tx['data'],
            max_priority_fee_per_gas=self.get_random_custom_prior_fee().Wei
        )

    def rEth_to_symb(self, amount: Optional[TokenAmount] = None):
        return self.token_to_symb(rEth_token_address, rEth_symb_address, rEth_symb_contract, self.get_rEth, amount)

    def get_rEth(self, amount: Optional[TokenAmount] = None):
        swap_function_selector = '0x55362f4d'
        reth_koef = 0.88

        if not amount:
            amount = self.get_amount()

        print(f'Starting swap of {amount.Ether} ETH to rETH')


        amount_out_min = TokenAmount(float(amount.Ether) * reth_koef, wei=False)

        uniswap = 0
        balancer = 10


        tx_params = (uniswap,
                     balancer,
                     amount_out_min.Wei,
                     amount.Wei
        )

        func = rEth_pool_contract.get_function_by_selector(swap_function_selector)
        tx = func(*tx_params).build_transaction({
            'from': self.client.address,
            'gas': Symbiotic.gasLimit,
            "maxPriorityFeePerGas": self.get_random_custom_prior_fee().Wei,
        })

        return self.client.send_transaction(
            to=rEth_pool_adress,
            data=tx['data'],
            max_priority_fee_per_gas=self.get_random_custom_prior_fee().Wei,
            value=amount.Wei,
        )

    def get_osEth(self, amount: Optional[TokenAmount] = None):
        swap_function_selector = '0x52bbbe29'

        if not amount:
            amount = self.get_amount()

        print(f'Starting swap of {amount.Ether} ETH to osETH')



        user_data_encoded = eth_abi.packed.encode_packed(['uint256'], [0])
        user_data_encoded = '0x'

        osEth_address = Web3.to_checksum_address('0xf1C9acDc66974dFB6dEcB12aA385b9cD01190E38')

        singleSwap = (
            '0xdacf5fa19b1f720111609043ac67a9818262850c000000000000000000000635',
            0,
            Web3.to_checksum_address('0x0000000000000000000000000000000000000000'),
            osEth_address,
            amount.Wei,
            user_data_encoded,
        )

        funds = (
            self.client.address,
            False,
            self.client.address,
            False,
        )

        limit = (1 - Symbiotic.slippage) * float(amount.Ether)
        limit = TokenAmount(limit, wei=False).Wei

        deadline = int(time.time() + Symbiotic.time_out)



        func = balancer_contract.get_function_by_selector(swap_function_selector)
        tx = func(
            singleSwap,
            funds,
            limit,
            deadline).build_transaction({
            'from': self.client.address,
            'gas': Symbiotic.gasLimit,
            "maxPriorityFeePerGas": Symbiotic.maxPriorityFeePerGas.Wei,
        })



        return self.client.send_transaction(
            to=balancer_address,
            data=tx['data'],
            max_priority_fee_per_gas=self.maxPriorityFeePerGas.Wei,
            value=amount.Wei,
        )

    def oseth_to_symb(self, amount: Optional[TokenAmount] = None):
        return self.token_to_symb(osEth_token_address, oseth_symb_address, oseth_symb_contract, self.get_osEth, amount)



    def ethx_to_symb(self, amount: Optional[TokenAmount] = None):
        return self.token_to_symb(ethx_adress, ethx_symb_address, ethx_symb_contract, self.get_ethx, amount)

    def get_ethx(self, amount: Optional[TokenAmount] = None):
        if not amount:
            amount = self.get_amount()

        print(f'Starting swap of {amount.Ether} ETH to ETHx')



        value = TokenAmount(round(amount.Ether, 4), wei=False)

        tx_params = (
            self.client.address
        )



        tx = ethx_contract.functions.deposit(tx_params).build_transaction({'from': self.client.address,
                                                              'gas': Symbiotic.gasLimit,
                                                              "maxPriorityFeePerGas": Symbiotic.maxPriorityFeePerGas.Wei,
                                                              })

        return self.client.send_transaction(
            to=ethx_adress,
            data=tx['data'],
            value=value.Wei,
            max_priority_fee_per_gas=self.maxPriorityFeePerGas.Wei

        )
