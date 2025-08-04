console.log("Login script loaded");

const loginForm = document.getElementById('loginForm');
const message = document.createElement("p");
message.classList.add("text-sm", "mt-2");
loginForm.appendChild(message);

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const emailValue = document.getElementById('email').value.trim();
    const passwordValue = document.getElementById('password').value.trim();

    message.textContent = "";
    message.style.color = "";

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
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
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

            // Guardar los datos del usuario en sesión
            sessionStorage.setItem("user", JSON.stringify(data));

            // Redireccionar
            window.location.href = "index.html";

        } else {
            message.textContent = data.detail || "Invalid credentials.";
            message.style.color = "red";
        }

    } catch (error) {
        console.error("Connection error:", error);
        alert("Could not connect to server.");
    }
});
