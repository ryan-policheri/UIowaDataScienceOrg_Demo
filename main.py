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
    url = "https://itsnt2259.iowa.uiowa.edu/piwebapi/streams/" + web_id + "/summary?startTime=1/1/2017 00:00:00&endTime=10/24/2023 16:00:00&summaryDuration=1h&summaryType=average&timeZone=Central Standard Time"
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

if __name__ == '__main__':
    main()
