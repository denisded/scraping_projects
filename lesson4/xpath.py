from lxml.html import fromstring
import requests
from string import whitespace
from datetime import datetime

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


if __name__ == "__main__":
    news_mail_ru = get_news_mail_ru()
