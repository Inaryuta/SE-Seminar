console.log("Register script loaded");

const registerForm = document.getElementById('registerForm');
const message = document.getElementById('message');

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    // Validación básica
    if (!username || !email || !password) {
        message.textContent = "All fields are required.";
        message.style.color = "red";
        return;
    }

    if (!validateEmail(email)) {
        message.textContent = "Invalid email format.";
        message.style.color = "red";
        return;
    }

    if (password.length < 6) {
        message.textContent = "Password must be at least 6 characters.";
        message.style.color = "red";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                email,
                password
            })
        });

        const data = await response.json();
        console.log("Response:", data);

        if (response.ok) {
            message.textContent = "Registration successful!";
            message.style.color = "green";
            setTimeout(() => {
                window.location.href = "./login.html";
            }, 1000);
        } else {
            message.textContent = data.message || "Registration failed.";
            message.style.color = "red";
        }

    } catch (error) {
        console.error("Connection error:", error);
        message.textContent = "Server connection failed.";
        message.style.color = "red";
    }
});

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email.toLowerCase());
}
