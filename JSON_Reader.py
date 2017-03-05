import json


def JSON_Reader(json_data):
    with open(json_data) as json_file:
        json_read = json.load(json_file)
        print(json_read['b']['Hello'])
