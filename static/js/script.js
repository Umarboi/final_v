// Function to scroll to the top of the page
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' 
    });
}


window.addEventListener('scroll', function() {
    
    const upButton = document.getElementById('upButton');


    if (window.scrollY > 20) {
        upButton.style.display = 'block';
    } else {
        upButton.style.display = 'none';
    }
});


//document.getElementById("testSuggestion").addEventListener("click", function () {
//    window.location.href = "/predict";
//});
function getTest() {
    // Get selected symptoms
    var selectedSymptoms = $("input[type='checkbox']:checked").map(function() {
        return $(this).val();
    }).get();

    // Get fever reading
    var feverReading = parseFloat($("#fever").val());

    console.log(selectedSymptoms)
    console.log(feverReading)

    // Check if feverReading is a valid number
    if (isNaN(feverReading)) {
        console.error("Fever reading is not a valid number.");
        return;
    }

    
    var data = {
        symptoms: selectedSymptoms,
        fever: feverReading
    };

    // Make AJAX request to Flask server
    $.ajax({
        url: "/predict",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function(response) {
            console.log(response)
            $("#testSuggestion").text("Suggested Tests : " + response.suggested_tests);
            $("#predictDiseseae").text("Predicted illness: " + response.predicted_disease);
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
}


document.getElementById("symptomInput").addEventListener("input", function () {
    var input, filter, symptoms, labels, i;

    input = document.getElementById("symptomInput");
    filter = input.value.toUpperCase();
    symptoms = document.getElementById("symptomsList");
    labels = symptoms.getElementsByTagName("label");

    for (i = 0; i < labels.length; i++) {
        var symptomText = labels[i].innerText.toUpperCase();
        if (symptomText.indexOf(filter) > -1) {
            labels[i].style.display = "";
        } else {
            labels[i].style.display = "none";
        }
    }
});




