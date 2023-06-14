import requests
import json

## AUTH, TOKEN, GRAFANA URL

token = "glsa_Z5GAEI4tP0tOyzOszutrsJroK6MuqWFq_e1927268"

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

url = "http://localhost:3000/api/dashboards/db"

## LOAD BASE DASHBOARD MODEL
with open("dashboard.json","r") as f:
    dashboard = json.load(f)

data = {
    'dashboard': dashboard,
    'overwrite': True  # Set to True to overwrite any existing dashboard with the same UID
}

response = requests.post(url=url, json=data,headers=headers)

print(response)