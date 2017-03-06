import json


def JSON_Reader(json_data, data_entry, name):
    with open(json_data) as json_file:
        json_read = json.load(json_file)
        print(json_read["NPC"][data_entry][name])
