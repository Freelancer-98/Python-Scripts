from env.pocket_credentials import consumer_key, access_token
from env.gsheet_config import pocket_spreadsheet, pocket_range
from extract.pocket import extract_pocket, extract_gsheet
from transform.pocket import get_new_items, get_past_x_days_stats, get_random_older_article
from load.gsheet import Gsheet
from datetime import datetime
from helpers import create_pocket_template, send_pocket_notification
import argparse

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

def send_weekly_stat(d):
    print(f"Sending weekly stats... ⏳")
    weekly_stats = get_past_x_days_stats(d)
    weekly_template = create_pocket_template(weekly_stats)
    send_pocket_notification(f"{datetime.today().strftime('%d-%m-%Y')} ending week pocket stats", weekly_template)
    print(f"Sent weekly stats... ✔️")

def send_random(d):
    print(f"Sending weekly random article... ⏳")
    random_article = get_random_older_article(d)
    random_template = create_pocket_template(random_article)
    send_pocket_notification(f"{datetime.today().strftime('%d-%m-%Y')} ending week random article", random_template)
    print(f"Sent weekly random article... ✔️")

def main(d):
    update_pocket(consumer_key, access_token, pocket_spreadsheet, pocket_range)
    send_weekly_stat(d)
    send_random(d)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-pd", "--pocketDays", type=int, default=7, help="Fetch pocket records of past X days")
    args = parser.parse_args()
    main(args.pocketDays)


