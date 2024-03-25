document.getElementById('fetchData').addEventListener('click', function() {
    var dataType = document.getElementById('dataType').value;
    var country = document.getElementById('countrySelect').value;

    // Create a FormData object and append the data
    var formData = new FormData();
    formData.append('dataType', dataType);
    formData.append('countrySelect', country);

    // Show loading spinner
    document.getElementById('loading').style.display = 'block';

    // Fetch API to send the data to the Flask app
    fetch('http://127.0.0.1:5000/fetch_data', { // Using a relative URL
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
        })
    .then(data => {
        // Hide loading spinner
        document.getElementById('loading').style.display = 'none';

        if (data.error && data.error.includes('No program found')) {
            console.log(`Directory: ${data.directory}`);
        }

        console.log(data); // Log the response from the Flask app
        document.getElementById('status').innerText = data.message || data.error;

        // If data.message is present, assume it contains the file content
        if (data.message) {
            // Create a Blob from the file content
            var blob = new Blob([data.message], { type: 'application/pdf' });

        }
    })
    .catch(error => {
        // Hide loading spinner on error
        document.getElementById('loading').style.display = 'none';

        console.error('Fetch Error:', error);
        document.getElementById('status').innerText = 'Error occurred. Please check console for details.';
    });

    // Save the last selected values to localStorage
    localStorage.setItem('lastSelectedDataType', dataType);
    localStorage.setItem('lastSelectedCountry', country);
}); 

document.getElementById('downloadFile').addEventListener('click', function() {
    var dataType = document.getElementById('dataType').value;
    var country = document.getElementById('countrySelect').value;
    var today = new Date().toISOString().slice(0,10); // Get today's date in format "YYYY-MM-DD"

    // Construct the URL for the file download
    var downloadUrl = `/output/${dataType}/${dataType}_${country}_${today}.pdf`;

    // Create a temporary anchor element
    var downloadLink = document.createElement("a");
    downloadLink.href = downloadUrl;
    downloadLink.download = `${dataType}_${country}_${today}.pdf`;
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);

    // Trigger the download by programmatically clicking the link
    downloadLink.click();

    // Remove the temporary link after triggering the download
    document.body.removeChild(downloadLink);
});



// Set initial values for user selections from localStorage or use default values
document.getElementById('dataType').value = localStorage.getItem('lastSelectedDataType') || 'select';
document.getElementById('countrySelect').value = localStorage.getItem('lastSelectedCountry') || 'select';

// Display the download file button
document.getElementById('downloadFile').style.display = 'block';