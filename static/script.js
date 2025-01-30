document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (!username || !password) {
            alert('Please fill in both fields.');
            return; // Stop further execution
        }

        // Here's where you'd handle the login logic:
        // - Send a request to your server (e.g., using fetch or AJAX)
        // - Verify user credentials
        // - Redirect or display an error message

        // For demo purposes, just log the values to the console:
        console.log(`Username: ${username}, Password: ${password}`);
    });
});