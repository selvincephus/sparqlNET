###################################################################################################
#  Parser for English-Sparql pairs from QUALD dataset
#
###################################################################################################
import json
import csv
import time
import re
import string

# start = time.time()
#
# with open('data/lcquad_qaldformat.json',encoding="utf8") as datafile:
#     data = json.load(datafile)
#     output_data = []
#     for idx, question in enumerate(data['questions']):
#         eng = question['question'][0]['string']
#
#         sparql = question['query']['sparql']
#         eng_sparql = [eng, sparql]
#         output_data.append(eng_sparql)
#
# with open('eng-sparql_tab.txt', mode='w',newline='',encoding="utf8") as engsparql_file:
#     file_writer = csv.writer(engsparql_file, delimiter=',')
#     for q in output_data:
#         file_writer.writerow({q[0]+'\t'+q[1]})
#
# end = time.time()
# print(end - start)

# import csv

in_file = r"data\eng-sparql.txt"
out_file = r"eng-sparql.txt"

with open(in_file, mode="r", encoding="utf8") as in_text:
    in_reader = csv.reader(in_text, delimiter = ',')
    with open(out_file, mode="w", encoding="utf8") as out_csv:
        out_writer = csv.writer(out_csv, delimiter='\t')
        for row in in_reader:
            out_writer.writerow(row)


