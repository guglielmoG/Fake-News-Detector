# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:18:42 2018

@author: guglielmo
"""

from flask import Flask
from newspaper import Article
from nltk.corpus import stopwords
import googlesearch
from difflib import SequenceMatcher
import numpy as np
from sklearn.naive_bayes import MultinomialNB

np.set_printoptions(threshold=np.NaN)
np.random.seed(34573623)

app = Flask(__name__)

#X=observationxfeatures(=urls)
#y=labels(fake or not)

#url_mapping = 

#BN_naive = MultinomialNB()
#BN_naive.fit(X,y)

@app.route('/<path:b>')
def a(b):
    return b
    
@app.route('/casa/<path:aaa>')
def b(aaa):
    return aaa

@app.route('/<path:url_name>', methods=['GET', 'POST'])
def test_maso(url_name):
    article = build(url_name)
    keys, text_origin = article.keywords, article.text
    title = article.title.replace('"',"'")
    image = article.top_image
    #json = '{"url":"%s","text":"%s","title":"%s","image":"%s"}'%(url_name, text_origin, title, image)
    json = '{"url":"%s","title":"%s","image":"%s"}'%(url_name, title, image)
    return json

#@app.route('/droidcon/<url_name>')
def get_url(url_name):
    d = {'it':'italian', 'en':'english'}
    print(1)
    article = build(url_name)
    keys, text_origin = article.keywords, article.summary
    print(article.summary)
    start = url_name.find('www')
    end = url_name.find('/', start+1)
    language = article.meta_lang
    if len(language) == 0:
        language = 'en'
    #handle case keys_clean = []
    print(2)
    print(article.meta_lang)
    keys_clean = clean_keywords(keys, d[language])
    print(3)
    query = " OR ".join(keys_clean)
    print(query)
    urls, texts = get_results(query, language, n_top=30)
    print('urls\n',urls)
    print(4)
    rank_text = compute_similarities(text_origin, texts)
    print(5)
    all_urls = [url_name[start:end]]
    all_urls.extend(urls)
    assert len(all_urls) == len(rank_text)
    prediction = predict(all_urls, rank_text)
    threshold = 0.7
    mask = rank_text > threshold
    rank_text[mask] = 4
    json = create_json(content)
    return json
    
def build(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article

def clean_keywords(keys, language='italian'):
    #could sort topwords and use binary search
    try:
        stop = stopwords.words(language)
    except OSError as ex:
        print('unknown language for article (stopwords)')
        raise
    
    keys_clean = []
    for key in keys:
        if key not in stop:
            keys_clean.append(key)
    return keys_clean

def data_extraction(text):
    #use API's
    pass

def get_results(query, lang='en', n_top=30):
    urls = googlesearch.search_news(query, num = 30)
    output = []
    text = []
    c = 0
    for url in urls:
        print('url', url, 'c', c)
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        #print(article.summary)
        text.append(article.summary)
        start = url.find('www')
        end = url.find('/', start+1)
        output.append(url[start:end])
        c += 1
        if c == n_top:
            break
    return output, text
    
def compute_similarities(text_origin, texts):
    print(text_origin, texts[0])
    rank = [1]
    for elem in texts:
        print('similarity')
        rank.append(SequenceMatcher(None, text_origin, elem).ratio())
    return np.array(rank)

def predict(all_urls, rank_text):
    print('all urls\n',all_urls)
    print('rank_text\n', rank_text)
    
def test():
    from copyleaks.copyleakscloud import CopyleaksCloud
    from copyleaks.product import Product
    cloud = CopyleaksCloud(Product.Education, 'airgommavigorsol@gmail.com', 'FB684AE9-CF20-4D36-8392-AC4497F76630')
    process = cloud.createByUrl('https://edition.cnn.com/2018/04/15/middleeast/us-uk-france-russia-un-syria-intl/index.html')
    return process