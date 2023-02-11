import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import json
from unidecode import unidecode
import urllib3
import sys

url = sys.argv[1]
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}
urlHh = f"https://hh.ru/search/vacancy?text={url}&from=suggest_post&area="
urlHabr = f"https://career.habr.com/vacancies?q={url}&l=1&type=all"


def scrapingHabr(url):
    res = requests.get(url, headers=headers, verify=False)
    data = {}
    all = bs(res.text, 'html.parser')
    title = all.find_all('a', class_="vacancy-card__title-link")
    price = all.find_all("div", class_="basic-salary")
    company = all.find_all("div", class_="vacancy-card__company-title")
    img = all.find_all("img", class_="vacancy-card__icon")
    for item, pr, com, im in zip(title, price, company, img):
        i = item.text
        r = pr.text
        c = com.text
        data[i] = {"href": item['href'], "price": r,
                   "company": c, "img": im["src"]}
    with open("api-back/data/habr.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=False, indent=4,
                  ensure_ascii=False, separators=(',', ': '))
    print("Gut parse Habr")


def scrapingHh(url):
    res = requests.get(url, headers=headers)
    data = {}

    all = bs(res.text, 'html.parser')
    title = all.find_all('a', class_='serp-item__title')
    price = all.find_all('span', class_='bloko-header-section-3')
    company = all.find_all('a', class_="bloko-link bloko-link_kind-tertiary")
    img = all.find_all("img", class_="vacancy-serp-item-logo")
    for item, pr, com, im in zip(title, price, company, img):
        r = pr.text
        c = com.text
        i = item.text
        data[i] = {"href": item['href'], "price": r,
                   "company": c, "img": im["src"]}
    with open("api-back/data/hh.json", "w", encoding='utf-8') as f:
        json.dump(data, f, sort_keys=False, indent=4,
                  ensure_ascii=False, separators=(',', ': '))
    print("Gut parse HH")


scrapingHh(urlHh)
scrapingHabr(urlHabr)
