$("#add-election").click(function() {
    var addButton = document.getElementById("add-election");
    if ($("#add-div").css("display") === "none") {
        addButton.textContent = "X";
        $("#add-div").slideDown();
    } else {
        addButton.textContent = "Add Election";
        $("#add-div").slideUp();
        $("#add-div").css("display", "none");
    }
    
});

$("#edit-election").click(function() {
    var editButton = document.getElementById("edit-election");
    if ($("#edit-div").css("display") === "none") {
        editButton.textContent = "X";
        $("#edit-div").slideDown();
    } else {
        editButton.textContent = "Edit Election";
        $("#edit-div").slideUp();
        $("#edit-div").css("display", "none");
    }
});

$('#candidateSelect').change(function () {
    // Get the selected option
    var selectedOption = $(this).find(':selected');

    // Set the title and body of the modal
    $('#candidateModalLabel').text(selectedOption.data('name'));
    $('#candidateModalBody').text(selectedOption.data('manifesto'));

    // Store the selected candidate ID for voting
    var selectedCandidateId = $(this).val();
    $('#voteButton').data('candidateId', selectedCandidateId);

    // Open the modal
    $('#candidateModal').modal('show');
});

$("#add-candidate").click(function() {
    var addButton = document.getElementById("add-candidate");
    if ($("#add-candidate-div").css("display") === "none") {
        addButton.textContent = "X";
        $("#add-candidate-div").slideDown();
    } else {
        addButton.textContent = "Add Party";
        $("#add-candidate-div").slideUp();
        $("#add-candidate-div").css("display", "none");
    }
    
});

// Add a click event listener to the "Vote" button
$('#voteButton').click(function () {
    // Get the selected candidate ID
    var selectedCandidateId = $(this).data('candidateId');

    // Redirect to the vote URL with the selected candidate ID
    window.location.href = '/vote/' + selectedCandidateId;
});