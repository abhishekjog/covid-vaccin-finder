import pandas as pd
import json
import requests
import datetime

look_for = {
    #"PIN" : [411057, 411001, 411002, 411003, 411004, 411026],
    "PIN" : range(411001, 412000),
    "DATE" : datetime.datetime.today().strftime("%d-%m-%Y"),
    #"DATE" : '04-05-2021',
    "STATE" : "Maharashtra",
    "DISTRICT" : "Pune",
    "AGE" : 18
}

GET_STATES = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
GET_DISTRICTS = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"
GET_SLOTS = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=districtid&date={look_for['DATE']}"
response = requests.get(GET_STATES)
if response.ok:
    df = pd.DataFrame(json.loads(response.text)["states"])
    state_id = (df.query(f"state_name == '{look_for['STATE']}'")["state_id"].iloc[0])
    GET_DISTRICTS += str(state_id)
    response = requests.get(GET_DISTRICTS)
    if response.ok:
        df = pd.DataFrame(json.loads(response.text)["districts"])
        district_id = (df.query(f"district_name == '{look_for['DISTRICT']}'")["district_id"].iloc[0])
        response = requests.get(GET_SLOTS.replace("districtid", str(district_id)))
        if response.ok:
            df = pd.DataFrame(json.loads(response.text)["centers"])
            df = df.explode("sessions")
            df['min_age_limit'] = df.sessions.apply(lambda x: x['min_age_limit'])
            df['available_capacity'] = df.sessions.apply(lambda x: x['available_capacity'])
            df['date'] = df.sessions.apply(lambda x: x['date'])
            df = df[["date", "available_capacity", "min_age_limit", "pincode", "name", "state_name", "district_name", "block_name", "fee_type"]]
            if 'PIN' in look_for.keys() and len(look_for['PIN']):
                print(df[(df['min_age_limit'] == look_for['AGE']) & (df['pincode'].isin(look_for['PIN']))].sort_values('date'))
            else:
                print(df[df['min_age_limit'] == look_for['AGE']].sort_values('date'))
        else:
            print("Could not fetch slot level")
    else:
        print("Could not fetch district level")
else:
    print("Could not fetch state level")