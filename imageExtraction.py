import pandas as pd
from pymongo import MongoClient
import gridfs
from pprint import pprint
import requests
from PIL import Image

db = MongoClient().Craiglist
fs = gridfs.GridFS(db)

fsFilesColl = db["Cars"]
cursor = fsFilesColl.find({})
count = 0

for doc in cursor:
    imageUrl = doc["image_url"]
    #print(imageUrl)

    response = requests.get(imageUrl)
    if response.status_code == 200:
        data = response.content

        if fs.put(data, filename=doc["id"]):
            count += 1
            if count % 10 == 0:
                print(str(count), "images loaded successfully")

print("Total", count, "images loaded successfully")