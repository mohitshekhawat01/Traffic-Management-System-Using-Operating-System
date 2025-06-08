function updateLights(roadId, status, trafficCount, vehicleType) {
  const road = document.getElementById(roadId);
  const lights = road.querySelectorAll('.light');
  const vehicleContainer = road.querySelector('.vehicles');

  lights.forEach(light => light.classList.remove('active'));
  if (status === "RED") road.querySelector('.light.red').classList.add('active');
  else if (status === "YELLOW") road.querySelector('.light.yellow').classList.add('active');
  else if (status === "GREEN") road.querySelector('.light.green').classList.add('active');

  vehicleContainer.innerHTML = '';

  for (let i = 0; i < Math.min(trafficCount, 6); i++) {
    const v = document.createElement('div');
    const isEmergency = vehicleType === 'ambulance' || vehicleType === 'firefighter';
    v.className = 'vehicle';
    if (isEmergency && i === 0) {
      v.classList.add('emergency');
      v.textContent = '🚑';
    }
    if (status === "GREEN") v.classList.add('moving');
    vehicleContainer.appendChild(v);
  }
}

async function updateUI() {
  try {
    const response = await fetch('/data');
    const data = await response.json();

    for (const road in data) {
      const { status, traffic, vehicle } = data[road];
      const id = road.replace(" ", "");
      updateLights(id, status, traffic, vehicle);
    }
  } catch (err) {
    console.error("Error fetching data", err);
  }
}

function startSimulation() {
  fetch('/start')
    .then(res => res.json())
    .then(data => {
      console.log("Simulation started", data);
      document.getElementById('simulation-status').textContent = "Status: Running";
    });
}

function stopSimulation() {
  fetch('/stop')
    .then(res => res.json())
    .then(data => {
      console.log("Simulation stopped", data);
      document.getElementById('simulation-status').textContent = "Status: Stopped";
    });
}

setInterval(updateUI, 1000);
updateUI();
