import pocket
import json
from datetime import datetime
import requests
import random

def extract_pocket(consumer_key, access_token):

    # 00. Create a modified version of get function to take more arguments
    @pocket.method_wrapper
    def get(self, **kwargs):
        pass

    # 01. Extracting everything
    pocket_instance = pocket.Pocket(consumer_key, access_token)
    pocket_data = get(pocket_instance, tags=1, annotations=1, authors=1, 
                    state='archive', sort='newest', detailType='complete')[0]

    # 02. Cleaning data
    # Structure => { ID: { Date Read, Title, Author, Link, Tags, Annotations, Favorite, Source }, ... } 
    pocket_articles = pocket_data['list']
    pocket_clean = {}

    for id in pocket_articles.keys():
        article = pocket_articles[id]
        if article['time_read'] != "0" and len(article['resolved_title']) > 0:
            
            # 01. Uniformize the data
            if 'authors' not in article.keys(): article['authors'] = {}
            if 'tags' not in article.keys(): article['tags'] = {}
            if 'annotations' not in article.keys(): article['annotations'] = []

            # 02. Getting the required data
            time_read = datetime.fromtimestamp(int(article['time_read'])).strftime('%Y-%m-%d')
            title = article['resolved_title']
            author = list(map(lambda x: article['authors'][x]['name'], article['authors'].keys()))
            link = article['resolved_url']
            tags = list(article['tags'].keys())
            annotations = list(map(lambda annotation: annotation['quote'], article['annotations']))
            favorite = int(article['favorite'])
            source = 'pocket'

            # 03. Appending to dictionary
            pocket_clean[id] = {'time_read': time_read, 'title': title, 'author': author, 'link': link, 
                                'tags': tags, 'annotations': annotations, 'favorite': favorite, 'source': source}
    
    with open('tmp/pocket.json', 'w+') as outfile:
        json.dump(pocket_clean,outfile,indent=2)

def make_stat(row):
    stat = []
    stat.append(row['time_read'])
    stat.append(row['title'])
    stat.append(row['author'])
    stat.append(row['link'])
    stat.append(row['tags'])
    stat.append(row['annotations'])
    stat.append(row['favorite'])
    return stat
    

def get_pocket_email_data():

    # 00. Extract all pocket data
    response = requests.get('https://nilshah98.github.io/Knowledge-Lake/data/pocket.json')
    pocket_data_week = []
    pocket_random = []
    pocket_older_id = []

    # 01. Get last week
    if response.status_code == 200:
        pocket_data = response.json()
        date_now = datetime.today()
        for article in pocket_data.keys():
            date_read = datetime.strptime(pocket_data[article]['time_read'], '%Y-%m-%d')
            if (date_now - date_read).days <= 7:
                pocket_data_week.append(make_stat(pocket_data[article]))
            else:
                pocket_older_id.append(article)    
    
        # 02. Get random
        pocket_random.append(make_stat(pocket_data[random.choice(pocket_older_id)]))

    return [pocket_data_week, pocket_random]



