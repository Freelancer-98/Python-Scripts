from env.pocket_credentials import consumer_key, access_token
from env.gsheet_config import pocket_spreadsheet, pocket_range
from extract.pocket import extract_pocket, extract_gsheet
from transform.pocket import get_all_items
from load.gsheet import Gsheet

if __name__ == '__main__':
    extract_pocket(consumer_key, access_token)
    pocket_all_data = get_all_items()
    pocket_spreadsheet = Gsheet(pocket_spreadsheet, pocket_range)
    pocket_spreadsheet.update('USER_ENTERED', {'values': pocket_all_data})

