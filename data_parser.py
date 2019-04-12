import json
import csv
import time
import urllib.parse as urlparse
import re
import string

start = time.time()

with open('data/lcquad_qaldformat.json',encoding="utf8") as datafile:
    data = json.load(datafile)
    output_data = []
    for idx, question in enumerate(data['questions']):
        eng = question['question'][0]['string']

        sparql = question['query']['sparql']
        eng_sparql = [eng, sparql]
        output_data.append(eng_sparql)

with open('eng-sparql.txt', mode='w',newline='',encoding="utf8") as engsparql_file:
    file_writer = csv.writer(engsparql_file, delimiter=',')
    for q in output_data:
        file_writer.writerow([q[0], q[1]])

end = time.time()
print(end - start)


