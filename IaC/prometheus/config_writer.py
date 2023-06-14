import yaml


ip_list = ["ip1","ip2"]

PORT = 9100

def prometheus_conf_writer(ip_list, PORT):

    ip_list = list(map(lambda x : x+":"+str(PORT), ip_list))

    with open("./prometheus.yml","r") as f:
        yaml_data = yaml.safe_load(f)

    print(yaml_data)

    yaml_data["scrape_configs"][1]["static_configs"][0]={'targets': ip_list}

    with open("./prometheus.yml","w") as f:
        yaml.dump(yaml_data,f)

prometheus_conf_writer(ip_list, PORT)
