import requests
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://www.wordnik.com/words/{}'


def get_page_source_for_word(word):
    r = requests.get(BASE_URL.format(word))
    if r.status_code != 200:
        raise ConnectionError(r.reason)
    return r.content


def get_all_definitions(html):
    tree = bs(html, 'html5lib')
    container = tree.find('div', id='define')
    definitions = []
    items = container.find_all('li')
    for item in items:
        part = item.find('abbr')
        part.extract()
        definitions.append((part.text.strip(), item.text.strip()))
    return definitions
