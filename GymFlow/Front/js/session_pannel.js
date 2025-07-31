document.addEventListener("DOMContentLoaded", () => {
  const addExerciseBtn = document.getElementById("addExerciseBtn");
  const exercisesContainer = document.getElementById("exercisesContainer");
  const form = document.getElementById("exerciseForm");

  // Lista de ejercicios
  const exercisesList = [
    "Squats",
    "Deadlift",
    "Bench Press",
    "Overhead Press",
    "Pull-ups",
    "Running"
  ];

  // Crear una fila de ejercicio
  function createExerciseRow() {
    const row = document.createElement("div");
    row.className = "grid grid-cols-6 gap-2 mb-2 items-center";

    // Selector de ejercicio
    const select = document.createElement("select");
    select.className = "border-gray-300 rounded-md col-span-2 p-1";
    exercisesList.forEach(name => {
      const opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name;
      select.appendChild(opt);
    });

    // Inputs
    const setsInput = createNumberInput("Sets");
    const repsInput = createNumberInput("Reps");
    const weightInput = createNumberInput("Weight (kg)");
    const distanceInput = createNumberInput("Distance (km)");
    distanceInput.style.display = "none"; // Oculto por defecto

    // Botón eliminar
    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "text-red-600 hover:underline text-sm";
    deleteBtn.textContent = "Remove";
    deleteBtn.onclick = () => row.remove();

    // Mostrar u ocultar inputs según tipo de ejercicio
    select.addEventListener("change", () => {
      if (select.value === "Running") {
        setsInput.style.display = "none";
        repsInput.style.display = "none";
        weightInput.style.display = "none";
        distanceInput.style.display = "block";
      } else {
        setsInput.style.display = "block";
        repsInput.style.display = "block";
        weightInput.style.display = "block";
        distanceInput.style.display = "none";
      }
    });

    row.appendChild(select);
    row.appendChild(setsInput);
    row.appendChild(repsInput);
    row.appendChild(weightInput);
    row.appendChild(distanceInput);
    row.appendChild(deleteBtn);

    return row;
  }

  // Crear input numérico con validación básica
  function createNumberInput(placeholder) {
    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = placeholder;
    input.className = "border-gray-300 rounded-md p-1";
    input.oninput = () => {
      const val = input.value.trim();
      if (val !== "" && (isNaN(val) || Number(val) < 0)) {
        input.classList.add("border-red-500");
      } else {
        input.classList.remove("border-red-500");
      }
    };
    return input;
  }

  // Agregar ejercicio
  addExerciseBtn.addEventListener("click", () => {
    const row = createExerciseRow();
    exercisesContainer.appendChild(row);
  });

  // Manejar envío
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const [date, duration, intensity, calories] = form.querySelectorAll("input");

    // Validar datos de cabecera
    if (!date.value) return alert("Date is required.");
    if (isNaN(duration.value) || duration.value < 0) return alert("Invalid duration.");
    if (isNaN(calories.value) || calories.value < 0) return alert("Invalid calories burned.");
    if (!intensity.value.trim()) return alert("Intensity is required.");

    const exerciseSession = {
      user_id: 1, // cambiar según login real
      exercise_id: null, // opcional en resumen general
      date: date.value,
      duration_minutes: Number(duration.value),
      session_intensity: intensity.value,
      distance_km: null, // opcional aquí
      calories_burned: Number(calories.value)
    };

    const routineExercises = [];
    const exerciseRows = exercisesContainer.querySelectorAll(".grid");

    exerciseRows.forEach(row => {
      const [select, sets, reps, weight, distance] = row.querySelectorAll("select, input");

      const isRunning = select.value === "Running";
      const obj = {
        routine_id: 1, // temporal o dummy
        exercise_id: getExerciseId(select.value),
        order_index: routineExercises.length + 1,
        sets: isRunning ? null : Number(sets.value),
        reps: isRunning ? null : Number(reps.value),
        weight: isRunning ? null : Number(weight.value),
        distance_km: isRunning ? Number(distance.value) : null
      };

      routineExercises.push(obj);
    });

    const payload = {
      exercise_session: exerciseSession,
      routine_exercises: routineExercises
    };

    console.log("Generated JSON:", JSON.stringify(payload, null, 2));
    alert("Session ready to be sent. Check console for JSON.");
  });

  // Simular conversión nombre → ID (esto sería de backend o catálogo real)
  function getExerciseId(name) {
    const map = {
      "Squats": 1,
      "Deadlift": 2,
      "Bench Press": 3,
      "Overhead Press": 4,
      "Pull-ups": 5,
      "Running": 6
    };
    return map[name] || 0;
  }
});
