import re

from project.data import util

OUTPUT_DIR = "output"
FILE_NAME_PREFIX = "anatomia geral"


def process_file(filename):
    text = util.read_file(filename)
    # remove tags <fontspec ../>
    text = re.sub(r'\t<fontspec .*>\n', r'', text)

    # the document structure is a page with the numbers the designation and an optional description
    # and following a page containing the corresponding images and numbers
    # so let's process the document page by page
    # Find all pages
    pages = re.findall(r'<page number="(\d+)"[^>]+>(.*?)</page>', text, re.DOTALL)
    dictionary = []
    for page in pages:
        imgs = re.findall(r'<image top="(\d+)" left="(\d+)" width="(\d+)" height="(\d+)" src="(.+?)"/>', page[1])
        if imgs:
            process_images(dictionary, imgs, page)
        else:
            process_terms(dictionary, page)

    util.write_json_file(OUTPUT_DIR + '/' + FILE_NAME_PREFIX + ".json", dictionary)


def process_terms(dictionary, page):
    id = r'<text [^>]*>\s*(\d+)</text>\n'
    term = r'<text [^>]*>(?:<(?:b|i)>)+([^>]+)(?:</(?:b|i)>)+</text>'
    descr = r'((?:(?!' + id + ').*\s?)*)'
    terms = re.findall(id + term + descr, page[1])

    new_terms = {term[1].strip(): {'id': term[0].strip(), 'descr': util.clear_tags(term[2])} for term in terms}

    dictionary.append({'terms': new_terms})


def process_images(dictionary, imgs, page):
    ids = extract_ids(page)
    images = extract_images(imgs)
    add_ids_and_images(dictionary, ids, images)


def extract_ids(page):
    ids_expr = r'<text top="(\d+)" left="(\d+)" width="\d+" height="\d+" font="\d+">(\d+)(?:;\s)?(\d*)</text>\s?'
    matches = re.findall(ids_expr, page[1])
    ids = {}
    for p in matches:
        pos = {'top': p[0], 'left': p[1]}
        ids[p[2]] = pos
        if p[3]:
            ids[p[3]] = pos
    return ids


def extract_images(imgs):
    return [{'name': img[4],
             'position': {'top': img[0], 'left': img[1], 'width': img[2], 'height': img[3]}}
            for img in imgs]


def add_ids_and_images(dictionary, ids, images):
    # get the last processed page
    terms = dictionary[-1]
    terms['imgs'] = images
    terms['ids'] = ids

    for term, prop in terms['terms'].items():
        pos = ids.get(prop['id'])
        prop['position'] = pos


process_file("anatomia geral.xml")
