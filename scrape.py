import requests
from bs4 import BeautifulSoup
import json

# request page
quote_page = requests.get("http://www.notable-quotes.com/r/rock_n_roll_quotes.html")

# use BeautifulSoup to parse data
souped_quote_page = BeautifulSoup(quote_page.content, 'html.parser')

# store list of quotes on page
quote_raw = souped_quote_page.find_all(class_="quotation")
quote_list = []
for quote in quote_raw:
    quote_list.append(quote.get_text())

# store list of authors
author_raw = souped_quote_page.find_all(class_="attribution")
author_list = []
for author in author_raw:
    author_list.append(author.get_text())

# dict to store quote / author
quote_with_author_dict = dict(zip(quote_list, author_list))
# list that will become json data
quotes_with_authors = []

# standardize the quotes in dictionaries
for quote, author in quote_with_author_dict.items():
    quotes_with_authors.append({
        'quote': quote,
        'author': author
        })

print(quotes_with_authors)

# put data in json file
with open('quotes-data.json', 'w') as datafile:
    json.dump(quotes_with_authors, datafile)




