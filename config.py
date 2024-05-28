import json
import os

json_file_path = "config.json"

if not os.path.exists(json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump({"TOKEN": ""}, json_file)

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)
    TOKEN = data.get("TOKEN")

if TOKEN is None or TOKEN == "":
    TOKEN = input("Please enter your token: ")
    with open(json_file_path, 'w') as json_file:
        json.dump({"TOKEN": TOKEN}, json_file)