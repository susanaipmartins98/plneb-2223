import re

from project.data import util

'''
CIH Bilingual Medical Glossary English-Spanish.xml
'''

OUTPUT_DIR = "output"
OUTPUT_FILE = OUTPUT_DIR + '/' + 'glossary.json'


def process_file(filename):
    text = util.read_file(filename)
    text = remove_unneeded_contents(text)
    areas = find_areas(text)
    glossary = process_terms(areas)
    process_prefix_root_suffix(text)
    util.write_json_file(OUTPUT_FILE, glossary)


def process_prefix_root_suffix(text):
    prefixes = process_words_meaning(find_prefixes(text))
    roots = process_words_meaning(find_roots(text))
    suffixes = process_words_meaning(find_suffixes(text))

    prefix_root_suffix_glossary = {'Prefixes': prefixes, 'Roots': roots, 'Suffixes': suffixes}
    util.write_json_file(OUTPUT_DIR + '/prefix_root_suffix_glossary.json', prefix_root_suffix_glossary)


# Remove any elements from the xml that are not needed
def remove_unneeded_contents(text):
    # Remove any lines that only have spaces in bold - (in bold when is the table header and only spaces for the lines)
    result = re.sub(r'<text [^>]*>(<b>)?\s+(</b>)?</text>\s?', "", text, 0, re.MULTILINE)
    return result


def find_areas(text):
    # Each area consists of a line with left="108" and with some bold text
    #   followed by one or more lines just with spaces. (in bold when is the table header and only spaces for the lines)
    #   followed by another line with left="486" (Spanish part)

    # In this case, we will ignore the headers ([^<]*?) getting all that are not in bold
    area_en = r'<text[^>]*left="108" [^>]*>([^<]*?)</text>\s?'
    area_es = r'<text[^>]*left="486" [^>]*>([^<]*?)</text>\s?'
    area = area_en + area_es
    return re.findall(area, text, re.MULTILINE)


def process_terms(terms):
    glossary = {}
    for area in terms:
        term_en, term_es = area
        glossary[term_en.strip().lower()] = {'i18n': {'es': term_es.strip()}}
    return glossary


def process_words_meaning(words):
    res = {}
    for w, meaning in words:
        w = clean_tags(w)
        meaning = clean_tags(meaning)
        if w and meaning:
            res[w] = meaning
    return res


def find_prefixes(text):
    prefixes = find_words_meaning(text, word_left_pos='108', meaning_left_pos='184', word_right_pos='460',
                                  meaning_right_pos='528')

    # special use case that the prefix and the meaning is in the same text line
    prefix_right = re.findall(r'<text [^>]*left="460" [^>]*><i>([^<]*?-)\s\s([^<]*?)</i></text>\s?', text,
                              re.MULTILINE)

    return prefixes + prefix_right


def find_suffixes(text):
    return find_words_meaning(text, word_left_pos='108', meaning_left_pos='197', word_right_pos='440',
                              meaning_right_pos='535')


def find_roots(text):
    return find_words_meaning(text, word_left_pos='108', meaning_left_pos='224', word_right_pos='427',
                              meaning_right_pos='568')


def find_words_meaning(text, word_left_pos, meaning_left_pos, word_right_pos, meaning_right_pos):
    word_left = r'((?:<text [^>]*left="' + word_left_pos + r'" [^>]*><i>[^<]*?</i></text>\s?)+?)'
    meaning_left = r'((?:<text [^>]*left="' + meaning_left_pos + r'" [^>]*><i>[^<]*?</i></text>\s?)+?)'
    word_right = r'((?:<text [^>]*left="' + word_right_pos + r'" [^>]*><i>[^<]*?</i></text>\s?)+?)'
    meaning_right = r'((?:<text [^>]*left="' + meaning_right_pos + r'" [^>]*><i>[^<]*?</i></text>\s?)+?)'
    return re.findall(word_left + meaning_left, text, re.MULTILINE) + \
           re.findall(word_right + meaning_right, text, re.MULTILINE)


def clean_tags(area):
    return re.sub(r'<text [^>]*><i>(.+?)</i></text>\s?', r'\1', area).strip()


process_file("CIH Bilingual Medical Glossary English-Spanish.xml")
