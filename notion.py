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
Return  : title_author  : Set(<title>)
'''
def get_media_ids(records):
    media_ids = set()
    for r in records:
        if r['properties']['Title']['title']:
            title = r['properties']['Title']['title'][0]['plain_text']
            media_ids.add(title)
    return media_ids

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
    payload['children'] = []

    props = payload['properties']
    blocks = payload['children']

    props['Link'] = {'url' : record['link']}
    props['Date'] = {'date': {'start': record['time_read']}}
    props['Media'] = {'select': {'name': 'Article'}}
    props['Title'] = {'title': [ 
                                {'text' : { 'content' : record['title'] } }
                                ]}
    props['Authors'] = {'rich_text': [
                                {'text': {'content': ','.join(record['author'])}}
                            ]}
    props['Tags'] = {'relation': []}
    for t in record['tags'] : 
        if t in tags_db.keys():
            props['Tags']['relation'].append({'id' : tags_db[t]})
        else:
            tag_resp = post_tag(t)
            if 'Error' not in tag_resp.keys():
                props['Tags']['relation'].append({'id' : tag_resp['id']})
                tags_db[t] = tag_resp['id']

    blocks.append({'object' :'block', 'type': 'heading_1', 'heading_1': {
                    'text': [{'type': 'text', 'text': {'content': 'Annotations'}}]
                }})
    for a in record['annotations']:
        blocks.append({'object' :'block', 'type': 'numbered_list_item', 'numbered_list_item': {
                    'text': [{'type': 'text', 'text': {'content': a}}]
                }})
    return payload

def post_media(media):
    create_page_resp = requests.post(f'https://api.notion.com/v1/pages', headers={ 'Authorization' : NOTION_TOKEN, 'Notion-Version' : NOTION_VERSION }, json=media)
    if create_page_resp.status_code == 200:
        return True
    else:
        print(create_page_resp.text)
        return False

def post_tag(tag):
    payload = dict()
    payload['parent'] = {'database_id': TAGS_DB_ID}
    payload['properties'] = {'Name': {'title': [ 
                                                { 'text': { 'content': tag } }
                                                ]}}
    create_tag_resp = requests.post(f'https://api.notion.com/v1/pages', headers={ 'Authorization' : NOTION_TOKEN, 'Notion-Version' : NOTION_VERSION }, json=payload)
    if create_tag_resp.status_code == 200:
        return create_tag_resp.json()
    else:
        return {'Error' : create_tag_resp.text}

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
        p_id = p['title']

        if p_id not in media_ids :
            new_ids.append(k)

    for id in new_ids :
        # Step 3.
        payload = create_media(pocket_db[id], tags_ids)

        # Step 4.
        if post_media(payload):
            print(f'Created { id } page')
        else:
            print('Error')




