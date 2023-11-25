// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

contract ElectionContract {

    // Contract's Owner address
    address public election;

    // Struct to represent candidate data
    struct Election {
        int election_id;
        bytes32 purpose;
        bool expired;
    }

    // Mapping to store parties
    mapping (int => Election) public elections;

    int[] public electionIds;

    // Event to create an election
    event ElectionCreated(int election_id, bytes32 purpose);
    

    constructor() {
        // Set owner to contract deployer.
        election = msg.sender;
    }

    // Function to add a new election
    function addElection(int election_id, bytes32 purpose) public {

        // Check if the election already exists
        require(elections[election_id].election_id == 0, "Election having the sent id already exists");

        // Create a new election
        Election memory newElection = Election({
            election_id: election_id,
            purpose: purpose,
            expired: false
        });
        elections[election_id] = newElection;

        electionIds.push(election_id);

        // Emit an event to log the addition of a new election
        emit ElectionCreated(election_id, purpose);
    }

   
    // Get all election ids
    function getAllElectionIds() public view returns (int[] memory) {
        return electionIds;
    }

    // Get all elections
    function getAllElections() public view returns (Election[] memory) {
        uint electionCount = electionIds.length;
        Election[] memory allElections = new Election[](electionCount);

        for (uint i = 0; i < electionCount; i++) {
            allElections[i] = elections[electionIds[i]];
        }

        return allElections;
    }

    // Get election information by election id
    function getElectionInfo(int election_id) public view returns (Election memory) {
        
        require(elections[election_id].election_id != 0, "Election with the provided id does not exist");
        return elections[election_id];
    }

    // Function to update an election's expired field
    function updateElectionExpired(int election_id, bool newExpired) public {

        // Check if the election exists
        require(elections[election_id].election_id != 0, "Election with the provided id does not exist");

        // Update the expired field
        elections[election_id].expired = newExpired;
    }

    // Function to update an election's purpose
    function updateElectionPurpose(int election_id, bytes32 newPurpose) public {

        // Check if the election exists
        require(elections[election_id].election_id != 0, "Election with the provided id does not exist");

        // Update the purpose
        elections[election_id].purpose = newPurpose;
    }

}

