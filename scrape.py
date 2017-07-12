import requests
from bs4 import BeautifulSoup
import json

# list of pages that will be scaped
all_pages = ["http://www.notable-quotes.com/r/rock_n_roll_quotes.html", "http://www.notable-quotes.com/r/rock_n_roll_quotes_ii.html", "http://www.notable-quotes.com/r/rock_n_roll_quotes_iii.html", "http://www.notable-quotes.com/r/rock_n_roll_quotes_iv.html"]

# list that will become json data
quotes_with_authors = []

def scrape_page_rock_quotes(html_address, final_list):
    '''
    Gathers the text on a page that is a quote about rock and roll.

    arguments:
    html_address(string) - the address that will be requested and scraped.
    final_list(list) - A compilation of the quotes and authors store in dictionaries formatted as   {
                                        "quote": "the quote text",
                                        "author": "the attributed author and source"
                                    }.
    '''

    # request page
    quote_page = requests.get(html_address)

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

    # standardize the quotes in dictionaries
    for quote, author in quote_with_author_dict.items():
        quote_with_attribute = {
            'quote': quote,
            'author': author
            }
        # add the quote dictionary to the list that will be exported to persistent file
        final_list.append(quote_with_attribute)

    print(len(quotes_with_authors))


def dump_data_to_json_file(data_list, persistent_file):
    '''
    Make a list persistent dumping the data to a json file for use in my music API.

    Arguments:
    data_list(list) - A compilation of the quotes and authors store in dictionaries formatted as   {
                                        "quote": "the quote text",
                                        "author": "the attributed author and source"
                                    }.
    persistent_file(outside file, type json) - An external file that contains persistent data.
    '''
    print(data_list)
    # put data in json file
    with open(persistent_file, 'w') as datafile:
        json.dump(data_list, datafile)

if __name__ == '__main__':
    for page in all_pages:
        scrape_page_rock_quotes(page, quotes_with_authors)
    dump_data_to_json_file(quotes_with_authors, "quotes-data.json")

