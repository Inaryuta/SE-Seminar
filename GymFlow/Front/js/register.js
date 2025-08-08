console.log("Register script loaded");

const registerForm = document.getElementById("registerForm");
const message = document.createElement("p");
message.classList.add("text-sm", "mt-2");
registerForm.appendChild(message);

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const usernameValue = document.getElementById("username").value.trim();
    const emailValue = document.getElementById("email").value.trim();
    const passwordValue = document.getElementById("password").value.trim();

    message.textContent = "";
    message.style.color = "";

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!usernameValue || usernameValue.length < 3) {
        message.textContent = "Username must be at least 3 characters.";
        message.style.color = "red";
        return;
    }

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
        const response = await fetch("http://127.0.0.1:8000/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: usernameValue,
                email: emailValue,
                password: passwordValue
            })
        });

        const data = await response.json();
        console.log("Register response:", data);

        if (response.ok) {
            message.textContent = "Registration successful!";
            message.style.color = "green";

            // Guardar usuario en sesión
            sessionStorage.setItem("user", JSON.stringify(data));

            // Redirigir a login para que pueda guardar su id en local storage
            window.location.href = "login.html.html";
        } else {
            message.textContent = data.detail || "Registration failed.";
            message.style.color = "red";
        }

    } catch (error) {
        console.error("Connection error:", error);
        alert("Could not connect to server.");
    }
});
