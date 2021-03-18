import sys
sys.path.insert(0, '..')

import requests
from lxml import html
from pprint import pprint
from datetime import datetime
from parse_to_mongo.mongo_global_variables import MONGO_URI
from pymongo import MongoClient
import pymongo
from pymongo.errors import BulkWriteError
import json
import pandas as pd

COLLECTION_NAME = "news_data"
MONGO_DB = 'posts'

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}

def save_to_mongo(data,
                  uri = MONGO_URI,
                  db = MONGO_DB, 
                  colletion = COLLECTION_NAME):
    with MongoClient(uri) as client:
        db = client[db]
        coll = db[colletion]
        records = json.loads(data.T.to_json()).values()
        try:
            coll.insert_many(records, ordered = False)
        
        except BulkWriteError as bwe:
            print("Batch Inserted with some errors. May be some duplicates "
                  "were found and are skipped.")
            print(f"Count is {coll.count()}.")

        except Exception as e:
            print( { 'error': str(e) })

def check_list(data, iso_dt = False):
    if isinstance(data, list):
            try:
                data = data[0]
                if iso_dt:
                    data = datetime.fromisoformat(data).date()
            except:
                pass
    return data
    
def parse_mailru_news(url = "https://news.mail.ru", 
                      headers = headers,
                      to_mongo = True,
                      ):
    
    xpath_string = './/*[contains(@class, "captions")]'
    r = requests.get(url, headers)
    elems = html.fromstring(r.text).xpath(xpath_string)
    
    data = []
    for elem in elems:
        info = {}
        title = elem.xpath(
            ".//*[contains(@class, 'title') or"
            " contains(@class, 'subtitle')]//text()")
        info['title'] = check_list(title)
        href = elem.xpath(".//ancestor::*/@href")
       
        href = check_list(href)
            
        if 'http' not in str(href):
            href = f'{url}{href}'
        
        info['link'] = href
        url_sub = href
        
        r_sub = requests.get(url_sub, headers)
        s_sub = r_sub.text
        doc_sub = html.fromstring(s_sub)
        date = doc_sub.xpath(".//span[contains(@class, 'js-ago')]//@datetime")
     
        date = check_list(date, iso_dt = True)
        info['date'] = date
        
        src = doc_sub.xpath(".//span[contains(@class, "
                                    "'breadcrumbs__item')]//a/@href")
        src = check_list(src)
        info['src'] = src
        
        data.append(info)
    
    data = pd.DataFrame(data)    
    
    if to_mongo:
        save_to_mongo(data)
           
    return data

def edit_lenta_link(list_of_links, url):
    list_of_links_tmp = []
    for link in list_of_links:
        if 'http' not in str(link):
            list_of_links_tmp.append(f'{url}{link}')
        else:
            list_of_links_tmp.append(link)
    return list_of_links_tmp
    

def parse_lentaru_news(url = "https://lenta.ru", 
                      headers = headers,
                      to_mongo = True,
                      ):
    
    # main news
    xpath_string_main = './/*[contains(text(), "Главные новости")]'
    r_main = requests.get(url, headers)
    
    elem_main = html.fromstring(r_main.text).xpath(xpath_string_main)[0]
    
    title_main = elem_main.xpath(".//parent::div//*[not(contains(@class, 'header'))]//text()")
    link_main = elem_main.xpath(".//parent::div//*[not(contains(@class, 'header'))]//@href")
    link_main = edit_lenta_link(link_main, url)[1:]
    
    date_main = []
    for url_sub in link_main:       
        r_sub = requests.get(url_sub, headers)
        s_sub = r_sub.text
        doc_sub = html.fromstring(s_sub)
        date_sub = doc_sub.xpath(".//time[contains(@class, 'date')]/text()")
        date_sub = check_list(date_sub, iso_dt = False)
        date_main.append(date_sub)
        
    # top 7 news
    xpath_string_top = './/*[contains(@class, "top7")]'
    r_top = requests.get(url, headers)
    elem_top = html.fromstring(r_top.text).xpath(xpath_string_top)[0]
    date_top = elem_top.xpath(".//*[contains(@class, datetime)]/@datetime")    
    title_top = elem_top.xpath(".//a[contains(@class, datetime) and "
                          "not(contains(@class, 'button')) and "
                          "not(contains(@class, 'favorite'))]/text()")
    link_top = elem_top.xpath(".//a[contains(@class, datetime) and "
                          "not(contains(@class, 'button')) and "
                          "not(contains(@class, 'favorite'))]/@href")
    link_top = edit_lenta_link(link_top, url)
    
    
    data = {}
    data['title'] = title_top+title_main
    data['link'] = link_top+link_main
    data['date'] = date_top+date_main
    data = pd.DataFrame.from_dict(data, orient='index').T
    data['src'] = url
    
    if to_mongo:
        save_to_mongo(data)
    
    return data

def parse_yandex_news(url = 'https://yandex.ru/news', 
                      headers = headers,
                      to_mongo = True,
                      ):

    xpath_string = './/*[contains(@class, "navigation")]'
    r = requests.get(url, headers)
    elem = html.fromstring(r.text).xpath(xpath_string)
    data = []
    el = elem[0].xpath(".//following::article")
    for e in el:
        info = {}
        info['title'] = check_list(e.xpath('.//*[contains(@class,'
                                           ' "annotation")]/text()'))
        info['link'] = e.xpath('.//*[contains(@class, "link")]/@href')[0]
        info['src'] = e.xpath('.//*[contains(@class, "source")]/text()')[0]
        info['date'] = str(datetime.today())+', '+\
            str(e.xpath('.//*[contains(@class, "source")]/text()')[1])
        data.append(info)
            
    data = pd.DataFrame(data)
    if to_mongo:
        save_to_mongo(data)
    
    return data

    
    
