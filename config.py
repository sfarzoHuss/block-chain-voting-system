from web3 import Web3
import json

######################################################################################
############################### WEB3 CONNECTORS ######################################
######################################################################################

# Connect to Ganache (or your Ethereum testnet)
web3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))  # Replace with your Ganache URL
web3.enable_unstable_package_management_api()


# Address of your deployed UserContract and VotingContract
user_contract_address = "0x92C2CaDAf01B85dDd245bF555315819221347489"
election_contract_address = "0x5bF3a35B6A6dB750Cd54f2B699FA9Ee05192ef7b"
candidate_contract_address = "0x0Cf486122D28776723a369222242d84750982824"
voting_contract_address = "0xa9DD45B72e5160d11bd1c53338fd9f591d5f12bd"

# ABIs
user_abi_file_path = './abis/user_contract_abi.json'
election_abi_file_path = './abis/election_contract_abi.json'
candidate_abi_file_path = './abis/candidate_contract_abi.json'
voting_abi_file_path = './abis/voting_contract_abi.json'

# Read the content of the JSON files
with open(user_abi_file_path, 'r') as file:
    user_contract_abi = json.load(file)

with open(election_abi_file_path, 'r') as file:
    election_contract_abi = json.load(file)

with open(candidate_abi_file_path, 'r') as file:
    candidate_contract_abi = json.load(file)

with open(voting_abi_file_path, 'r') as file:
    voting_contract_abi = json.load(file)

# Create contract instances
user_contract = web3.eth.contract(address=user_contract_address, abi=user_contract_abi)
election_contract = web3.eth.contract(address=election_contract_address, abi=election_contract_abi)
candidate_contract = web3.eth.contract(address=candidate_contract_address, abi=candidate_contract_abi)
voting_contract = web3.eth.contract(address=voting_contract_address, abi=voting_contract_abi)


# account used for general transactions:
#   -) users login (same procedure for both, government employees and citizens);
#   -) voting action;
account_elections = web3.eth.accounts[0]

# account used for government operations (flag is_admin set):
#   -) government employees registration;
account_government = web3.eth.accounts[1]
# account used for citizens operations (flag is_admin not set):
#   -) citizens registration;
account_citizens = web3.eth.accounts[2]

