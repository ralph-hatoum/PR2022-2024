import requests
import json

NODES = ["134.214.202.27","134.214.202.28","8.8.8.8","4.4.4.4"]


def country_discriminator(NODES,country_code):
    API_ENDPOINT = "https://api.iplocation.net/?ip="

    nodes_to_keep = []

    for node in NODES:
        response = requests.get(API_ENDPOINT+node)
        if response.status_code == 200:
            data = json.loads(response.text)
            if data["country_code2"]==country_code:
                nodes_to_keep.append(node)
        else:
            print("Error - could not determine IP location")


    return nodes_to_keep


print(country_discriminator(NODES, "FR"))