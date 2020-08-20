from bs4 import BeautifulSoup
import re

vocab_list = set()

# Part 1 : Extracting words from APA Citations imported from Kindle
# Reading the highlights file
highlights_file = open('env/highlights/test.html', mode='r')
highlights_html = highlights_file.read()
highlights_file.close()

# Passing the highlights to bs4 for html parsing
highlights_soup = BeautifulSoup(highlights_html, 'html.parser')
highlights_span = highlights_soup.find_all('span', class_='highlight_blue')

# Extracting all words
for highlight in highlights_span:
    # Removing following and trailing newlines and whitespace
    word = highlight.parent.next_sibling.next_sibling.string.strip()
    # Removing all punctuation marks
    word = re.sub(r'[^\w\s]','',word)
    vocab_list.add(word)
print(vocab_list)

# Part 2 : Extracting words from Google Dictionary Chrome extension