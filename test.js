import fetch from 'node-fetch'
async function sendNumber(number) {
    const url = 'http://localhost:8000'; // URL of your backend server
    const data = { number };

    try {
        const response = await fetch(url, {
            method: 'POST', // HTTP method
            headers: {
                'Content-Type': 'application/json', // Indicate we're sending JSON data
            },
            body: JSON.stringify(data), // Convert JavaScript object to JSON string
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const responseData = await response.json();
        console.log('Response from the server:', responseData);
    } catch (error) {
        console.error('Failed to send number:', error);
    }
}

// Example: Send the number 123 to the backend
sendNumber(123);