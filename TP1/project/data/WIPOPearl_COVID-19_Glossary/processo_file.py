import re

from project.data import util

OUTPUT_DIR = "output"


def process_file(filename):
    text = util.read_file(filename)
    text = remove_unneeded_contents(text)
    glossary = process_translations(text)
    util.write_json_file(OUTPUT_DIR + "/glossary.json", glossary)


"""
    term_expr = r'((?:<text [^>]* height="15" font="8"><b>[^<]+</b></text>\s*)+)'
    syn_expr = r'(<text [^>]*><i>\(syn\.\)\s*</i></text>\s*<text [^>]*>[^<]+</text>\s*)?'
    descr_expr = r'((?:<text [^>]* height="12" font="6">[^<]+</text>\s*)+)'
    tag_expr = r'((?:<text [^>]* height="11" font="11">[^<]+</text>\s*)+)'
    not_end_of_file = r'(?!<text top="958")'
    trad = r'((?:' + not_end_of_file + r'[^>]*>(?:<i>)?[^<]+(?:</i>)?</text>\s*)+)'
    ar = r'<text [^>]*><b>\s*(AR)</b></text>\s*' + trad
    de = r'<text [^>]*><b>(DE)\s*</b></text>\s*' + trad
    es = r'<text [^>]*><b>(ES)\s*</b></text>\s*' + trad
    fr = r'<text [^>]*><b>(FR)\s*</b></text>\s*' + trad
    ja = r'<text [^>]*><b>(JA)\s*</b></text>\s*' + trad
    ko = r'<text [^>]*><b>(KO)\s*</b></text>\s*' + trad
    pt = r'<text [^>]*><b>(PT)\s*</b></text>\s*' + trad
    ru = r'<text [^>]*><b>(RU)\s*</b></text>\s*' + trad
    zh = r'<text [^>]*><b>(ZH)\s*</b></text>\s*' + trad

    matches = re.findall(term_expr + syn_expr + descr_expr + tag_expr + ar + de + es + fr + ja + ko + pt + ru + zh,
                         text, re.MULTILINE)
"""

LANG = ['AR', 'DE', 'ES', 'FR', 'JA', 'KO', 'PT', 'RU', 'ZH']


def process_translations(text):
    term_expr = r'((?:<text [^>]* height="15" font="8"><b>[^<]+</b></text>\s*)+)'
    syn_expr = r'(<text [^>]*><i>\(syn\.\)\s*</i></text>\s*<text [^>]*>[^<]+</text>\s*)?'
    descr_expr = r'((?:<text [^>]* height="12" font="6">[^<]+</text>\s*)+)'
    tag_expr = r'((?:<text [^>]* height="11" font="11">[^<]+</text>\s*)+)'
    not_end_of_file = r'(?!<text top="958")'
    trad_expr = r'((?:' + not_end_of_file + r'[^>]*>(?:<i>)?[^<]+(?:</i>)?</text>\s*)+)'
    all_lang_expr = ""
    for lang in LANG:
        all_lang_expr += r'<text [^>]*><b>\s*(' + lang + r')\s*</b></text>\s*' + trad_expr

    matches = re.findall(term_expr + syn_expr + descr_expr + tag_expr + all_lang_expr, text, re.MULTILINE)
    glossary = {}
    for m in matches:
        term = util.clear_tags(m[0])
        syn = util.clear_tags(m[1])
        descr = util.clear_tags(m[2])
        tag = util.clear_tags(m[3])
        i18n = {}
        i = 4
        for _ in LANG:
            i18n[m[i].lower()] = util.clear_tags(m[i + 1])
            i += 2
        glossary[term] = {'syn': syn, 'descr': descr, 'tag': tag, 'i18n': i18n}
    return glossary


def remove_unneeded_contents(text):
    # remove empty lines
    text = re.sub(r'<text [^>]+>\s+</text>\s?', '', text)
    # remove page tag
    text = re.sub(r'</?page[^>]*>\s?', '', text)
    # remove fontspec
    text = re.sub(r'<fontspec[^>]*/>\s?', '', text)
    # remove page number
    text = re.sub(r'<text top="1158" [^>]*>\d+\s*</text>', '', text)
    # remove header
    text = re.sub(r'<text top="65" [^>]*>[^<]*</text>', '', text)

    return text


process_file("WIPOPearl_COVID-19_Glossary.xml")
