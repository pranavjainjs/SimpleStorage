from web3 import Web3

from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")
install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
network_id = 1337
address = "0xCbEd45395d47D17298E958C39322eBdfC5745Da5"

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)  # we have a contract

# build a tx
# sign a tx
# send a tx

nonce = w3.eth.getTransactionCount(address)
print(nonce)

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": network_id,
        "from": address,
        "nonce": nonce,
    }
)
my_pvt_key = os.getenv("my_pvt_key")
# print(my_pvt_key)

signed_txn = w3.eth.account.signTransaction(transaction, private_key=my_pvt_key)

print("original-")
# send the signed txn

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print("waiting for tx to finish")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("deployed contract")
print(SimpleStorage.functions.retrieve().call())

#working with contract
#contract ABI = abi
#contract address = tx.receipt.contractAddress

simple_storage = w3.eth.contract(address = tx_receipt.contractAddress, abi = abi)

#call -> simulate making the call and getting a return value
#transact -> actually make a state change

store_tx = simple_storage.functions.store(88).buildTransaction(
    {
        "chainId": network_id,
        "from": address,
        "nonce": nonce + 1
    }
)

signed_store_tx = w3.eth.account.sign_transaction(
    store_tx, private_key = my_pvt_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print("updated!!")
print(simple_storage.functions.retrieve().call())
