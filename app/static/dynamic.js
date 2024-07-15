document.getElementById('weather-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    fetch('/weather', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        $('.weather-grid').removeClass('hidden');
        $('.city').text(data.city);
        $('.weather').text(data.description);
        $('.temp').text(`${data.temperature} °C`);
        $('.minTemp').text(`${data.temp_min} °C`);
        $('.maxTemp').text(`${data.temp_max} °C`);
        $('.icon').attr('src', `http://openweathermap.org/img/w/${data.icon}.png`);
        
        const forecastContainer = $('#forecast-cards');
        forecastContainer.empty(); // Clear previous cards
        
        if (data.forecast && data.forecast.length > 0) {
            data.forecast.forEach(forecast => {
                const card = $('<div>').addClass('card');
                card.html(`
                    <p class="date">${forecast.date}</p>
                    <p class="weather">${forecast.description}</p>
                    <p class="temp">${forecast.temperature} °C</p>
                    <img src="http://openweathermap.org/img/w/${forecast.icon}.png" alt="weather icon">
                `);
                forecastContainer.append(card);
            });
        } else {
            forecastContainer.append('<p>No forecast data available.</p>');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while fetching the weather data.');
    });
});
