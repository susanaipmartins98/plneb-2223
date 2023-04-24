import re

from project.data import util

'''
Dicionario_de_termos_medicos_e_de_enfermagem.xml
'''

OUTPUT_DIR = "output"


def process_file(filename):
    text = util.read_file(filename)
    text = remove_header_and_footer(text)
    areas = find_areas(text)
    dictionary = process_terms(areas)
    util.write_json_file(OUTPUT_DIR + '/' + 'terms.json', dictionary)


# Remove headers and footers, so they don't appear in the middle of the text
def remove_header_and_footer(text):
    # headers are all <text top="75", "108" "119"
    text = re.sub(r'<text top="(75|108|)" left="\d+" width="\d+" height="11" font="20">.*</text>\s?', "", text, 0,
                  re.MULTILINE)
    text = re.sub(r'<text top="119" left="\d+" width="1" height="2" font="27">.*</text>\s?', "", text, 0, re.MULTILINE)
    # letter in header "35" "83" "88", "128"
    text = re.sub(r'<text top="(35|88)" left="\d+" width="\d+" height="185" font="17">.*</text>\s?', "", text, 0,
                  re.MULTILINE)
    text = re.sub(r'<text top="(83|128)" left="\d+" width="\d+" height="111" font="18">.*</text>\s?', "", text, 0,
                  re.MULTILINE)
    # footers are all <text top="750" e "815"
    text = re.sub(r'<text top="(750|815)" [^>]*>.*</text>\s?', "", text, 0, re.MULTILINE)
    # remove the page number "703" e "735"
    text = re.sub(r'<text top="(703|735)" left="\d+" width="\d+" height="11" font="6">.*</text>\s?', "", text, 0,
                  re.MULTILINE)
    return text


def find_areas(text):
    # Each area consists of
    term = r'(?:<text[^>]*><b>(.+)</b></text>\s?)+'
    sep = r'<text [^>]*> - </text>\s'
    descr = r'((?:(?!<text[^>]*><b>).*\s?)*)'

    return re.findall(term + sep + descr, text, re.MULTILINE)


def extract_text(text):
    text = re.sub(r'</?i>', "", text)
    matches = re.findall('<text [^>]*>\s?(.*?)-?</text>', text)
    return ''.join(matches).strip()


def process_terms(terms):
    dictionary = {}
    for term, term_descr in terms:
        dictionary[term.strip().lower()] = {'descr': extract_text(term_descr)}
    return dictionary


process_file("Dicionario_de_termos_medicos_e_de_enfermagem.xml")
