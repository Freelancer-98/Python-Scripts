import os
from src.pocket import extract_pocket, get_pocket_email_data
from src.notification import create_pocket_template, send_email_notification
from datetime import datetime
import argparse

POCKET_CONSUMER_KEY = os.environ.get('POCKET_CONSUMER_KEY')
POCKET_ACCESS_TOKEN = os.environ.get('POCKET_ACCESS_TOKEN')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_RECEIVER = os.environ.get('EMAIL_RECEIVER')

def extract():
    extract_pocket(POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN)

def send_notification():
    pocket_email_data = get_pocket_email_data()
    if len(pocket_email_data[0]) :
        template = create_pocket_template(pocket_email_data[0])
        send_email_notification(EMAIL_PASSWORD, EMAIL_SENDER, EMAIL_RECEIVER,
                            f'Pocket summary for the {datetime.now().strftime("%d %B %Y")} ending week', template)
    if len(pocket_email_data[1]) :
        template = create_pocket_template(pocket_email_data[1])
        send_email_notification(EMAIL_PASSWORD, EMAIL_SENDER, EMAIL_RECEIVER,
                            f'Pocket random for the {datetime.now().strftime("%d %B %Y")} ending week', template)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--notify", help="Send notifications", action="store_true")
    parser.add_argument("-e", "--extract", help="Extract data", action="store_true")
    args = parser.parse_args()
    if(args.notify):
        send_notification()
    if(args.extract):
        extract()

if __name__ == '__main__':
    main()


