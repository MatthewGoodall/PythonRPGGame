import json

global var
var = list()
text = list()


def Read_JSON(json_data, data_entry, name):
    with open(json_data) as json_file:
        json_read = json.load(json_file)
        print(json_read["NPC"][data_entry][name])
        global rand
        rand = json_read["NPC"][data_entry][name]
        var.append(rand)
        print(var[0])