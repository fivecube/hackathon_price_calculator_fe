import requests
import json

def get_category_and_subcategory_options_api_response():
    url = "http://localhost:8000/api/accounts/categories/all/"
    response = requests.request("GET", url)
    return response.json()

def get_countries_api_response():
    url = "http://localhost:8000/api/geo/countries"
    response = requests.request("GET", url)
    return response.json()

def send_to_niranjan(item_to_be_sent, edited):
    if edited:
        url = "http://localhost:8000/api/billing/pricing/recalculate"
        print('payload', item_to_be_sent)
        payload = json.dumps(item_to_be_sent)
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'csrftoken=Cw4puBKh2cSFOsLYXYO5sbmJqILtmd586dk9iYflbfbftrjy3hDZPBvvPkQJiz6x'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()