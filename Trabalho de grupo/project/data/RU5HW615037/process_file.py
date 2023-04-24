import re

from project.data import util

'''
Glossário Médico RU5HW615037.pdf
'''

OUTPUT_DIR = "output"
OUTPUT_FILE = OUTPUT_DIR + '/glossary.json'


def process_file(filename):
    text = util.read_file(filename)
    # remove form feed
    text = re.sub(r'\f', '', text)
    # process file to extract terms translation for each dictionary combination
    terms = find_terms(text)
    glossary = process_terms(terms)
    util.write_json_file(OUTPUT_FILE, glossary)


def find_terms(text):
    term = r'(.+)'
    sep = r' - '
    term_pt = r'(.+)'
    end_of_line = r'(?:\s|$)'
    return re.findall(term + sep + term_pt + end_of_line, text)


def process_terms(terms):
    dictionary = {}
    for term in terms:
        trans = util.clean(term[1])
        dictionary[term[0].strip().lower()] = {'i18n': {'pt': trans}}
    return dictionary


process_file("RU5HW615037.txt")
