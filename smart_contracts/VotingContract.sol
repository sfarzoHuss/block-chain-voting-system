// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

import "./candidates.sol"; // Import the CandidateContract

contract VotingContract {

    CandidateContract private candidate_contract;

    // Contract's Owner address
    address public election;

    // Struct to represent candidate data
    struct Vote {
        bytes32 email;
        int candidate_id;
        int election_id;
        bool voted;
    }

    // Mapping to store parties
    mapping (bytes32 => Vote) public votes;    

    constructor(address _candidateContractAddress) {
        // Set owner to contract deployer.
        election = msg.sender;

        candidate_contract = CandidateContract(_candidateContractAddress);
    }

    // Function to add a new election
    function VoteCandidateByElection(bytes32 _email, int candidate_id, int election_id) public {

        // Generate a unique code using the election's address and timestamp
        bytes32 uniqueCode = keccak256(abi.encodePacked(_email, election_id));

        // Check if the vote already exists
        require(votes[uniqueCode].voted == false, "The current user already voted for the current election.");

        // Create a new election
        Vote memory newVote = Vote({
            email: _email,
            candidate_id: candidate_id,
            election_id: election_id,
            voted: true
        });
        votes[uniqueCode] = newVote;

        // Increment the vote count for the candidate
        candidate_contract.incrementCandidateVotes(candidate_id);
    }

    // Function to check if a user has already voted
    function hasUserVoted(bytes32 _email, int election_id) public view returns (bool) {
        bytes32 uniqueCode = keccak256(abi.encodePacked(_email, election_id));
        return votes[uniqueCode].voted;
    }
}

