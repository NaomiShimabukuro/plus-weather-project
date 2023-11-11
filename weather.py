import csv
from datetime import datetime

DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"


def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and Celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees celcius."
    """
    return f"{temp}{DEGREE_SYBMOL}"


def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.

    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    # Convert ISO date string to a datetime object

    iso_date = datetime.fromisoformat(iso_string)
    
    formatted_date = iso_date.strftime("%A %d %B %Y")
    return formatted_date
    pass


def convert_f_to_c(temp_in_fahrenheit):
    """Converts an temperature from farenheit to celcius.

    Args:
        temp_in_farenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees celcius, rounded to 1dp.
    """
    if isinstance(temp_in_fahrenheit, str):
        temp_in_fahrenheit = float(temp_in_fahrenheit)
    if not isinstance(temp_in_fahrenheit, (float, int)):
        raise ValueError("Input must be a float, int, or a string representing a number.")

    temp_in_celsius = (temp_in_fahrenheit - 32) * 5/9
    return round(temp_in_celsius, 1)


def calculate_mean(weather_data):
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """
    if not weather_data:
        return 0.0

    # Convert string values to numbers (int or float)
    numeric_data = [float(value) if isinstance(value, str) else value for value in weather_data]

    return sum(numeric_data) / len(numeric_data)


def load_data_from_csv(csv_file):
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """
    data = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append([row["date"], float(row["min"]), float(row["max"])])
    return data
    pass


def find_min(weather_data):
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minium value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:
        return ()

    min_value = None
    min_index = None

    for i, value in enumerate(weather_data):
        if isinstance(value, str):
            value = float(value)

        if min_value is None or value <= min_value:
            min_value = value
            min_index = i

    return min_value, min_index
    pass


def find_max(weather_data):
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:
        return ()

    max_value = None
    max_index = None

    for i, value in enumerate(weather_data):
        if isinstance(value, str):
            value = float(value)

        if max_value is None or value >= max_value:
            max_value = value
            max_index = i

    return max_value, max_index
 
    pass


def generate_summary(weather_data):
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    summary = ""
    min_list = []
    max_list = []

    for min_temp in weather_data:
        min_list.append(min_temp[1])

    for max_temp in weather_data:
        max_list.append(max_temp[2])

    num_of_days = len(weather_data)
    for day in weather_data:
 
        high_temp = find_max(max_list)
        high_temp_day = high_temp[1]
        high_temp_day = weather_data[high_temp_day]
        high_date = convert_date(high_temp_day[0])
        low_temp = find_min(min_list)
        low_temp_day = low_temp[1]
        low_temp_day = weather_data[low_temp_day]
        low_date = convert_date(low_temp_day[0])
        f_high_temp = convert_f_to_c(high_temp[0])
        f_low_temp = convert_f_to_c(low_temp[0])
        average_low = calculate_mean(min_list)
        f_average_low = convert_f_to_c(average_low)
        average_high = calculate_mean(max_list)
        f_average_high = convert_f_to_c(average_high)
        
    summary += (
        f"{num_of_days} Day Overview\n"
            f"  The lowest temperature will be {f_low_temp}°C, and will occur on {low_date}.\n" 
            f"  The highest temperature will be {f_high_temp}°C, and will occur on {high_date}.\n"  
            f"  The average low this week is {f_average_low}°C.\n"  
            f"  The average high this week is {f_average_high}°C.\n"
        )
    
    return summary


def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    if not weather_data:
        return ""
    lines=""
    
    for day in weather_data:
        date = convert_date(day[0])
        min_celcius=convert_f_to_c(day[1])
        max_celcius=convert_f_to_c(day[2])
        lines += (
                f"---- {date} ----\n"
                f"  Minimum Temperature: {format_temperature(min_celcius)}\n"
                f"  Maximum Temperature: {format_temperature(max_celcius)}\n\n"
                )
        
    return lines


