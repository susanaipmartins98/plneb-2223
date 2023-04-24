import re

from project.data import util

'''
dicionario_termos_medicos_pt_es_en.xml

Medical Dictionary english – spanish – portuguese 
Diccionario de Medicina español – inglés – portugués 
Dicionário de termos médicos português – inglês –espanhol
'''
# Translation key mapping
EN = ('U', 'en')
ES = ('E', 'es')
PT = ('P', 'pt')

DIC = {
    'en': [ES, PT],
    'es': [EN, PT],
    'pt': [EN, ES]
}
OUTPUT_DIR = "output"
FILE_NAME_PREFIX = "dicionario_termos_medicos"


def process_file(filename):
    text = util.read_file(filename)

    # Delete lines that are positioned at top=104, with height=50 and have a single capital letter
    # These are the page headers for each letter (and could be confused with the expressions to translate)
    text = re.sub(r'<text top="104"[^>]* height="50"[^>]*><b>[A-Z]</b></text>\s?', "", text, 0, re.MULTILINE)

    # process file to extract terms translation for each dictionary combination
    for lang, trans_lang in DIC.items():
        separator1, lang1 = trans_lang[0]
        separator2, lang2 = trans_lang[1]
        terms = find_terms(separator1, separator2, text)
        dictionary = process_terms(lang1, lang2, terms)
        write_json_file(dictionary, lang, lang1, lang2)


def find_terms(separator1, separator2, text):
    """<text[^>]*><b>(.+?)</b></text>
        \s?
        <text[^>]*>E</text>
        \s?
        <text[^>]*>(.*?)</text>
        \s?
        <text[^>]*>P</text>
        \s?
        <text[^>]*>(.*?)</text>
    """
    # A term starts with bold
    term_start = r'<text[^>]*><b>.+?</b></text>\s?'
    term_italic = r'<text[^>]*><i>.+?</i></text>\s?'
    term_comma = r'<text[^>]*>,</text>\s?'
    term = r'(' + term_start + r'(?:' + term_italic + '|' + term_comma + '|' + term_start + ')*' + ')'
    sep1 = r'<text[^>]*>' + separator1 + r'</text>\s'
    trans1 = r'((?:<text[^>]*>.*?</text>\s?)+?)'
    sep2 = r'<text[^>]*>' + separator2 + r'</text>\s'
    # catch everything that doesn't start at the beginning of the term (<text[^>]*><b>)
    trans2 = r'((?:(?!' + term_start + ').*\s?)*)'

    return re.findall(term + sep1 + trans1 + sep2 + trans2, text, re.MULTILINE)


# Remove tags, line breaks in words
def clean_tags(text):
    text = re.sub(r'</?(i|b)>', "", text)
    # remove line breaks in words -
    text = re.sub(r'<text[^>]*>(.+?)-</text>\s?', r'\1', text)
    text = re.sub(r'<text[^>]*>(.+?)</text>\s?', r'\1 ', text)
    # remove spaces between a word and a comma
    text = text.replace(' ,', ',')
    # remove spaces between ()
    text = text.replace(' )', ')')
    text = text.replace('( ', '(')
    # remove multiple spaces
    text = re.sub(r'\s\s+', r' ', text)
    return text.strip()


def process_terms(lang1, lang2, terms):
    dictionary = {}
    for term in terms:
        t = clean_tags(term[0])
        trans1 = clean_tags(term[1])
        trans2 = clean_tags(term[2])
        dictionary[t] = {lang1: trans1, lang2: trans2}
    return dictionary


def write_json_file(dictionary, lang, lang1, lang2):
    filename = OUTPUT_DIR + '/' + FILE_NAME_PREFIX + "_" + lang + "_" + lang1 + "_" + lang2 + ".json"
    util.write_json_file(filename, dictionary)


process_file("dicionario_termos_medicos_pt_es_en.xml")
