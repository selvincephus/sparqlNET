###################################################################################################
#  Written by Selvin Cephus Jayakumar
#  Processing the sparql queries to be "learnable" in training.
#  The following tokens were created,
#  http://dbpedia.org/resource/ - dbpedia resource
#  http://dbpedia.org/ontology/ - dbpedia ontology
#  http://www.w3.org/1999/02/22-rdf-syntax-ns#type - 22rdfsyntaxnstype
#  http://dbpedia.org/property/ - dbpedia property
#  < - starturl
#  > - endurl
#  ( - openbrace
#  ) - closebrace
###################################################################################################

import urllib.parse as urlparse
import re
import string

class SparqlPostprocessing:
    def __init__(self):
        pass
        # query = "SELECT DISTINCT ?uri WHERE openbrace ?uri closebrace starturl dbpedia ontology creator endurl starturl dbpedia resource Bill Finger endurl . ?uri starturl rdfsyntaxnstype endurl starturl dbpedia ontology ComicsCharacter endurl"
        # sparql_tokens = query.split(' ')
    def sparqilise(self, query):
        query = query.replace("starturl", " <")
        query = query.replace("endurl", "> ")
        query = query.replace("openbrace", " (")
        query = query.replace("closebrace", ") ")

        if re.search("dbpedia resource", query):
            query = query.replace("dbpedia resource", "http://dbpedia.org/resource/")

        if re.search("dbpedia ontology", query):
            query = query.replace("dbpedia ontology", "http://dbpedia.org/ontology/")

        if re.search("rdfsyntaxnstype", query):
            query = query.replace("rdfsyntaxnstype", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

        if re.search("dbpedia property", query):
            query = query.replace("dbpedia property", "http://dbpedia.org/property/")

        return query

