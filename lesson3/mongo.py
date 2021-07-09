from pymongo import MongoClient
import pandas as pd
import json

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "hh"
MONGO_COLLECTION = "vacancy"


def write_vacancy_to_mongobd(col):
    df_vacancy = pd.read_csv("../lesson2/vacancy.csv")
    json_vacancy = json.loads(df_vacancy.T.to_json()).values()
    col.insert(json_vacancy)


if __name__ == "__main__":
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancy = db[MONGO_COLLECTION]
        write_vacancy_to_mongobd(vacancy)
