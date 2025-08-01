console.log("Login script loaded");

const loginForm = document.getElementById('loginForm');
const message = document.createElement("p");
message.classList.add("text-sm", "mt-2");
loginForm.appendChild(message);

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    // Get the values
    const emailValue = document.getElementById('email').value.trim();
    const passwordValue = document.getElementById('password').value.trim();

    // Clear previous message
    message.textContent = "";
    message.style.color = "";

    // Frontend validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(emailValue)) {
        message.textContent = "Please enter a valid email.";
        message.style.color = "red";
        return;
    }

    if (passwordValue.length < 6) {
        message.textContent = "Password must be at least 6 characters.";
        message.style.color = "red";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: emailValue,
                password: passwordValue
            })
        });

        const data = await response.json();
        console.log("Response data:", data);

        if (response.ok) {
            message.textContent = "Login successful!";
            message.style.color = "green";

            // Store user data in session
            sessionStorage.setItem("user", JSON.stringify(data.user));

            // Redirection
            window.location.href = "index.html";

        } else {
            message.textContent = data.message || "Invalid credentials.";
            message.style.color = "red";
        }

    } catch (error) {
        console.error("Connection error:", error);
        alert("Could not connect to server.");
    }
});
