import requests
from bs4 import BeautifulSoup
import extracter

def save(html, path):
    with open(path, 'w') as f:
        f.write(BeautifulSoup(html, 'html.parser').prettify())

def open_html(filename):
    with open(filename, 'r') as f:
        return f.read()

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

url = 'https://www.eldiariomontanes.es'
for name in url.split('https://www.'):
    if '.' in name:
        filename = name.split('.')[0] + '.html'
        break
r = requests.get(url)
save(r.text, filename)
extracted_info = extracter.extract_urls(open_html(filename))