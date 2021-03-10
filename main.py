import requests
import os
from datetime import datetime

NUT_APP_ID = os.environ.get('NUT_ID')
NUT_APP_KEY = os.environ.get('NUT_KEY')
EXERCISE_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'

GENDER = os.environ.get('VAR_GENDER')
WEIGHT = os.environ.get('VAR_WEIGHT')
HEIGHT = os.environ.get('VAR_HEIGHT')
AGE = os.environ.get('VAR_AGE')
PROJECT_NAME = 'exerciseTracker'
SHEET = 'sheet1'
USERNAME = os.environ.get('GOOG_USER')
AUTH_HEADER = {'Authorization': os.environ.get('AUTH_KEY')}

SHEETY_ENDPOINT = f'https://api.sheety.co/{USERNAME}/{PROJECT_NAME}/{SHEET}'

now = datetime.now()
today = now.strftime("%m/%d/%Y")
time = str(now)
time_of_day = time[11:19]

query = input('WHAT YOU DO: ')

request_body = {
    'query':query,
    'gender':GENDER,
    'weight_kg':WEIGHT,
    'height_cm':HEIGHT,
    'age':AGE,
}

headers = {
    'x-app-id':NUT_APP_ID,
    'x-app-key':NUT_APP_KEY,
}

request = requests.post(url=EXERCISE_ENDPOINT, json=request_body, headers=headers)
new_data = request.json()


cals_burned = new_data['exercises'][0]['nf_calories']
time_spent = new_data['exercises'][0]['duration_min']
exercise_type = new_data['exercises'][0]['name']

sheety_body = {
    'sheet1': {
        'date':today,
        'time':time_of_day,
        'exercise':exercise_type,
        'duration':time_spent,
        'calories':cals_burned,
}
}

update_sheet = requests.post(url=SHEETY_ENDPOINT, json=sheety_body, headers=AUTH_HEADER)
