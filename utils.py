from config import *

def string_to_bytes32(input_string):
    # Ensure the string is UTF-8 encoded
    utf8_string = input_string.encode('utf-8')

    # Pad the string with zeros to make it 32 bytes
    padded_string = utf8_string.ljust(32, b'\0')

    return padded_string

def bytes32_to_string(bytes32):
    # Convert bytes32 to string and remove trailing null bytes
    return bytes32.rstrip(b'\0').decode('utf-8')

def get_all_elections():
    all_elections = election_contract.functions.getAllElections().call()
    print("All Elections:")
    elections = []
    for election in all_elections:
        # election is list-like access
        election_dictionary = {'id': election[0],
        'purpose': bytes32_to_string(election[1]),
        'expired': election[2]
        }
        elections.append(election_dictionary)
        print(f"Election ID: {election_dictionary['id']}, Purpose: {election_dictionary['purpose']}, Expired: {election_dictionary['expired']}")
    
    return elections

def get_election_info(id_election):

    try:
        election = election_contract.functions.getElectionInfo(int(id_election)).call()
        selction_info = {
            'id': election[0],
            'purpose': bytes32_to_string(election[1]),
            'expired': election[2]
        }
        return selction_info

    except ValueError:
        return None
    

# Function to update an election's expired field
def update_election_expired(election_id, new_expired):
    id = int(election_id)
    transaction = election_contract.functions.updateElectionExpired(id, new_expired).build_transaction({
        "from": account_elections,
        'gas': 200000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        "nonce": web3.eth.get_transaction_count(account_elections),
    })

    try:
        # Send the transaction
        transaction_hash = web3.eth.send_transaction(transaction)

        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

        if receipt["status"] == 1:
            return "Election expiration edited!"
        else:
            return "Failed to edit expiration election!"

    except ValueError:
        return "Failed to edit expiration election!"
    

# Function to update an election's purpose
def update_election_purpose(election_id, new_purpose):
    id = int(election_id)
    transaction = election_contract.functions.updateElectionPurpose(id, new_purpose).build_transaction({
        "from": account_elections,
        'gas': 200000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        "nonce": web3.eth.get_transaction_count(account_elections),
    })

    try:
        # Send the transaction
        transaction_hash = web3.eth.send_transaction(transaction)

        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

        if receipt["status"] == 1:
            return "Election purpose edited!"
        else:
            return "Failed to edit purpose election!"

    except ValueError:
        return "Failed to edit purpose election!"
    

def add_election(election_id, purpose):
    
    transaction = election_contract.functions.addElection(
        int(election_id),
        string_to_bytes32(purpose)
    ).build_transaction({
        "from": account_elections,
        'gas': 200000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        "nonce": web3.eth.get_transaction_count(account_elections),
    })

    try:
        # Send the transaction
        transaction_hash = web3.eth.send_transaction(transaction)

        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

        if receipt["status"] == 1:
            return "Election added!"
        else:
            return "Failed to add election!"

    except ValueError:
        return "Failed to add election!"
    

def add_candidate_to_election(id, name, lastname, manifesto, election_id):
    
    transaction = candidate_contract.functions.addCandidateToParty(
        int(id),
        string_to_bytes32(name),
        string_to_bytes32(lastname),
        string_to_bytes32(manifesto),
        int(election_id)
    ).build_transaction({
        "from": account_elections,
        'gas': 200000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        "nonce": web3.eth.get_transaction_count(account_elections),
    })

    try:
        # Send the transaction
        transaction_hash = web3.eth.send_transaction(transaction)

        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

        if receipt["status"] == 1:
            return "Candidate added!"
        else:
            return "Failed to add candidate!"

    except ValueError:
        return "Failed to add candidate!"
    

def get_all_candidates():
    candidates = candidate_contract.functions.getAllCandidates().call()
    return candidates

def get_user_info(email):
    
    encoded_email = string_to_bytes32(email)

    # checking if the user is a government employee or a citizen
    email_domain = email.split("@")[1]

    if email_domain == "government.it":
        account = account_government
    else:
        account = account_citizens

    # Call the contract function
    user_info = user_contract.functions.getUserInfo(encoded_email).call({
        "from": account,
    })

    # Now 'user_info' contains the returned values from the contract function
    name, lastname, is_admin = user_info

    # Convert bytes32 to string
    name = bytes32_to_string(name)
    lastname = bytes32_to_string(lastname)
    user = {
        'name': name,
        'lastname': lastname,
        'email': email, 
        'is_admin': is_admin
    }
    return user


def vote_candidate_by_election(email, candidate_id, election_id):
    
    encoded_email = string_to_bytes32(email)
    candidate_id = int(candidate_id)
    election_id = int(election_id)

    # Increment the vote count for the candidate
    transaction = voting_contract.functions.VoteCandidateByElection(encoded_email, candidate_id, election_id).build_transaction({
        "from": account_elections,
        'gas': 200000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        "nonce": web3.eth.get_transaction_count(account_elections),
    })

    try:
        # Send the transaction
        transaction_hash = web3.eth.send_transaction(transaction)

        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

        if receipt["status"] == 1:
            return True
        else:
            return False

    except ValueError:
        return False
    
def check_if_user_voted(email, id_election):
    encoded_email = string_to_bytes32(email)
    election_id = int(id_election)
    has_voted = voting_contract.functions.hasUserVoted(encoded_email, election_id).call()
    return has_voted