// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

contract CandidateContract {

    // Contract's Owner address
    address public election;

    // Struct to represent candidate data
    struct Candidate {
        int id;
        bytes32 name;
        bytes32 lastname;
        bytes32 manifesto;
        int votes;
        int election_id;
    }

    // Mapping to store candidates
    mapping (int => Candidate) public candidates;

    int[] public candidateIds;

    // Event to register a candidate
    event CandidateRegistered(bytes32 _candidateName, bytes32 _lastname, bytes32 _manifesto, int election_id);
    

    constructor() {
        // Set owner to contract deployer.
        election = msg.sender;
    }

    function addCandidateToParty(int id_candidate, bytes32 _candidateName, bytes32 _lastname, bytes32 _manifesto, int election_id) public {
        // Check if the candidate already exists
        require(candidates[id_candidate].id == 0, "Candidate with this ID already exists");

        // Create a new candidate
        Candidate memory newCandidate = Candidate({
            id: id_candidate,
            name: _candidateName,
            lastname: _lastname,
            manifesto: _manifesto,
            votes: 0,
            election_id: election_id
        });

        candidates[id_candidate] = newCandidate;
        candidateIds.push(id_candidate);

        emit CandidateRegistered(_candidateName, _lastname, _manifesto, election_id);
    }


    // Get all candidates
    function getAllCandidates() public view returns (Candidate[] memory) {
        uint candiateCount = candidateIds.length;
        Candidate[] memory allCandidates = new Candidate[](candiateCount);

        for (uint i = 0; i < candiateCount; i++) {
            allCandidates[i] = candidates[candidateIds[i]];
        }

        return allCandidates;
    }

    // Function to increment the vote count for a candidate
    function incrementCandidateVotes(int candidate_id) public {
        // Check if the candidate exists
        require(candidates[candidate_id].id != 0, "Candidate with the provided ID does not exist");

        // Increment the vote count
        candidates[candidate_id].votes++;
    }

}