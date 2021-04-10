from env.pocket_credentials import consumer_key, access_token
from src.pocket import extract_pocket

def main():
    extract_pocket(consumer_key, access_token)

if __name__ == '__main__':
    main()


