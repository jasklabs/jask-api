# Derived from: https://gist.githubusercontent.com/stantonk/b0a937ca9c035a83b14c/raw/bff09b6977579057cec7812e41d2e486a07a14b2/get_valid_tlds.py
# Daniel Smallwood, Jask Labs Inc.
# Jan 2017
# requirements.txt
# pip install requests
# pip install BeautifulSoup4

import codecs
import requests
from bs4 import BeautifulSoup

PER_LINE = 12

text = requests.get('http://www.iana.org/domains/root/db').text
soup = BeautifulSoup(text, "html.parser")
x = soup.find('table', {'id': 'tld-table'})
#tlds = [anchor.text for anchor in x.find_all('a')]
tld_uris = [anchor.attrs['href'] for anchor in x.find_all('a')]
tlds = []
for uri in tld_uris:
    fields = uri.split("/")
    fields = fields[-1].split(".")
    tlds.append(fields[0])

print tlds
