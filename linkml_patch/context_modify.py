# File: context_modify.py
# Purpose: modify jsonld context file
#
import sys
import json


def main(argv):
    try:
        file = open(argv[0], 'r')
        json_object = json.load(file)
        file.close()

        json_object["@context"]["@base"] = "http://resource.isamples.org/schema/"
        json_object["@context"]['ark'] = "http://ark.org"
        json_object["@context"]["type"] = "@type"

        json_object["@context"]['hasContextCategory']["@type"] = "@vocab"
        json_object["@context"]['hasContextCategory']["@context"]["@vocab"] = "http://resource.isamples.org/vocabulary/contextcategory/"

        json_object["@context"]['hasMaterialCategory']["@type"] = "@vocab"
        json_object["@context"]['hasMaterialCategory']["@context"]["@vocab"] = "http://resource.isamples.org/vocabulary/materialtype/"

        json_object["@context"]['hasSpecimenCategory']["@type"] = "@vocab"
        json_object["@context"]['hasSpecimenCategory']["@context"]["@vocab"] = "http://resource.isamples.org/vocabulary/specimencategory/"
        print(json.dumps(json_object, indent=4))
    except IOError:
        print(f"Could not open file: {argv[0]}")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])