# standard imports
from datetime import datetime
import time
import numbers

# pip install pyautogui
import pyautogui
# pip install requests
import requests
# pip install tabulate
import tabulate
# pip install py-linq
from py_linq import Enumerable

schaeffer_hall_electric_power_web_id = "F1AbEAVYciAZHVU6DzQbJjxTxWw_E_fKY9J6RGuHFS_ZKR9xgqgO-CVKTR1YoEwPKZJbPnwSVRTTlQyMjU5XFVJLUVORVJHWVxNQUlOIENBTVBVU1xTQ0hBRUZGRVIgSEFMTHxFTCBQT1dFUg"
schaeffer_hall_steam_power_web_id = "F1AbEAVYciAZHVU6DzQbJjxTxWw_E_fKY9J6RGuHFS_ZKR9xgsGEGEIKioF8UMkXwaeK6eQSVRTTlQyMjU5XFVJLUVORVJHWVxNQUlOIENBTVBVU1xTQ0hBRUZGRVIgSEFMTHxTVCBQT1dFUg"
schaeffer_hall_chilled_water_power_web_id = "F1AbEAVYciAZHVU6DzQbJjxTxWw_E_fKY9J6RGuHFS_ZKR9xg0C85gn786lU03BVwI5i3SQSVRTTlQyMjU5XFVJLUVORVJHWVxNQUlOIENBTVBVU1xTQ0hBRUZGRVIgSEFMTHxDVyBQT1dFUg"

def to_local_time(timestamp_string):
    utc_datetime =  datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%SZ")
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def get_hourly_data_from_pi(web_id, user_name, password):
    url = "https://pi-vision.facilities.uiowa.edu/piwebapi/streams/" + web_id + "/summary?startTime=1/1/2017 00:00:00&endTime=10/24/2023 16:00:00&summaryDuration=1h&summaryType=average&timeZone=Central Standard Time"
    response = requests.get(url, auth=(user_name,password))
    body = response.json()
    tuples = []
    for item in body["Items"]:
        time = to_local_time(item["Value"]["Timestamp"])
        value = item["Value"]["Value"]
        if not isinstance(value, numbers.Number):
            value = -1
        tuple = (time, value)
        tuples.append(tuple)
    return tuples

def main():
    user_name = input("Enter HawkId Username: ")
    password = pyautogui.password(text='Enter HawkId password', title='Password Entry Window', default='', mask='*')

    steam_data = get_hourly_data_from_pi(schaeffer_hall_steam_power_web_id, user_name, password)
    print("Amount of bad data points: " + str(Enumerable(steam_data).where(lambda x: x[1] == -1).count()))
    steam_data = Enumerable(steam_data).order_by_descending(lambda x: x[1]).take(20).to_list()
    print(tabulate.tabulate(steam_data, headers=["Timestamp", "Value"]))

    chilled_water_data = get_hourly_data_from_pi(schaeffer_hall_chilled_water_power_web_id, user_name, password)
    print("Amount of bad data points: " + str(Enumerable(chilled_water_data).where(lambda x: x[1] == -1).count()))
    chilled_water_data = Enumerable(chilled_water_data).order_by_descending(lambda x: x[1]).take(20).to_list()
    print(tabulate.tabulate(chilled_water_data, headers=["Timestamp", "Value"]))

    electric_data = get_hourly_data_from_pi(schaeffer_hall_electric_power_web_id, user_name, password)
    electric_data = Enumerable(electric_data).select(lambda x: (x[0], x[1]*3600))
    print("Amount of bad data points: " + str(Enumerable(electric_data).where(lambda x: x[1] == -1).count()))
    electric_data = Enumerable(electric_data).order_by_descending(lambda x: x[1]).take(20).to_list()
    print(tabulate.tabulate(electric_data, headers=["Timestamp", "Value"]))

if __name__ == '__main__':
    main()
