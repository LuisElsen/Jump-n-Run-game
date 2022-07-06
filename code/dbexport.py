import json

import pymongo
from pymongo import MongoClient
cluster = MongoClient(
    "mongodb+srv://Luis_Elsen_Messmer:GFgrpM3c0x7GW7qu@cluster0.ocuhchc.mongodb.net/?retryWrites=true&w=majority")

db = cluster["jump_n_run_maps"]

collection = db["luis"]
with open("Maps\\big one.json", "r") as f:
    data = json.load(f)
    data["name"] = "Maps\\big one.json"
collection.insert_one(data)
