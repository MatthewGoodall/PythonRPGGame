import json

def make_npc(file_path, all_npcs):
    with open(file_path) as data_file:
        data = json.load(data_file)
        for npc in data:
            print(data[npc]['Mother'], data[npc]['Bad Guy'])
            all_npcs.append(a_npc)

all_npcs = []
mother = make_npc("Resources/JSON Data/JSON_DATA.json", all_npcs)
