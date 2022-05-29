# weatherstation

## Running the webapp
The webapp can be run with the command

    python weatherstation.py

## Using the webapp
You can use the webapp by pointing your browser to http://localhost:9875 after running the webapp.

## Geocoding
To enable geocoding, you can create a Google developer profile, make a project on the Google Developer Platform, and create an API key. After making an API key, you can use this API key in calls to Google web services. To use the Geocoding API, a Google API key is needed.

Once you have your Google API key, you can insert your key into the weather.ini file, which will be read when the weather.py module is loaded. The Google API key will be stored in the GOOGLE_API_KEY variable, which is used by the geocode method.

## Looking up coordinates for a city
When you're using the webapp, you can enter a city name in the city input field. After entering a city name, you can simply press the "Enter" key (keyCode=13) to look up the city's coordinates. If the search is successful, the city's coordinates will be filled out in the latitude and longitude fields.

In order to use this feature, a GOOGLE_API_KEY must be supplied in the weather.ini file.