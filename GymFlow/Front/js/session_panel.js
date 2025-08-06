document.addEventListener("DOMContentLoaded", async () => {
    const exerciseSelects = document.querySelectorAll(".exercise-select");
    const addExerciseBtn = document.getElementById("addExerciseBtn");
    const saveSessionBtn = document.getElementById("saveSessionBtn");
    const exercisesContainer = document.getElementById("exercisesContainer");

    // 1. Cargar ejercicios para el select
    let exerciseDataMap = new Map();

    async function loadExercises() {
        try {
            const response = await fetch("http://127.0.0.1:8000/exercises/");
            const exercises = await response.json();

            // Guardar en map por ID
            exercises.forEach(ex => {
                exerciseDataMap.set(ex.id.toString(), ex); // clave como string
            });

            // Rellenar selects existentes
            exerciseSelects.forEach(select => {
                exercises.forEach(ex => {
                    const option = document.createElement("option");
                    option.value = ex.id;
                    option.textContent = ex.name;
                    select.appendChild(option);
                });

                select.addEventListener("change", () => {
                    handleExerciseChange(select);
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
            <input type="number" placeholder="Sets" class="sets" style="display:none;" />
            <input type="number" placeholder="Reps" class="reps" style="display:none;" />
            <input type="number" placeholder="Weight (kg)" class="weight" style="display:none;" />
            <input type="number" placeholder="Distance (km)" class="distance" style="display:none;" />
            <button class="remove-btn" style="color:red">Remove</button>
        `;
        exercisesContainer.appendChild(block);

        // Cargar ejercicios y asociar lógica
        try {
            const response = await fetch("http://127.0.0.1:8000/exercises/");
            const exercises = await response.json();
            const select = block.querySelector(".exercise-select");

            exercises.forEach(ex => {
                const option = document.createElement("option");
                option.value = ex.id;
                option.textContent = ex.name;
                option.dataset.type = ex.type; // Guardamos el tipo en el option
                select.appendChild(option);
            });

            // Detectar cambio en el select y mostrar los campos apropiados
            select.addEventListener("change", () => {
                const selectedOption = select.options[select.selectedIndex];
                const type = selectedOption.dataset.type;

                const sets = block.querySelector(".sets");
                const reps = block.querySelector(".reps");
                const weight = block.querySelector(".weight");
                const distance = block.querySelector(".distance");

                if (type === "Cardio") {
                    // Solo mostrar distancia
                    sets.style.display = "none";
                    reps.style.display = "none";
                    weight.style.display = "none";
                    distance.style.display = "inline-block";
                } else {
                    // Mostrar fuerza/core, etc.
                    sets.style.display = "inline-block";
                    reps.style.display = "inline-block";
                    weight.style.display = "inline-block";
                    distance.style.display = "none";
                }
            });

            // Disparar el evento por defecto por si hay opción seleccionada
            select.dispatchEvent(new Event("change"));
        } catch (error) {
            console.error("Error loading exercises in new block:", error);
        }

        block.querySelector(".remove-btn").addEventListener("click", () => {
            block.remove();
        });
    });

    function handleExerciseChange(selectElement) {
        const selectedId = selectElement.value;
        const exercise = exerciseDataMap.get(selectedId);
        if (!exercise) return;

        const parent = selectElement.closest(".exercise-block");
        const sets = parent.querySelector(".sets");
        const reps = parent.querySelector(".reps");
        const weight = parent.querySelector(".weight");
        const distance = parent.querySelector(".distance");

        // Resetear visibilidad
        sets.style.display = "none";
        reps.style.display = "none";
        weight.style.display = "none";
        distance.style.display = "none";

        if (exercise.type === "Cardio") {
            distance.style.display = "inline-block";
        } else if (exercise.type === "Strength" || exercise.type === "Core") {
            sets.style.display = "inline-block";
            reps.style.display = "inline-block";
            weight.style.display = "inline-block";
        }
    }

    // 3. Guardar sesión
    saveSessionBtn.addEventListener("click", async () => {
        const user_id = parseInt(localStorage.getItem("user_id"));
        if (!user_id || isNaN(user_id)) {
            alert("Debes iniciar sesión para continuar.");
            return;
        }
        const routineName = "Routine for " + new Date().toLocaleDateString();
        const rawDate = document.getElementById("date").value;

        function formatDateWithoutTimezone(dateStr) {
            const date = new Date(dateStr);
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            return `${year}-${month}-${day}`;
        }

        const date = rawDate ? formatDateWithoutTimezone(rawDate) : null;
        const duration = parseInt(document.getElementById("duration").value);
        const intensity = document.getElementById("intensity").value;
        const calories = parseInt(document.getElementById("calories").value);

        try {
            // Paso 1: Crear rutina
            const routineRes = await fetch("http://127.0.0.1:8000/routines/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id,
                    name: routineName,
                    date: date
                })
            });

            const routineData = {
                user_id: user_id,
                name: "Exercise Session",
                date: new Date(date).toISOString()
            };
            const createdRoutine = await routineRes.json();
            const routine_id = createdRoutine.id;

            // Paso 2: Crear sesión vinculada
            const sessionRes = await fetch("http://127.0.0.1:8000/routine-sessions/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: user_id,
                    routine_id: routine_id,
                    date: date,
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
                const exercise = exerciseDataMap.get(exercise_id.toString());

                if (!exercise) {
                    alert("Invalid exercise selected.");
                    return;
                }

                let sets = null;
                let reps = null;
                let weight = null;
                let distance_km = null;

                if (exercise.type === "Cardio") {
                    distance_km = parseFloat(block.querySelector(".distance").value);
                    if (isNaN(distance_km) || distance_km <= 0) {
                        alert(`Please enter a valid distance (km) for ${exercise.name}.`);
                        return;
                    }
                } else {
                    sets = parseInt(block.querySelector(".sets").value);
                    reps = parseInt(block.querySelector(".reps").value);
                    weight = parseFloat(block.querySelector(".weight").value);

                    if (isNaN(sets) || sets <= 0 || isNaN(reps) || reps <= 0 || isNaN(weight) || weight < 0) {
                        alert(`Please enter valid sets, reps, and weight for ${exercise.name}.`);
                        return;
                    }
                }

                await fetch("http://127.0.0.1:8000/routine-exercises/", {
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

    loadExercises();
});
