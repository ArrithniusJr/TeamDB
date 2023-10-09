function login() {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    // Send a POST request to the server for login
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("message").innerText = "Login successful!";
        } else {
            document.getElementById("message").innerText = "Login failed. Please check your credentials.";
        }
    });
}

function register() {
    const newUsername = document.getElementById("registerUsername").value;
    const newPassword = document.getElementById("registerPassword").value;

    // Send a POST request to the server for registration
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ newUsername, newPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("message").innerText = "Registration successful!";
        } else {
            document.getElementById("message").innerText = "Registration failed. Username may already exist.";
        }
    });
}

