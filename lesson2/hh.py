from bs4 import BeautifulSoup as bs
import requests
import pickle
import pandas as pd
import time
import urllib

def m_page(p):
    mp = 0
    for i in p:
        if i.find().text.isdigit():
            if int(i.find().text) > mp:
                mp = int(i.find().text)
    return mp


def take_html(n, page):
    url = "https://irkutsk.hh.ru/search/vacancy"
    params = {
        "text": n,
        "page": page
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }
    rr = requests.get(url, headers=headers, params=params)
    # with open("hh.rsp", 'wb') as f:
    #     pickle.dump(r, f)
    # with open("hh.rsp", 'rb') as f:
    #     rr = pickle.load(f)
    return rr


if __name__ == "__main__":
    name_vacancy = input("Веедите даные для поиска ")
    len_name = len(name_vacancy)

    r = take_html(name_vacancy, 0)
    soup = bs(r.text, 'html.parser')
    pages = soup.findAll(attrs={"class": "bloko-button", "rel": "nofollow"})
    max_page = int(m_page(pages))
    # max_page = 40
    page = 1
    dicts = {"name": [], "oklad": [], "link": [], "site": []}
    while page < max_page:
        r = take_html(name_vacancy, str(page))
        all_vacancy = soup.findAll(True, attrs={"class": "vacancy-serp"})
        for i in all_vacancy:
            vacancys = soup.find_all(True, attrs={"class": ['vacancy-serp-item_premium', "vacancy-serp-item"]})
            for j in vacancys:
                dicts["name"].append(j.find(attrs={"class": "vacancy-serp-item__info"}).text)
                dicts["oklad"].append(j.find(attrs={"class": "vacancy-serp-item__sidebar"}).text)
                dicts["link"].append(str(j.find(attrs={"class": "vacancy-serp-item__info"}).a)[66:111 + len_name])
                dicts["site"].append("hh.ru")
        print(f"Сканирую {page + 1} страницу")
        page = page + 1
        time.sleep(1)

    df_vacancy = pd.DataFrame.from_dict(dicts, 'index').transpose()
    print(df_vacancy)
    df_vacancy.to_csv('vacancy.csv')
