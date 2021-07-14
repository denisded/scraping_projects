from lxml.html import fromstring
import requests
from string import whitespace
from pymongo import MongoClient

CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")


def clear_string(s, whitespaces=CUSTOM_WHITESPACE):
    for space in whitespaces:
        s = s.replace(space, " ")
    return s


def get_dom(url):
    hed = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }
    return fromstring(requests.get(url, headers=hed).text)


def get_news_mail_ru():
    dom_mail_ru = get_dom("https://news.mail.ru/")
    items = dom_mail_ru.xpath('//div[contains(@class, "daynews__item")]')
    list_news = []
    for i in items:
        info = {
            'name': list(map(clear_string, i.xpath('.//span[contains(@class, "_title")]/text()'))),
            'link': i.xpath('.//a/@href')
        }
        dom_news = get_dom(i.xpath('.//a/@href')[0])
        items_news = dom_news.xpath('//span[contains(@class, "breadcrumbs__item")]')
        for j in items_news:
            try:
                info['date'] = j.xpath('.//span/@datetime')[0]
            except Exception as exp:
                print(f"Исключение {exp}")
            info['source'] = j.xpath('.//span[contains(@class, "link__text")]/text()')
        list_news.append(info)

    return list_news


def get_news_lenta_ru():
    dom_lenta_ru = get_dom('https://lenta.ru/')
    items = dom_lenta_ru.xpath(
        '//div[contains(@class, "b-yellow-box__wrap")]/div[not(contains(@class, "b-yellow-box__header"))]'
    )
    list_news = []
    for i in items:
        info = {
            'name': list(map(clear_string, i.xpath('.//a/text()'))),
        }
        link = 'https://lenta.ru' + str(i.xpath('.//a/@href')[0])
        source = 'lenta.ru'
        if i.xpath('.//a/@href')[0][:5] == "https":
            link = i.xpath('.//a/@href')[0]
            source = i.xpath('.//a/@href')[0][8:i.xpath('.//a/@href')[0].find(".ru")]
        info['link'] = link
        info['source'] = source
        info['date'] = get_dom(link).xpath('//div[contains(@class, "b-topic__info")]/time/@datetime')
        list_news.append(info)
    return list_news


def get_news_yandex_ru():
    dom_lenta_ru = get_dom('https://yandex.ru/')
    items = dom_lenta_ru.xpath('//ol/li/a')
    list_news = []
    for i in items:
        info = {
            'name': list(map(clear_string, i.xpath('./@aria-label'))),
            'link': i.xpath('./@href'),
            'source': get_dom(
                i.xpath('./@href')[0]
            ).xpath('//span[contains(@class, "news-story__subtitle-text")]//text()'),
            'date': get_dom(get_dom(
                    i.xpath('./@href')[0]
                ).xpath('//div[contains(@class, "news-story__head")]/a//@href')[0]
            ).xpath('//time[contains(@itemprop, "datePublished")]/@datetime')
        }
        list_news.append(info)
    return list_news


MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "news"
MONGO_COLLECTION = "news"

if __name__ == "__main__":
    news_mail_ru = get_news_mail_ru()
    news_lenta_ru = get_news_lenta_ru()
    news_yandex_ru = get_news_yandex_ru()
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        news = db[MONGO_COLLECTION]
        news.insert_many(news_mail_ru)
        news.insert_many(news_lenta_ru)
        news.insert_many(news_yandex_ru)