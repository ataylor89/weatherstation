$(document).ready(function() {
    var today = moment().format("YYYY-MM-DD");
    $("#today").html("Today is " + moment().format("dddd MMMM Do YYYY"));
    $('input[name="city"]').on('keydown', function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            var city = $(this).val();
            if (city) {
                var url = '/geocode/' + city;
                $.get(url, function(data) {
                    if (data) {
                        var latitude = data['latitude'];
                        var longitude = data['longitude'];
                        var location = data['address'];
                        $('input[name="city"]').val(location);
                        $('input[name="latitude"]').val(latitude);
                        $('input[name="longitude"]').val(longitude);
                    }
                });
            }
        }
    });
    $("#weatherform").on('submit', function(e) {
        e.preventDefault();
        var latitude = $('input[name="latitude"]').val();
        var longitude = $('input[name="longitude"]').val();
        var url = "/weather_report/" + latitude + "," + longitude;
        $.get(url, function(data) {
            $('#weathertable tr:not(:first-child)').remove();
            console.dir(data);
            todays_report = data[today];
            for (time in todays_report) {
                var time_formatted = moment(time, "HH:mm:ss").format("h a");
                var tr = $("<tr>");
                var td0 = $("<td>").html(time_formatted);
                var td1 = $("<td>");
                if (todays_report[time]['temp']['fahrenheit'] && todays_report[time]['temp']['celsius'])
                    td1.html(todays_report[time]['temp']['fahrenheit'] + '&deg;F (' + todays_report[time]['temp']['celsius'] + '&deg;C)');
                var td2 = $("<td>").html(todays_report[time]['relative_humidity']['percent']);
                var td3 = $("<td>").html(todays_report[time]['chance_of_rain']['percent']);
                var td4 = $("<td>");
                if (todays_report[time]['dewpoint']['fahrenheit'] && todays_report[time]['dewpoint']['celsius'])
                    td4.html(todays_report[time]['dewpoint']['fahrenheit'] + '&deg;F (' + todays_report[time]['dewpoint']['celsius'] + '&deg;C)');                
                var td5 = $("<td>");
                if (todays_report[time]['wind_direction']['angle'])
                    td5.html(todays_report[time]['wind_direction']['angle'] + '&deg;');
                var td6 = $("<td>").html(todays_report[time]['wind_speed']['speed']);
                tr.append(td0);
                tr.append(td1);
                tr.append(td2);
                tr.append(td3);
                tr.append(td4);
                tr.append(td5);
                tr.append(td6);
                $('#weathertable').append(tr);
            }
            $('#weathertable').show();
        });
    });
});