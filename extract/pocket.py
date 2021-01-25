import pockexport.export
import json
import pickle
from load.gsheet import Gsheet

def extract_pocket(consumer_key, access_token):
    pocketData = pockexport.export.get_json(consumer_key=consumer_key, access_token=access_token)
    with open('source/pocket/all.json', 'w') as outfile:
        json.dump(pocketData,outfile,indent=2)

def extract_gsheet(id, range):
    pocket_spreadsheet = Gsheet(id, range)
    pocket_spreadsheet_data = pocket_spreadsheet.get()
    if 'values' in pocket_spreadsheet_data.keys():
        pocket_spreadsheet_data = pocket_spreadsheet_data['values']
        with open('source/pocket/loaded.pickle', 'wb') as outfile:
            pickle.dump(pocket_spreadsheet_data, outfile)