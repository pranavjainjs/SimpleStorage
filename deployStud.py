from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()

with open("./students.sol", "r") as file:
    simple_storage_file = file.read()


install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"students.sol": {"content": simple_storage_file}},
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



# with open("./compiled_stud.json", "w") as file2:
#     file2.write(str(compiled_sol))
#     file2.close()

bytecode = compiled_sol["contracts"]["students.sol"]["student"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["students.sol"]["student"]["abi"]


w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
network_id = 1337
address = "0xC7e616b64552a407F2988501fE8e11831054D92F"
private_key = os.getenv("private_key_ganache")

# the contract
aStudent = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(address)
print(nonce)

#building a txn
txn = aStudent.constructor().buildTransaction(
    {
        "chainId": network_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)

#signing the txn
txn_signed = w3.eth.account.sign_transaction(txn, private_key=private_key)

#sending the txn
#deployed the contract
txn_hash = w3.eth.send_raw_transaction(txn_signed.rawTransaction)

print("waiting for tx to finish")

#txn receipt
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Done! Contract deployed to {txn_receipt.contractAddress}")

## interacting with the deployed contract
simple_storage = w3.eth.contract(address = txn_receipt.contractAddress, abi = abi)

with open("./index.txt", "r") as file:
    index = int(file.read())
    file.close()

print(index)

#building a txn
txn_addStud = simple_storage.functions.addStud(210103003, 'ACHINTYA', 'Mechanical Engineering', 'g.achintya ', index).buildTransaction(
    {
        "chainId": network_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce + 1
    }
)

#signed the txn
txn_addStud_signed = w3.eth.account.sign_transaction(
    txn_addStud, private_key = private_key
)

#sent the txn
txn_addStud_hash = w3.eth.send_raw_transaction(txn_addStud_signed.rawTransaction)

#txn receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(txn_addStud_hash)

print("updated!!")

with open("./index.txt", "w") as file:
    index = index + 1
    file.write(str(index))
    file.close()

print(simple_storage.functions.retrieve(210103003).call())
