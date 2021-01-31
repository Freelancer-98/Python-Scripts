import pickle
import json
import datetime
import random

# Get all the article ids
pocket_all = json.load(open('source/pocket/all.json'))
pocket_all_articleIds = pocket_all['list'].keys()

# Make pocket_all uniform for my use
for id in list(pocket_all_articleIds):
    article = pocket_all['list'][id]

    if 'author' not in article.keys(): article['authors'] = {}
    if 'tags' not in article.keys(): article['tags'] = {}
    if 'annotations' not in article.keys(): article['annotations'] = []
    if 'time_to_read' not in article.keys(): article['time_to_read'] = 0

def make_stat(article):
    # format - [article_link, article_name, reading_time, [tags], [annotations]]
    stat = ['','',0,[],[]]
    stat[0] = f"https://getpocket.com/read/{article['item_id']}"
    stat[1] = article['resolved_title']
    stat[2] = article['time_to_read']
    stat[3] = list(article['tags'].keys())
    stat[4] = list(map(lambda annotation: annotation['quote'], article['annotations']))
    return stat

# Get new articles in the particular format. For now, get all
def get_new_items():
    # format - [id, time_added, time_read, resolved_title, authors, url, tags, annotation, time_to_read, favorite]
    rows = []
    for id in list(pocket_all_articleIds):
        row = []
        article = pocket_all['list'][id]
        authors = map(lambda x: article['authors'][x]['name'], article['authors'].keys())
        tags = [''] + list(article['tags'].keys())
        annotations = [''] + list(map(lambda annotation: annotation['quote'], article['annotations']))

        row.append(id)
        row.append(datetime.datetime.fromtimestamp(int(article['time_added'])).strftime('%Y-%m-%d'))
        row.append(datetime.datetime.fromtimestamp(int(article['time_read'])).strftime('%Y-%m-%d'))
        row.append(article['resolved_title'])
        row.append(''.join(authors))
        row.append(article['resolved_url'])
        row.append('\n● '.join(tags))
        row.append('\n- '.join(annotations))
        row.append(article['time_to_read'])
        row.append(article['favorite'])

        rows.append(row)
    return rows

def get_current_week_stats():
    stats = []
    for id in list(pocket_all_articleIds):
        article = pocket_all['list'][id]

        time_now = datetime.datetime.today()
        time_added = datetime.datetime.fromtimestamp(int(article['time_added']))
        time_read = datetime.datetime.fromtimestamp(int(article['time_read']))

        if (time_now - time_read).days <= 7:
            stats.append(make_stat(article))
    return stats

def get_random_older_article():
    stats = []
    flag = True

    while flag:
        articleid = random.choice(list(pocket_all['list'].keys()))
        article = pocket_all['list'][articleid]

        time_now = datetime.datetime.today()
        time_added = datetime.datetime.fromtimestamp(int(article['time_added']))
        time_read = datetime.datetime.fromtimestamp(int(article['time_read']))

        if (time_now - time_read).days > 7:
            stats.append(make_stat(article))
            flag = False
        else:
            continue
    return stats





