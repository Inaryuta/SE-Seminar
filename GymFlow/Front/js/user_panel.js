const sessionList = document.querySelector("ul");
const userId = parseInt(localStorage.getItem("user_id"));
const startDateInput = document.getElementById("start-date");
const endDateInput = document.getElementById("end-date");
const filterBtn = document.getElementById("filter-btn");
const chartCanvas = document.getElementById("routineChart");
const topRoutineDisplay = document.getElementById("topRoutine");


async function fetchRoutines() {
  const response = await fetch("http://127.0.0.1:8000/routines");
  const routines = await response.json();
  return routines.filter(r => r.user_id === userId);
}

async function fetchRoutineSessions(routine_id) {
  const response = await fetch(`http://127.0.0.1:8000/routine-sessions/by-routine/${routine_id}`);
  return await response.json();
}

async function fetchRoutineExercises(session_id) {
  const response = await fetch(`http://127.0.0.1:8000/routine-exercises/${session_id}`);
  return await response.json();
}

async function fetchAllExercises() {
  const response = await fetch("http://127.0.0.1:8000/exercises");
  return await response.json();
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-GB", {
    day: "numeric", month: "short", year: "numeric"
  });
}

function estimateDuration(exercises) {
  if (!exercises || exercises.length === 0) return 0;
  return exercises.reduce((sum, ex) => sum + (ex.sets * ex.reps * 0.5), 0);
}

function isWithinDateRange(dateStr, startDate, endDate) {
  const sessionDate = new Date(dateStr);
  if (startDate && sessionDate < new Date(startDate)) return false;
  if (endDate && sessionDate > new Date(endDate)) return false;
  return true;
}

async function renderSessionHistory(filter = false) {
  const routines = await fetchRoutines();
  const allExercises = await fetchAllExercises();
  sessionList.innerHTML = "";

  const startDate = startDateInput.value;
  const endDate = endDateInput.value;

  for (const routine of routines) {
    const sessions = await fetchRoutineSessions(routine.id);
    const routineExercises = await fetchRoutineExercises(routine.id);

    for (const session of sessions) {
      if (filter && !isWithinDateRange(session.date, startDate, endDate)) continue;

      const dateFormatted = formatDate(session.date);
      
      const routineExercises = await fetchRoutineExercises(session.id);
      const duration = estimateDuration(routineExercises);

      const exerciseDetails = routineExercises.map(re => {
        const exercise = allExercises.find(ex => ex.id === re.exercise_id);
        return `${exercise?.name || 'Unknown'}: ${re.sets}x${re.reps}`;
      }).join("<br>");

      const li = document.createElement("li");
      li.className = "p-3 bg-white rounded-md shadow-sm border";
      li.innerHTML = `
        <div class="flex justify-between items-center">
          <span>${routine.name} • ${dateFormatted}</span>
          <span class="text-sm text-gray-500">${duration.toFixed(1)} min</span>
        </div>
        <div class="text-sm text-gray-600 mt-1">
          ${exerciseDetails}
        </div>
      `;
      sessionList.appendChild(li);
    }
  }
}

let routineChartInstance;

async function renderStatistics() {
  const routines = await fetchRoutines();

  const routineCountMap = {};
  for (const routine of routines) {
    const sessions = await fetchRoutineSessions(routine.id);
    routineCountMap[routine.name] = (routineCountMap[routine.name] || 0) + sessions.length;
  }

  const labels = Object.keys(routineCountMap);
  const data = Object.values(routineCountMap);

  const max = Math.max(...data);
  const topIndex = data.indexOf(max);
  const topRoutineName = labels[topIndex];
  topRoutineDisplay.textContent = `Most frequent routine: ${topRoutineName} (${max} sessions)`;

  //Avoid overposition
  if (routineChartInstance) {
    routineChartInstance.destroy();
  }

  routineChartInstance = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Sessions per routine",
        data,
        backgroundColor: "rgba(59, 130, 246, 0.7)",
        borderColor: "rgba(59, 130, 246, 1)",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
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


