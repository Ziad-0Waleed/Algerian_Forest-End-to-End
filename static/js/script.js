document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    // 1. Stop the HTML form from refreshing the page
    event.preventDefault();

    const form = event.target;
    const submitBtn = document.getElementById('submit-btn');
    const resultBox = document.getElementById('result-box');

    // 2. Visual feedback: Change button to "Loading..." and disable it
    submitBtn.innerText = 'Calculating...';
    submitBtn.disabled = true;
    resultBox.style.display = 'none';
    resultBox.className = 'result-box'; // Reset classes

    // 3. Gather all the data from the form inputs
    const formData = new FormData(form);

    // Convert FormData to a standard JSON object
    const dataObject = {};
    formData.forEach((value, key) => {
        dataObject[key] = parseFloat(value); // Convert string inputs to floats for the API
    });

    try {
        // 4. Send the data to your API endpoint
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataObject)
        });

        const result = await response.json();

        // 5. Display the result
        if (result.status === 'success') {
            resultBox.innerHTML = `Predicted FWI: <span>${result.prediction}</span>`;
            resultBox.style.display = 'block';
        } else {
            // Handle errors thrown by the backend
            resultBox.innerHTML = `Error: ${result.message}`;
            resultBox.classList.add('error-box');
            resultBox.style.display = 'block';
        }

    } catch (error) {
        // Handle network errors
        console.error('Error:', error);
        resultBox.innerHTML = 'An error occurred while connecting to the server.';
        resultBox.classList.add('error-box');
        resultBox.style.display = 'block';
    } finally {
        // 6. Reset the button back to normal
        submitBtn.innerText = 'Predict FWI';
        submitBtn.disabled = false;
    }
});