import pickle
import json
import datetime

# Get new articles in the particular format
def get_new_items():
    # Get all the article ids
    pocket_all = json.load(open('source/pocket/all.json'))
    pocket_all_articleIds = pocket_all['list'].keys()

    # Get gsheet article ids
    with open ('source/pocket/loaded.pickle', 'rb') as f:
        pocket_loaded = pickle.load(f)
    pocket_loaded_articleIds = set(map(lambda x: x[0], pocket_loaded[1:]))

    # Get new pocket items
    pocket_new_articleIds = filter(lambda x: x not in pocket_loaded_articleIds, pocket_all_articleIds)

    rows = []
    for id in list(pocket_new_articleIds):
        row = []
        article = pocket_all['list'][id]

        row.append(id)
        row.append(datetime.datetime.fromtimestamp(int(article['time_added'])).strftime('%Y-%m-%d'))
        row.append(datetime.datetime.fromtimestamp(int(article['time_read'])).strftime('%Y-%m-%d'))
        row.append(article['resolved_title'])

        authors = []
        if 'authors' in article.keys():
            for author in article['authors']:
                authors.append(article['authors'][author]['name'])
        row.append(''.join(authors))
        
        row.append(article['resolved_url'])
        
        tags = ['']
        if 'tags' in article.keys():
            tags.extend(article['tags'].keys())
        row.append('\n● '.join(tags))
        
        annotations = ['']
        if 'annotations' in article.keys():
            annotations.extend(list(map(lambda annotation: annotation['quote'], article['annotations'])))
        row.append('\n- '.join(annotations))
        
        if 'time_to_read' in article.keys():
            row.append(article['time_to_read'])
        else:
            row.append(0)
        
        row.append(article['favorite'])

        rows.append(row)
    return rows