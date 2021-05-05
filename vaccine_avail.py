import pandas as pd
import json
import requests
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--age", help="Age group : 18 or 45", type=int, choices=[18, 45], default=18)
parser.add_argument("--pincodes", help="Comma separate list of pincodes, \"all\" for all pincodes in the district", default="all")
parser.add_argument("--pinrange", help="hyphen separate range of pincodes")
parser.add_argument("--state", help="State name (first letter caps)", default="Maharashtra")
parser.add_argument("--district", help="District name (first letter caps)", default="Pune")
parser.add_argument("--vaccine", help="Name of the vaccine", choices=["Covaxin", "Covishield"])
parser.add_argument("--date", help="Select from date in dd-mm-yyyy format", default=datetime.datetime.today().strftime("%d-%m-%Y"))
args = parser.parse_args()

look_for = {
    "PIN" : [int(x) for x in args.pincodes.split(',')] if args.pincodes and args.pincodes != "all" \
        else [] if args.pincodes == "all" \
            else range(args.pinrange('-')[0], args.pinrange('-')[1]) if args.pinrange \
                else range(411001, 412000),
    "DATE" : args.date,
    "STATE" : args.state,
    "DISTRICT" : args.district,
    "AGE" : args.age
}

GET_STATES = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
GET_DISTRICTS = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"
GET_SLOTS = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=districtid&date=date_val"

response = requests.get(GET_STATES)
if response.ok:
    df = pd.DataFrame(json.loads(response.text)["states"])
    state_id = (df.query(f"state_name == '{look_for['STATE']}'")["state_id"].iloc[0])
    GET_DISTRICTS += str(state_id)
    response = requests.get(GET_DISTRICTS)

    if response.ok:
        df = pd.DataFrame(json.loads(response.text)["districts"])
        district_df = df.query(f"district_name == '{look_for['DISTRICT']}'")["district_id"]
        if ( district_df.empty ):
            print("District should be one of below")
            print(df.district_name.to_string(index=False)) 
            exit(1) 
        district_id = district_df.iloc[0]
        local_get_slots = GET_SLOTS.replace("districtid", str(district_id))
        local_get_slots = local_get_slots.replace("date_val",str(look_for['DATE']))
        response = requests.get(local_get_slots)
               
        if response.ok:
            slots = pd.DataFrame(json.loads(response.text)["centers"])
            slots = slots.explode("sessions")
            slots['min_age_limit'] = slots.sessions.apply(lambda x: x['min_age_limit'])
            slots['available_capacity'] = slots.sessions.apply(lambda x: x['available_capacity'])
            slots['date'] = slots.sessions.apply(lambda x: x['date'])
            slots = slots[["date", "available_capacity", "min_age_limit", "pincode", "name", "state_name", "district_name", "block_name", "fee_type"]]
            if 'PIN' in look_for.keys() and len(look_for['PIN']):
                print(slots[(slots['min_age_limit'] == look_for['AGE']) & (slots['pincode'].isin(look_for['PIN']))].sort_values('date'))
            else:
                print(slots[slots['min_age_limit'] == look_for['AGE']].sort_values('date'))
                
                available_capacity = slots[(slots['min_age_limit'] == look_for['AGE']) & (slots['available_capacity'] != 0)].sort_values('date')    
                if(available_capacity.empty):
                    print("")
                    print("No slots available")
                else:
                    print("Below are available slots")
                    print(available_capacity)
        else:
            print("Could not fetch slot level")
    else:
        print("Could not fetch district level")
else:
    print("Could not fetch state level")
