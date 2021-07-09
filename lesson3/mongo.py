from pymongo import MongoClient
import pandas as pd
import json

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "hh"
MONGO_COLLECTION = "vacancy"


def write_vacancy_to_mongobd(col):
    df_vacancy = pd.read_csv("../lesson2/vacancy.csv")
    df_vacancy.drop_duplicates(subset=['link'], inplace=True)
    json_vacancy = json.loads(df_vacancy.T.to_json()).values()
    col.insert_many(json_vacancy)


def print_vacancy_oklad_big(oklad):
    cursor = vacancy.find({
        "oklad": {"$gt": oklad}
    })
    for i in cursor:
        print(i)


def write_new_vacancy_to_mongobd(col):
    df_vacancy = pd.read_csv("../lesson2/vacancy.csv")
    df_vacancy.drop_duplicates(subset=['link'], inplace=True)
    json_vacancy = json.loads(df_vacancy.T.to_json()).values()
    cursor = col.find({"site": df_vacancy['site'][0]})
    list_link_cursor = []
    for i in cursor:
        list_link_cursor.append(i['link'])
    # print(list_link_cursor)
    for j in json_vacancy:
        if j['link'] in list_link_cursor:
            continue
        col.insert_one(j)


if __name__ == "__main__":
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancy = db[MONGO_COLLECTION]
        # write_vacancy_to_mongobd(vacancy)
        # print_vacancy_oklad_big(100000)
        write_new_vacancy_to_mongobd(vacancy)
