import pockexport.export
import json
from datetime import datetime

def extract_pocket(consumer_key, access_token):
    # 01. Extracting everything
    pocket_data = pockexport.export.get_json(consumer_key=consumer_key, access_token=access_token)    

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
    
    with open('pocket.json', 'w+') as outfile:
        json.dump(pocket_clean,outfile,indent=2)