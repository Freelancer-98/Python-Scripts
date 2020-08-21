from bs4 import BeautifulSoup
import re
from PyDictionary import PyDictionary
from gsheet_ops import get_authenticated_service, gsheet_append

vocab_list = set()
# result_rows follow the format of => ['word', 'pos' , 'meaning', 'synonym']
result_rows = []

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

for word in vocab_list:
    rows = []
    word_meanings = PyDictionary.meaning(word)
    
    if(word_meanings):
        for pos in word_meanings.keys():
            rows.append([word, pos, "● " + "\n● ".join(word_meanings[pos])])
        
        syn = PyDictionary.synonym(word)
        if syn: rows[0].append(", ".join(syn))

        result_rows.extend(rows)

vocab_sheet = '16XwTneCe03ek7Efp3V7YYvkvxRLDsEOvbTzXOMYRBMA'
vocab_sheet_range = 'Sheet1!A1:D'

service = get_authenticated_service()
gsheet_append(service, vocab_sheet, vocab_sheet_range, 'INSERT_ROWS', 'USER_ENTERED', {'values': result_rows})

# TODO : Part 2 : Extracting words from Google Dictionary Chrome extension