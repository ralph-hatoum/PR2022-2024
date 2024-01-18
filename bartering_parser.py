import json



def extract_bartering_config(config_path):
    with open(config_path,"r") as f:
        config = json.load(f)


    bartering_conf = config["Bartering_network"]

    failure_model = bartering_conf["FailureModel"]
    