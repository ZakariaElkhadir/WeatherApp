$(document).ready(function(){
    $('#weather-form').on('submit', function(event){
        const cel = '°C';
        event.preventDefault();
        var city = $('#city').val();
        $.ajax({
            url: '/weather',
            type: 'POST',
            data: {city: city},
            success: function(response){
               if (response == 'error') {
                alert('Please enter a valid city name');
            } else {
                $('.city').text(response.city);
                $('.weather').text(response.description);
                $('.temp').text(response.temperature + cel);
                $('.minTemp').text(response.temp_min + cel);
                $('.maxTemp').text(response.temp_max + cel);
               }
            }
        })
        
        $('.hidden').css('display', 'block');
        $('.welcome').css('display', 'none');
    });
});