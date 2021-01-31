from env.pocket_credentials import consumer_key, access_token
from env.gsheet_config import pocket_spreadsheet, pocket_range
from extract.pocket import extract_pocket, extract_gsheet
from transform.pocket import get_new_items, get_current_week_stats, get_random_older_article
from load.gsheet import Gsheet
from datetime import datetime
from helpers import create_pocket_template, send_pocket_notification

# Workflows
def update_pocket(consumer_key, access_token, pocket_spreadsheet, pocket_range):
    print(f"Extracting pocket articles via pockexport... ⏳")
    extract_pocket(consumer_key, access_token)
    print(f"Extraction complete... ✔️")
    print(f"Updating GSheet... ⏳")
    pocket_new_data = get_new_items()
    pocket_spreadsheet = Gsheet(pocket_spreadsheet, pocket_range)
    pocket_spreadsheet.clear()
    pocket_spreadsheet.update('USER_ENTERED', {'values': pocket_new_data})
    print(f"Updation complete... ✔️")

def send_weekly_stat():
    print(f"Sending weekly stats... ⏳")
    weekly_stats = get_current_week_stats()
    weekly_template = create_pocket_template(weekly_stats)
    send_pocket_notification(f"{datetime.today().strftime('%d-%m-%Y')} ending week pocket stats", weekly_template)
    print(f"Sent weekly stats... ✔️")

def send_random():
    print(f"Sending weekly random article... ⏳")
    random_article = get_random_older_article()
    random_template = create_pocket_template(random_article)
    send_pocket_notification(f"{datetime.today().strftime('%d-%m-%Y')} ending week random article", random_template)
    print(f"Sent weekly random article... ✔️")

if __name__ == '__main__':
    update_pocket(consumer_key, access_token, pocket_spreadsheet, pocket_range)
    send_weekly_stat()
    send_random()


