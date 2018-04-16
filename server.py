# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:18:42 2018

@author: guglielmo
"""

from flask import Flask
from newspaper import Article
import googlesearch
import numpy as np

np.set_printoptions(threshold=np.NaN)
np.random.seed(34573623)

app = Flask(__name__)



@app.route('/<path:url_name>', methods=['GET', 'POST'])
def test_maso(url_name):
    article = build(url_name)
    title = article.title.replace('"',"'")
    image = article.top_image
    json = '{"url":"%s","title":"%s","image":"%s"}'%(url_name, title, image)
    return json

#@app.route('/droidcon/<url_name>')
def get_url(url_name):
    #incomplete
    d = {'it':'italian', 'en':'english'}
    article = build(url_name)
    start = url_name.find('www')
    end = url_name.find('/', start+1)
    language = article.meta_lang
    if len(language) == 0:
        language = 'en'
    query = article.title
    urls= get_results(query, d[language], n_top=5)
    all_urls = [url_name[start:end]]
    all_urls.extend(urls)
    
def build(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article

def get_results(query, lang='en', n_top=30):
    urls = googlesearch.search_news(query, num = 30)
    output = []
    c = 0
    for url in urls:
        article = Article(url)
        article.download()
        start = url.find('www')
        end = url.find('/', start+1)
        output.append(url[start:end])
        c += 1
        if c == n_top:
            break
    return output

