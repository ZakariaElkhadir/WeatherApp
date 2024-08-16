/**
 * Handles the form submission event and fetches weather data from the server.
 *
 * @param {Event} event - The form submission event.
 */
function suggestCities() {
  const input = document.getElementById("city").value.toLowerCase();
  const suggestionList = document.getElementById("suggestionList");
  
  // Clear previous suggestions
  suggestionList.innerHTML = '';

  if (input.length === 0) return;

  // Retrieve cities from the data attribute
  const cities = document.querySelector('.container-input').dataset.cities.split(',');

  // Filter cities based on input
  const filteredCities = cities.filter(city => city.toLowerCase().includes(input));
  
  // Create and append list items for suggestions
  filteredCities.forEach(city => {
      const listItem = document.createElement("li");
      listItem.textContent = city;
      listItem.addEventListener("click", () => {
          document.getElementById("city").value = city;
          suggestionList.innerHTML = '';
      });
      suggestionList.appendChild(listItem);
  });
}

document
  .getElementById('weather-form')
  .addEventListener('submit', function (event) {
    event.preventDefault()

    // Create a FormData object from the form submission
    const formData = new FormData(event.target)

    // Fetch weather data from the server
    fetch('/weather', {
      method: 'POST',
      body: formData
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error)
          return
        }
        // Display the weather data
        $('.weather-grid').removeClass('hidden')
        $('.city').text(data.city)
        $('.weather').text(data.description)
        $('.temp').text(`${data.temperature} °C`)
        $('.minTemp').text(`${data.temp_min} °C`)
        $('.maxTemp').text(`${data.temp_max} °C`)
        $('.icon').attr(
          'src',
          `https://openweathermap.org/img/w/${data.icon}.png`
        )

        const forecastContainer = $('#forecast-cards')
        forecastContainer.empty()

        // Array containing various types of stable weather conditions.
        const stableWeather = [
          'clear sky',
          'few clouds',
          'scattered clouds',
          'broken clouds',
          'overcast clouds'
        ]
        // Array containing various types of fluctuating weather conditions.
        const fluctuatingWeather = [
          'shower rain',
          'rain',
          'thunderstorm',
          'snow',
          'mist',
          'heavy intensity rain',
          'light rain',
          'moderate rain',
          'very heavy rain',
          'heavy intensity shower rain',
          'tornado',
          'squalls',
          'dust',
          'sand',
          'volcanic ash',
          'sand/dust whirls',
          'fog',
          'sand',
          'dust',
          'ash',
          'squalls',
          'tornado'
        ]

        // Display the forecast data
        if (data.forecast && data.forecast.length > 0) {
          data.forecast.forEach((forecast) => {
            const card = $('<div>').addClass('card-next')
            // Add a red glow to the card if the weather is fluctuating
            if (
              fluctuatingWeather.includes(forecast.description.toLowerCase())
            ) {
              card.addClass('red-glow')
            } else if (
              stableWeather.includes(forecast.description.toLowerCase())
            ) {
              card.addClass('green-glow')
            }
            // Add the forecast data to the card
            card.html(`
                    <p class="date">${forecast.date}</p>
                    <p class="weather">${forecast.description}</p>
                    <p class="temp">${forecast.temperature} °C</p>
                    <img src="https://openweathermap.org/img/w/${forecast.icon}.png" alt="weather icon">
                `)
            forecastContainer.append(card)
          })
        } else {
          forecastContainer.append('<p>No forecast data available.</p>')
        }
      })
      .catch((error) => {
        console.error('Error:', error)
        alert('An error occurred while fetching the weather data.')
      })
  })
