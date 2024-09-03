import os
import sys
from pathlib import Path
from data.prvt_key import prvt_key

DATABASE_NAME = 'application.sqlite'

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, 'abis')

TOKEN_ABI = os.path.join(ABIS_DIR, 'token.json')
WOOFI_ABI = os.path.join(ABIS_DIR, 'woofi.json')
ETHX_ABI = os.path.join(ABIS_DIR, 'ethx.json')
ETHX_SYMB_ABI = os.path.join(ABIS_DIR, 'symb\ethx_symb.json')
Balancer_ABI = os.path.join(ABIS_DIR, 'balancer.json')
OSETH_SYMB_ABI = os.path.join(ABIS_DIR, 'symb\oseth_symb.json')
RETH_POOL_ABI = os.path.join(ABIS_DIR, 'reth_pool.json')
STARGATE_ABI = os.path.join(ABIS_DIR, 'stargate.json')

private_key = prvt_key
seed = ''
eth_rpc = 'https://mainnet.infura.io/v3/'
arb_rpc = 'https://rpc.ankr.com/arbitrum/'
