import pandas as pd
import json
import requests
import datetime
import argparse
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui

PHONE = ""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--age", help="Age group : 18 or 45", type=int, choices=[18, 45], default=18)
    parser.add_argument("--pincodes", help="Comma separate list of pincodes, \"all\" for all pincodes in the district")
    parser.add_argument("--pinrange", help="hyphen separate range of pincodes")
    parser.add_argument("--state", help="State name (first letter caps)", default="Maharashtra")
    parser.add_argument("--district", help="District name (first letter caps)", default="Pune")
    parser.add_argument("--vaccine", help="Name of the vaccine", choices=["Covaxin", "Covishield"])
    parser.add_argument("--date", help="Select from date in dd-mm-yyyy format", default=datetime.datetime.today().strftime("%d-%m-%Y"))
    parser.add_argument("--vacant-only", help="Show only vacant slots", type=bool, default=False)
    parser.add_argument("--phone", help="Phone to login CoWin")
    parser.add_argument("--dose", help="Dose number 1 or 2", type=int, choices=[1, 2], default=1)
    args = parser.parse_args()
    return args

def check_slots(args:argparse.Namespace):
    look_for = {
        "PIN" : [int(x) for x in args.pincodes.split(',')] if args.pincodes and args.pincodes != "all" \
            else [] if args.pincodes == "all" \
                else range(args.pinrange('-')[0], args.pinrange('-')[1]) if args.pinrange \
                    else range(411001, 412000),
        "DATE" : args.date,
        "STATE" : args.state,
        "DISTRICT" : args.district,
        "AGE" : args.age,
        "DOSE" : f"{args.dose}",
        "VACANT_ONLY" : args.vacant_only
    }
    global PHONE
    PHONE = args.phone

    print(datetime.datetime.today().strftime("%d-%m-%Y %HH:%MM:%SS") + " " + str(look_for))

    headers = {'Cache-Control': 'no-cache','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
    GET_STATES = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    GET_DISTRICTS = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"
    GET_SLOTS = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=districtid&date={look_for['DATE']}"

    try:
        response = requests.get(GET_STATES, headers=headers)
        if response.ok:
            df = pd.DataFrame(json.loads(response.text)["states"])
            state_id = (df.query(f"state_name == '{look_for['STATE']}'")["state_id"].iloc[0])
            GET_DISTRICTS += str(state_id)
            response = requests.get(GET_DISTRICTS, headers=headers)

            if response.ok:
                df = pd.DataFrame(json.loads(response.text)["districts"])
                district_id = (df.query(f"district_name == '{look_for['DISTRICT']}'")["district_id"].iloc[0])
                response = requests.get(GET_SLOTS.replace("districtid", str(district_id)), headers=headers)

                if response.ok:
                    slots = pd.DataFrame(json.loads(response.text)["centers"])
                    slots = slots.explode("sessions")
                    slots['min_age_limit'] = slots.sessions.apply(lambda x: x['min_age_limit'])
                    slots['available_capacity'] = slots.sessions.apply(lambda x: x[f"available_capacity_dose{look_for['DOSE']}"])
                    slots['vaccine'] = slots.sessions.apply(lambda x: x['vaccine'])
                    slots['date'] = slots.sessions.apply(lambda x: x['date'])
                    slots = slots[["date", "vaccine", "available_capacity", "min_age_limit", "pincode", "name", "state_name", "district_name", "block_name", "fee_type"]]
                    available_capacity = []
                    if 'PIN' in look_for.keys() and len(look_for['PIN']):
                        print(slots[(slots['min_age_limit'] == look_for['AGE']) & (slots['pincode'].isin(look_for['PIN']))].sort_values('date'))
                        available_capacity = slots[(slots['min_age_limit'] == look_for['AGE']) & (slots['pincode'].isin(look_for['PIN'])) & (slots['available_capacity'] != 0)].sort_values('date')
                    else:
                        print(slots[slots['min_age_limit'] == look_for['AGE']].sort_values('date'))
                        
                        available_capacity = slots[(slots['min_age_limit'] == look_for['AGE']) & (slots['available_capacity'] != 0)].sort_values('date')    
                    if(available_capacity.empty):
                        print("")
                        print("No slots available")
                    else:
                        print("Below are available slots")
                        print(available_capacity)
                    return available_capacity, None
                else:
                    return None, "Could not fetch slot level"

            else:
                return None, "Could not fetch district level"

        else:
            return None, "Could not fetch state level"
    except Exception as e:
        print(e)

def open_website():
    driver = webdriver.Chrome("C:\\Users\\AbhishekJog\\Downloads\\chromedriver_win32\\chromedriver.exe")
    driver.get("https://selfregistration.cowin.gov.in/")
    
    pyautogui.press('tab')
    time.sleep(0.25)
    pyautogui.press('tab')
    time.sleep(0.25)
    pyautogui.press('tab')
    time.sleep(0.25)
    pyautogui.press('tab')
    time.sleep(0.25)
    pyautogui.typewrite(f"{PHONE}")
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(600)
    
if __name__ == "__main__":
    args = parse_args()
    while True:
        try:
            df, err = check_slots(args)
            if not err:
                print(df)
                if len(df):
                    open_website()
                
            time.sleep(5)
        except Exception as e:
            print (e)
            
            
