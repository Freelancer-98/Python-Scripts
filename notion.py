from dotenv import load_dotenv
import requests
import os

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

def get_tags_ids(records):
    tags = dict()
    for r in records:
        id = r['id']
        tag = r['properties']['Name']['title'][0]['plain_text']
        tags[tag] = id
    return tags

def create_media(record):
    pass

def post_media(media):
    pass


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


