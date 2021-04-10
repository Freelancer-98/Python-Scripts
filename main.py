import os
from src.pocket import extract_pocket

POCKET_CONSUMER_KEY = os.environ.get('POCKET_CONSUMER_KEY')
POCKET_ACCESS_TOKEN = os.environ.get('POCKET_ACCESS_TOKEN')

def main():
    extract_pocket(POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN)

if __name__ == '__main__':
    main()


