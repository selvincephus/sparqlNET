import json
import csv
import time
import urllib.parse as urlparse
import re
import string

url = 'http://dbpedia.org/ontology/creator'
sparql = 'SELECT DISTINCT ?uri WHERE {?uri <http://dbpedia.org/ontology/creator> ' \
         '<http://dbpedia.org/resource/Bill_Finger>  ' \
         '. ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/ComicsCharacter>}'
parsed = urlparse.urlparse(url)
# Example: 'http://dbpedia.org/ontology/creator'
# Parsed data - scheme: http/Https; hostname/netloc: dbpedia.org ;  path: /ontology/creator
print(parsed.scheme, parsed.hostname, parsed.path)
link = sparql[sparql.find("<")+1:sparql.find(">")]
print(link)
link = re.findall('\<(.*?)\>', sparql)
print(link)
print('url parsed')

infile = open('data/eng-spar.txt', mode='r', newline='', encoding="utf8")
temp = 0
for row in infile:
    # print(len(row))
    words = row.split(' ')
    # print(len(words))
    if len(words) > temp:
        temp = len(words)
    # print(row)
print(temp)
