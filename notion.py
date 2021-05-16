from dotenv import load_dotenv
import requests
import os
import json

'''
Return : records    : Rows of the media list database in Notion
                    : {properties : field : {}}
'''
def get_media_records():
    all_records_resp = requests.post( f'https://api.notion.com/v1/databases/{MEDIA_DB_ID}/query', headers={ 'Authorization' : NOTION_TOKEN } )
    if all_records_resp.status_code == 200 :
        return all_records_resp.json()
    else :
        return {'Error' : all_records_resp.status_code}

def get_pocket_records():
    pocket_resp = requests.get('https://nilshah98.github.io/Knowledge-Lake/data/pocket.json')
    if pocket_resp.status_code == 200 :
        return pocket_resp.json()
    else:
        return {'Error' : pocket_resp.status_code}

def get_tags_records():
    tags_resp = requests.post( f'https://api.notion.com/v1/databases/{TAGS_DB_ID}/query', headers={ 'Authorization' : NOTION_TOKEN } )
    if tags_resp.status_code == 200:
        return tags_resp.json()
    else:
        return {'Error' : tags_resp.status_code}

'''
Input   : records       : Rows of the media list database in Notion
                        : {properties : field : {}}
Return  : title_author  : Set('<title>_<author1>_<author2>')
                        : If multiple authors are there, they will be sorted alphabetically
'''
def get_media_ids(records):
    title_authors = set()
    for r in records:
        authors = []
        if r['properties']['Title']['title']:
            title = r['properties']['Title']['title'][0]['plain_text']
            authors = list(map(lambda x : x['name'], r['properties']['Author']['multi_select']))
            authors.sort()
            title_authors.add(title + '_' + ('_').join(authors))
    return title_authors

def get_pocket_ids(records):
    title_authors = set()
    for r in records.values():
        title = r['title']
        authors = r['author']
        authors.sort()
        title_authors.add(title + '_' + ('_').join(authors))
    return title_authors

'''
Input   : records       : Rows of the tags database in Notion
                        : {properties : field : {}}
Return  : tags : { tag_name : tag_id }
'''
def get_tags_ids(records):
    tags = dict()
    for r in records:
        id = r['id']
        tag = r['properties']['Name']['title'][0]['plain_text']
        tags[tag] = id
    return tags

def create_media(record, tags_db):
    payload = dict()
    payload['parent'] = {'database_id': MEDIA_DB_ID}
    payload['properties'] = dict()
    props = payload['properties']
    props['Link'] = {'url' : record['link']}
    props['Date'] = {'date': {'start': record['time_read']}}
    props['Media'] = {'select': {'name': 'Article'}}
    props['Title'] = {'title': [ 
                            {'text' : { 'content' : record['title'] } }
                            ]}
    props['Tags'] = {'relation': []}
    for t in record['tags'] : 
        if t in tags_db.keys():
            props['Tags']['relation'].append({'id' : tags_db[t]})
        else:
            pass
    # props['Author'] = {'multi_select': []}
    # for a in record['author']:
    #     props['Author']['multi_select'].append({'name' : a})
    return payload

def post_media(media):
    create_page_resp = requests.post(f'https://api.notion.com/v1/pages', headers={ 'Authorization' : NOTION_TOKEN, 'Notion-Version' : NOTION_VERSION }, json=media)
    if create_page_resp.status_code == 200:
        return True
    else:
        print(create_page_resp.text)
        print(create_page_resp.reason)
        return False

if __name__ == '__main__':
    load_dotenv()
    NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
    NOTION_VERSION = os.environ.get('NOTION_VERSION')
    MEDIA_DB_ID = os.environ.get('MEDIA_DB_ID')
    TAGS_DB_ID = os.environ.get('TAGS_DB_ID')

    '''
    Steps -
    0. Get all the DB items
        0.a Get Pocket DB
        0.b Get Media DB
        0.c Get Tags DB
    1. Get IDs for Media & Tags DB
    2. Get diff b/w Pocket and Media
        2.a Get Pocket ID
        2.b Compare w/ Media IDs
    3. Create new page payload for the dif
    4. Post the payload to create page

    Future -
    5. Add block to the newly created page and append annotations
    '''

    # Step 0.
    pocket_db = get_pocket_records()
    media_db = get_media_records()
    tags_db = get_tags_records()

    # Step 1.
    media_ids = get_media_ids(media_db['results'])
    tags_ids = get_tags_ids(tags_db['results'])

    # Step 2.
    # Instead of ids can use index, if it is an array.
    new_ids = []
    for k,p in pocket_db.items():
        title = p['title']
        authors = p['author']
        authors.sort()
        p_id = title + '_' + ('_').join(authors)

        if p_id not in media_ids :
            new_ids.append(k)

    for id in new_ids[:1] :
        # Step 3.
        payload = create_media(pocket_db[id], tags_ids)

        # Step 4.
        if post_media(payload):
            print(f'Created { id } page')
        else:
            print('Error')



