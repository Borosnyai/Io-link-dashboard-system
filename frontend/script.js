const testData = [
    {
        name: 'Vibration Sensor 1',
        velocity: 2.5,
        frequency: 60,
        temperature: 45,
        status: 'OK'
    }
];

function displaySensors(sensors) {
    const container = document.getElementById('sensorCards');
    container.innerHTML = '';
    
    sensors.forEach(sensor => {
        container.innerHTML += `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${sensor.name}</h5>
                        <p class="card-text">Velocity: ${sensor.velocity} mm/s</p>
                        <p class="card-text">Frequency: ${sensor.frequency} Hz</p>
                        <p class="card-text">Temperature: ${sensor.temperature} °C</p>
                        <p class="card-text">Status: <span class="badge bg-success">${sensor.status}</span></p>
                    </div>
                </div>
            </div>
        `;
    });
}

displaySensors(testData);