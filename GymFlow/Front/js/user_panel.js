const sessionList = document.querySelector("ul");
const userId = parseInt(localStorage.getItem("user_id"));
const startDateInput = document.getElementById("start-date");
const endDateInput = document.getElementById("end-date");
const filterBtn = document.getElementById("filter-btn");
const chartCanvas = document.getElementById("routineChart");
const topRoutineDisplay = document.getElementById("topRoutine");

let routineChartInstance;
let fetchedData = [];

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-GB", {
    day: "numeric", month: "short", year: "numeric"
  });
}

function isWithinDateRange(dateStr, startDate, endDate) {
  const sessionDate = new Date(dateStr);
  if (startDate && sessionDate < new Date(startDate)) return false;
  if (endDate && sessionDate > new Date(endDate)) return false;
  return true;
}

function estimateDuration(sets, reps) {
  if (!sets || !reps) return 0;
  return sets * reps * 0.5;
}

async function fetchUserRoutineData() {
  const response = await fetch(`http://127.0.0.1:8000/routines/user/${userId}`);
  const data = await response.json();
  fetchedData = data;
  return data;
}

function groupByRoutineSession(data, startDate, endDate) {
  const sessions = {};

  data.forEach(entry => {
    const sessionKey = `${entry.routine_id}_${entry.session_id}`;
    if (!sessions[sessionKey]) {
      if (startDate || endDate) {
        if (!isWithinDateRange(entry.session_date, startDate, endDate)) return;
      }

      sessions[sessionKey] = {
        routine_id: entry.routine_id,
        routine_name: entry.routine_name,
        session_date: entry.session_date,
        duration: entry.duration_minutes,
        exercises: []
      };
    }

    sessions[sessionKey].exercises.push(entry);
  });

  return Object.values(sessions);
}

async function renderSessionHistory(filter = false) {
  const startDate = startDateInput.value;
  const endDate = endDateInput.value;

  sessionList.innerHTML = "";

  const data = await fetchUserRoutineData();
  const groupedSessions = groupByRoutineSession(data, startDate, endDate);

  groupedSessions.forEach(session => {
    const dateFormatted = formatDate(session.session_date);
    const duration = session.duration || session.exercises.reduce((sum, ex) => sum + estimateDuration(ex.sets, ex.reps), 0);

    const exerciseDetails = session.exercises.map(ex => {
      if (ex.distance_km !== null) {
        return `${ex.exercise_name}: ${ex.distance_km} km`;
      } else {
        return `${ex.exercise_name}: ${ex.sets || 0}x${ex.reps || 0} (${ex.weight || 0} kg)`;
      }
    }).join("<br>");

    const li = document.createElement("li");
    li.className = "p-3 bg-white rounded-md shadow-sm border";
    li.innerHTML = `
      <div class="flex justify-between items-center">
        <span>${session.routine_name} • ${dateFormatted}</span>
        <span class="text-sm text-gray-500">${duration.toFixed(1)} min</span>
      </div>
      <div class="text-sm text-gray-600 mt-1">
        ${exerciseDetails}
      </div>
    `
    sessionList.appendChild(li);
  });
}

async function renderStatistics() {
  const data = fetchedData.length ? fetchedData : await fetchUserRoutineData();

  const routineCountMap = {};
  const caloriesMap = {};
  const durationList = new Set();
  const routineSessions = new Set();

  let totalCalories = 0;
  let totalDuration = 0;

  data.forEach(entry => {
    const routine = entry.routine_name;
    const sessionKey = `${entry.routine_id}_${entry.session_id}`;

    // Contador por rutina
    if (!routineCountMap[routine]) {
      routineCountMap[routine] = new Set();
      caloriesMap[routine] = 0;
    }

    routineCountMap[routine].add(entry.session_id);
    routineSessions.add(sessionKey);

    // Calorías acumuladas
    if (entry.calories_burned !== null) {
      totalCalories += entry.calories_burned;
      caloriesMap[routine] += entry.calories_burned;
    }

    // Duración acumulada por sesión
    if (!durationList.has(sessionKey)) {
      const dur = entry.duration_minutes || estimateDuration(entry.sets, entry.reps);
      totalDuration += dur;
      durationList.add(sessionKey);
    }
  });

  const routineLabels = Object.keys(routineCountMap);
  const routineCounts = routineLabels.map(r => routineCountMap[r].size);
  const calorieCounts = routineLabels.map(r => caloriesMap[r]);

  const max = Math.max(...routineCounts);
  const topRoutine = routineLabels[routineCounts.indexOf(max)];

  document.getElementById("topRoutine").textContent = `Most frequent routine: ${topRoutine} (${max} sessions)`;
  document.getElementById("totalCalories").textContent = totalCalories.toFixed(0);
  document.getElementById("avgDuration").textContent = (totalDuration / durationList.size).toFixed(1);
  document.getElementById("totalSessions").textContent = routineSessions.size;

  // Destruir gráfico previo si existe
  if (routineChartInstance) routineChartInstance.destroy();

  // Gráfico de sesiones por rutina
  routineChartInstance = new Chart(document.getElementById("routineChart"), {
    type: "bar",
    data: {
      labels: routineLabels,
      datasets: [{
        label: "Sessions per routine",
        data: routineCounts,
        backgroundColor: "rgba(59, 130, 246, 0.7)",
        borderColor: "rgba(59, 130, 246, 1)",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 }
        }
      }
    }
  });

  // gráfico calorías por rutina
  new Chart(document.getElementById("caloriesChart"), {
    type: "bar",
    data: {
      labels: routineLabels,
      datasets: [{
        label: "Calories burned",
        data: calorieCounts,
        backgroundColor: "rgba(16, 185, 129, 0.7)",
        borderColor: "rgba(5, 150, 105, 1)",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

renderSessionHistory();
renderStatistics();

filterBtn.addEventListener("click", () => {
  const start = startDateInput.value;
  const end = endDateInput.value;
  if (start && end && new Date(start) > new Date(end)) {
    alert("Start date must be before end date.");
    return;
  }
  renderSessionHistory(true);
});

document.getElementById("logoutBtn").addEventListener("click", () => {
    
    localStorage.removeItem("user_id");
    window.location.href = "login.html";
});
