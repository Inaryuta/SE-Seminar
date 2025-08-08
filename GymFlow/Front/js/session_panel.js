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

            exercises.forEach(ex => {
                exerciseDataMap.set(ex.id.toString(), ex);
            });

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
                option.dataset.type = ex.type;
                select.appendChild(option);
            });

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
                    // Mostrar fuerza/core etc
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

        // Obtener valores del formulario
        const routineNameInput = document.getElementById("routineName");
        let routineName = routineNameInput ? routineNameInput.value.trim() : "";
        if (!routineName) routineName = "Routine for " + new Date().toLocaleDateString();

        const rawDate = document.getElementById("date").value;
        if (!rawDate) {
            alert("Por favor selecciona una fecha y hora.");
            return;
        }

        // Formatear fecha sin zona horaria: YYYY-MM-DDTHH:MM:SS
        function formatDateNoTZ(dateStr) {
            const d = new Date(dateStr);
            const YYYY = d.getFullYear();
            const MM = String(d.getMonth() + 1).padStart(2, "0");
            const DD = String(d.getDate()).padStart(2, "0");
            const hh = String(d.getHours()).padStart(2, "0");
            const mm = String(d.getMinutes()).padStart(2, "0");
            const ss = String(d.getSeconds()).padStart(2, "0");
            return `${YYYY}-${MM}-${DD}T${hh}:${mm}:${ss}`;
        }

        const dateIsoNoTZ = formatDateNoTZ(rawDate);

        const duration = parseInt(document.getElementById("duration").value);
        const intensity = document.getElementById("intensity").value.trim();
        const calories = parseFloat(document.getElementById("calories").value);

        // Validaciones básicas
        if (isNaN(duration) || duration <= 0) {
            alert("Por favor ingresa una duración válida (minutos).");
            return;
        }
        if (!intensity) {
            alert("Por favor ingresa la intensidad de la sesión.");
            return;
        }
        if (isNaN(calories) || calories < 0) {
            alert("Por favor ingresa las calorías quemadas (número >= 0).");
            return;
        }

        // Validación de que haya al menos un ejercicio y que cada ejercicio sea válido
        const exerciseBlocks = document.querySelectorAll(".exercise-block");
        if (!exerciseBlocks || exerciseBlocks.length === 0) {
            alert("Agrega al menos un ejercicio a la rutina.");
            return;
        }

        for (let block of exerciseBlocks) {
            const selectEl = block.querySelector(".exercise-select");
            if (!selectEl) {
            alert("Hay un bloque de ejercicio mal formado.");
            return;
            }
            const exercise_id = parseInt(selectEl.value);
            const exercise = exerciseDataMap.get(String(exercise_id));
            if (!exercise) {
            alert("Selecciona un ejercicio válido en todos los bloques.");
            return;
            }

            if (exercise.type === "Cardio") {
            const distance_km = parseFloat(block.querySelector(".distance").value);
            if (isNaN(distance_km) || distance_km <= 0) {
                alert(`Por favor ingresa una distancia válida (km) para ${exercise.name}.`);
                return;
            }
            } else {
            const sets = parseInt(block.querySelector(".sets").value);
            const reps = parseInt(block.querySelector(".reps").value);
            const weight = parseFloat(block.querySelector(".weight").value);
            if (isNaN(sets) || sets <= 0 || isNaN(reps) || reps <= 0 || isNaN(weight) || weight < 0) {
                alert(`Por favor ingresa sets, reps y peso válidos para ${exercise.name}.`);
                return;
            }
            }
        }

        // Todo validado enviar al servidor
        try {
            // 1 Crear Routine
            const routineRes = await fetch("http://127.0.0.1:8000/routines/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id,
                name: routineName,
                date: dateIsoNoTZ
            })
            });

            if (!routineRes.ok) {
            const errText = await routineRes.text();
            alert(`Error creando rutina: ${routineRes.status} ${errText}`);
            return;
            }
            const createdRoutine = await routineRes.json();
            const routine_id = createdRoutine.id;

            // 2 Crear RoutineSession
            const sessionRes = await fetch("http://127.0.0.1:8000/routine-sessions/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id,
                routine_id,
                date: dateIsoNoTZ,
                duration_minutes: duration,
                session_intensity: intensity,
                calories_burned: calories
            })
            });

            if (!sessionRes.ok) {
            const errText = await sessionRes.text();
            alert(`Error creando sesión: ${sessionRes.status} ${errText}`);
            return;
            }
            const sessionData = await sessionRes.json();

            // 3 Crear RoutineExercises
            for (let block of exerciseBlocks) {
            const exercise_id = parseInt(block.querySelector(".exercise-select").value);
            const exercise = exerciseDataMap.get(String(exercise_id));

            let sets = null, reps = null, weight = null, distance_km = null;
            if (exercise.type === "Cardio") {
                distance_km = parseFloat(block.querySelector(".distance").value);
            } else {
                sets = parseInt(block.querySelector(".sets").value);
                reps = parseInt(block.querySelector(".reps").value);
                weight = parseFloat(block.querySelector(".weight").value);
            }

            const reRes = await fetch("http://127.0.0.1:8000/routine-exercises/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ routine_id, exercise_id, sets, reps, weight, distance_km })
            });

            if (!reRes.ok) {
                const errText = await reRes.text();
                alert(`Error agregando ejercicio: ${reRes.status} ${errText}`);
                return;
            }
            }

            alert("Sesión guardada con éxito.");
            window.location.reload();
        } catch (err) {
            console.error("Error saving session:", err);
            alert("Ocurrió un error al guardar la sesión. Revisa la consola del servidor para más detalles.");
        }
        });

    loadExercises();
});
