import re

from project.data import util

OUTPUT_DIR = "output"


def process_file(filename):
    text = util.read_file(filename)
    text = remove_unneeded_contents(text)

    dictionary = {}
    # process the designations, the last pages with the description of each image label
    process_designations(text, dictionary)

    # the document structure is a page with images and identifiers
    # for each page we must store the title, the images and the identifies
    pages = re.findall(r'<page number="\d+" [^>]+>(.*?)</page>', text, re.DOTALL)
    for page in pages:
        process_page_with_img(page, dictionary)
    util.write_json_file(OUTPUT_DIR + '/' + "ossos.json", dictionary)


def remove_unneeded_contents(text):
    # remove "header/footer"
    text = re.sub(r'<text top="\d+" left="(1226|1227)" width="0" [^>]+>.*?</text>\s?', '', text)
    # remove page number
    text = re.sub(r'<text top="\d+" left="1203" width="35" [^>]+>.*?</text>\s?', '', text)
    return text


def process_page_with_img(page, dictionary):
    title = find_title(page).strip()
    if title:
        imgs = process_imgs(page)
        if imgs:
            identifiers = process_identifiers(page)
            section = dictionary.get(title)
            if section:
                section['imgs'] = imgs
                section['ids'] = util.merge_dicts(section['ids'], identifiers)
            else:
                dictionary[title] = {'imgs': imgs, 'ids': identifiers}


def find_title(page):
    # procurar os titulos em bold, como a sequência
    # numeração + ponto + numeração + texto
    # por exemplo '1.1 CRÂNIO: VISTA ANTERIOR - I'
    # apenas filtramos o que está top="38" para não aparecer repetido
    title_expr = r'<text top="38" [^>]*>' + get_title_expr() + r'</text>\s?'
    cont = r'(?:(?!<text[^>]*><b>\d+(?:\.\d+)+).)*'

    matches = re.findall(title_expr + cont, page, re.MULTILINE)
    title = join_title_and_clear_tags(matches)
    return title


def process_imgs(page):
    matches = re.findall(r'<image top="(\d+)" left="(\d+)" width="(\d+)" height="(\d+)" src="(.+?)"/>', page)
    return [{'name': img[4],
             'position': {
                 'top': img[0],
                 'left': img[1],
                 'width': img[2],
                 'height': img[3]
             }} for img in matches]


def process_identifiers(page):
    matches = re.findall(r'<text top="(\d+)" left="(\d+)" [^>]*><b>([a-z])\s*</b></text>', page)
    return {p[2]: {'position': {'top': p[0], 'left': p[1]}} for p in matches}


def get_title_expr():
    # o titutlo começa por bold (na sua maioria, existem casos em que é opcional)
    # seguido de um número seguido de um ponto número uma ou mais vezes
    # exemplo 1.1, 1.1.1 e pode terminar ou não num ponto
    # seguido se um espaço e depois um conjunto de carateres com o titulo
    return r'(?:<b>)?\d+(?:\.\d+)+\.?\s*[^<]+(?:</b>)?'


def process_designations(text, dictionary):
    text = re.sub(r'</?page[^>]*>\s?', '', text)

    title_expr = r'<text top="\d+" left="(?:43|621)"[^>]*>' + get_title_expr() + r'</text>\s?'
    cont = r'(?:(?!<text[^>]*><b>\d+(?:\.\d+)+).)*?'
    designation_expr = r'<text top="\d+" left="(?:43|621)"[^>]*>[a-z][a-z0-9]?\)[^<]+</text>\s?'

    matches = re.findall(r'(' + title_expr + cont + r')' + r'\s*((?:' + designation_expr + r')+)', text, re.MULTILINE)
    for title, designations in matches:
        # Concatenar os vários títulos e remover as tags para ser a chave do dicionário
        t = join_title_and_clear_tags(title)
        # Procurar as várias entradas das designações, com a letra e a 2ª letra ou dígito mais o ), no início
        descr = re.findall(r'<text[^>]*>([a-z][a-z0-9]?)\)([^<]+)</text>\s?', designations, re.MULTILINE)
        dictionary[t] = {'ids': {d[0]: {'descr': d[1].strip()} for d in descr}}


def join_title_and_clear_tags(matches):
    if matches:
        title = ''.join(matches)
        # remover as tags HTML
        title = util.clear_tags(title)

        # uniformização no para retirar o ultimo .
        # alguns sitios tem o . no final nas designações e na imagem não tem
        title = re.sub(r'((?:\d+.\d+)+)\.?(\s.+) - I+', r'\1\2 ', title)
        return title.strip()
    return ""


process_file("ossos.xml")
