document.addEventListener("DOMContentLoaded", async () => {
    const exerciseSelects = document.querySelectorAll(".exercise-select");
    const addExerciseBtn = document.getElementById("addExerciseBtn");
    const saveSessionBtn = document.getElementById("saveSessionBtn");
    const exercisesContainer = document.getElementById("exercisesContainer");

    // 1. Cargar ejercicios para el select
    async function loadExercises() {
        try {
            const response = await fetch("http://127.0.0.1:8000/exercises/");
            const exercises = await response.json();

            exerciseSelects.forEach(select => {
                exercises.forEach(ex => {
                    const option = document.createElement("option");
                    option.value = ex.id;
                    option.textContent = ex.name;
                    select.appendChild(option);
                });
            });
        } catch (error) {
            console.error("Error loading exercises:", error);
        }
    }

    // 2. Agregar nuevo bloque de ejercicio
    addExerciseBtn.addEventListener("click", async () => {
        const block = document.createElement("div");
        block.classList.add("exercise-block");
        block.innerHTML = `
            <select class="exercise-select"></select>
            <input type="number" placeholder="Sets" class="sets" />
            <input type="number" placeholder="Reps" class="reps" />
            <input type="number" placeholder="Weight (kg)" class="weight" />
            <input type="number" placeholder="Distance (km)" class="distance" />
            <button class="remove-btn" style="color:red">Remove</button>
        `;
        exercisesContainer.appendChild(block);

        // Rellenar select con ejercicios
        try {
            const response = await fetch("http://127.0.0.1:8000/exercises/");
            const exercises = await response.json();
            const select = block.querySelector(".exercise-select");

            exercises.forEach(ex => {
                const option = document.createElement("option");
                option.value = ex.id;
                option.textContent = ex.name;
                select.appendChild(option);
            });
        } catch (error) {
            console.error("Error loading exercises in new block:", error);
        }

        block.querySelector(".remove-btn").addEventListener("click", () => {
            block.remove();
        });
    });

    // 3. Guardar sesión
    saveSessionBtn.addEventListener("click", async () => {
        const user_id = parseInt(localStorage.getItem("user_id"));
        const routineName = "Routine for " + new Date().toLocaleDateString();
        const date = document.getElementById("date").value;
        const duration = parseInt(document.getElementById("duration").value);
        const intensity = document.getElementById("intensity").value;
        const calories = parseInt(document.getElementById("calories").value);

        if (!user_id || !date || isNaN(duration)) {
            alert("Please fill in required fields.");
            return;
        }

        try {
            // Paso 1: Crear rutina
            const routineRes = await fetch("http://127.0.0.1:8000/routines/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id,
                    name: routineName,
                    date: new Date(date).toISOString()
                })
            });

            const routineData = await routineRes.json();
            const routine_id = routineData.id;

            // Paso 2: Crear sesión vinculada
            const sessionRes = await fetch("http://127.0.0.1:8000/routine_sessions/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id,
                    routine_id,
                    date: new Date(date).toISOString(),
                    duration_minutes: duration,
                    session_intensity: intensity,
                    calories_burned: calories
                })
            });

            const sessionData = await sessionRes.json();

            // Paso 3: Recoger todos los ejercicios añadidos y postear
            const exerciseBlocks = document.querySelectorAll(".exercise-block");

            for (let block of exerciseBlocks) {
                const exercise_id = parseInt(block.querySelector(".exercise-select").value);
                const sets = parseInt(block.querySelector(".sets").value);
                const reps = parseInt(block.querySelector(".reps").value);
                const weight = parseFloat(block.querySelector(".weight").value);
                const distance_km = parseFloat(block.querySelector(".distance").value);

                await fetch("http://127.0.0.1:8000/routine_exercises/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        routine_id,
                        exercise_id,
                        sets,
                        reps,
                        weight,
                        distance_km
                    })
                });
            }

            alert("Session saved successfully!");
            window.location.reload();

        } catch (error) {
            console.error("Error saving session:", error);
        }
    });

    loadExercises(); // Load ejercicios iniciales al cargar la página
});
