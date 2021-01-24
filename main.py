from env.pocket_credentials import consumer_key, access_token
from env.gsheet_config import pocket_spreadsheet, pocket_range
from extract.pocket import extract_pocket, extract_gsheet
from transform.pocket import get_new_items
from load.gsheet import Gsheet

if __name__ == '__main__':
    extract_pocket(consumer_key, access_token)
    extract_gsheet(pocket_spreadsheet, pocket_range)
    pocket_new_data = get_new_items()
    pocket_spreadsheet = Gsheet(pocket_spreadsheet, pocket_range)
    pocket_spreadsheet.append('INSERT_ROWS', 'USER_ENTERED', {'values': pocket_new_data})

