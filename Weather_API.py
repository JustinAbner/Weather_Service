import requests


def user_city_and_state(cityname, statecode, countrycode, APIkey):  # Parameters set to receive arguments from main()
    try:
        city_get = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q='
                                f'{cityname},{statecode},{countrycode}&appid={APIkey}')
        # User provided information being passed into the URL to retrieve requested data

        connection_check = city_get.ok  # Checking for connection errors and informing user of outcome
        if connection_check is True:
            print('Connection successful')
            print('Processing. . .')
        elif connection_check is False:
            print('Connection was not successful')
        city_json = city_get.json()
    except ConnectionError as connection:  # Exceptions added to prevent crashing
        print(f'A Connection error has occurred: {connection}')
        print('Please try again')
    except TimeoutError as timeout:
        print(f'A Timeout error has occurred: {timeout}')
        print('Please try again')
    except requests.exceptions.ConnectionError:
        print(f'An internet issue has occurred, please try again once addressed')
    else:
        try:
            lat_get = city_json[0]['lat']  # Storing longitude and latitude from the retrieved data
            lon_get = city_json[0]['lon']
        except IndexError as index:  # Exceptions added to catch retrieval of lat and lon errors.
            print(f'An Index error has occurred: {index}')
            print('Please try again')
        except KeyError as key:
            print(f'A Key error has occurred: {key}')
            print('Please try again')
        else:
            coordinate_lookup(lat_get, lon_get, APIkey)


def user_zip_code(zip, country, APIkey):  # Parameters set to receive arguments from main()
    try:
        zip_get = requests.get(f'https://api.openweathermap.org/geo/1.0/zip?zip={zip},{country}&appid={APIkey}')
        connection_check = zip_get.ok  # Checking for connection errors and informing user of outcome
        if connection_check is True:
            print('Connection successful')
            print('Processing. . .')
        elif connection_check is False:
            print('Connection was not successful')
        zip_json = zip_get.json()
    except ConnectionError as connection:  # Exceptions added to prevent crashing
        print(f'A Connection error has occurred: {connection}')
        print('Please try again')
    except TimeoutError as timeout:
        print(f'A Timeout error has occurred: {timeout}')
        print('Please try again')
    except requests.exceptions.ConnectionError:  # If internet connectivity issues occur
        print(f'An internet issue has occurred, please try again once addressed')
    else:
        try:
            pull_lat = zip_json['lat']  # Storing longitude and latitude from the retrieved data
            pull_lon = zip_json['lon']
        except KeyError:  # Exception to catch invalid zipcodes
            print(f'A Key error has occurred, please try again')
        else:
            lat = str(pull_lat)  # Converting latitude on longitude from integers to strings
            lon = str(pull_lon)

            coordinate_lookup(lat, lon, APIkey)  # Passing the following variables as arguments to next function


def coordinate_lookup(lat, lon, APIkey):  # Parameters set to receive arguments from user_zip() & user_city_and_state()
    temp_units = input('Choose temperature units, (F) for Fahrenheit, (C) for Celsius, (K) for Kelvin: ')
    while True:  # Looping through temperature units until a valid option is chosen
        if temp_units.upper() == 'F':
            unit_type = '&units=imperial'  # String formatted as such to fit perfectly in the URL
            break
        elif temp_units.upper() == 'C':
            unit_type = '&units=metric'
            break
        elif temp_units.upper() == 'K':
            unit_type = ''
            break
        else:
            temp_units = input('Please enter a valid unit type, (F) for Fahrenheit, (C) for Celsius, (K) for Kelvin: ')

    weather_get = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat='
                               f'{lat}&lon={lon}&appid={APIkey}{unit_type}')
    # Passing the latitude, longitude, APIkey and unit type into the URL to retrieve the final weather information

    weather_json = weather_get.json()  # Putting data into an easier to access format
    print('-' * 80)  # Cosmetic divider

    cloud_cover_get = weather_json['clouds']['all']  # Accessing cloud coverage data
    cloud_cover = int  # Making the cloud_cover variable accessible outside of conditionals
    if cloud_cover_get == 0:
        cloud_cover = 'Clear Skies'
    elif 0 < cloud_cover_get <= 33:
        cloud_cover = 'Light Cloud Cover'
    elif 33 < cloud_cover_get <= 66:
        cloud_cover = 'Partial Cloud Cover'
    elif 66 < cloud_cover_get <= 99:
        cloud_cover = 'Heavily Cloud Cover'
    elif cloud_cover_get == 100:
        cloud_cover = 'Full Cloud Cover'

    # Retrieving weather data
    location_name = weather_json['name']
    current_temperature = weather_json['main']['temp']
    high_temperature = weather_json['main']['temp_max']
    low_temperature = weather_json['main']['temp_min']
    pressure = weather_json['main']['pressure']
    humidity = weather_json['main']['humidity']
    description = weather_json['weather'][0]['description']

    clean_print_weather(location_name, current_temperature, high_temperature, low_temperature, pressure, humidity,
                        cloud_cover, description)
    #  Passing all retrieved weather data to the final function to clean and print neatly


def clean_print_weather(location_name, current_temperature, high_temperature, low_temperature, pressure, humidity,
                        cloud_cover, description):

    # Creating personalized keys with retrieved values
    print(f'\nCurrent Weather Conditions For {location_name}')
    print(f'Current Temperature: {current_temperature}°')
    print(f'Temperature High: {high_temperature}°')
    print(f'Temperature Low: {low_temperature}°')
    print(f'Pressure: {pressure}hPa')
    print(f'Humidity: {humidity}%')
    print(f'Cloud Cover: {cloud_cover}')
    print(f'Weather Description: {description.title()}\n')
    print('-' * 63)  # Cosmetic divider

    while True:  # Asking user if they would like to do another look up, with a loop to ensure valid response
        user_lookup_again = input('Would you like to do another lookup? (y) for Yes, (N) for No: ')
        if user_lookup_again.upper() == 'Y':  # Returns user back to the start for a fresh lookup
            main()
        elif user_lookup_again.upper() == 'N':  # Ends weather lookup
            print('Thank you for using this program,\nGoodbye')
            quit()
        else:
            print('Response not valid, try again.')


def main():
    api_key = #REDACTED   # This is where you would enter your personal API Key
    country = 'US'

    print('\n-----Welcome to Justin\'s weather program-----')
    print('Would you like to search via your Zipcode or City/State?')
    while True:  # Loop created to collect user lookup method and ensure valid response
        user_input = input('Enter (1) for Zipcode or (2) for City/State or (Q) to quit: ')

        if user_input == '1':
            zipcode = input('Please enter your zip code: ')
            while True:
                if zipcode == '':  # Condition to stop empty response
                    zipcode = input('Response not valid, please enter a valid zipcode: ')
                else:
                    user_zip_code(zipcode, country, api_key)
                    break  # Break created for when user collects weather information, a fresh lookup can begin
        elif user_input == '2':
            city = input('Please enter your City/Town: ')
            while True:
                if city == '':
                    city = input('Response not valid, please enter a valid City: ')
                else:
                    break
            state = input('Please enter your State: ')
            while True:
                if state == '':
                    state = input('Response not valid, please enter a valid State: ')
                else:
                    break
            user_city_and_state(city, state, country, api_key)

        elif user_input.upper() == 'Q':  # Option to quit
            print('Farewell')
            quit()
        else:
            print('Response not valid, try again')


if __name__ == '__main__':
    main()
