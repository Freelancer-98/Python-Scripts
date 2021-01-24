import json
import datetime
from gsheet_ops import get_authenticated_service, gsheet_append

pocketData = json.load(open('./pocketData.json'))
articles = pocketData['list']

rows = []
for id in articles.keys():
    row = []
    article = articles[id]

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

SAMPLE_SPREADSHEET_ID = '1-dFsoyUyyNEQfGOoApBNmikn4Tv_ggHpnT2dcgxEpNQ'
SAMPLE_RANGE_NAME = 'Sheet1!A1:J'

service = get_authenticated_service()
gsheet_append(service, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, 'INSERT_ROWS', 'USER_ENTERED', {'values': rows})