import json
import os
import re


def write_json_file(filename, dictionary):
    print('Generating file "{}"'.format(filename))
    with open(filename, "w", encoding="UTF8") as fw:
        json.dump(dictionary, fw, ensure_ascii=False, indent=2)


def read_file(filename):
    with open(filename) as f:
        return f.read()


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def clean(term):
    return term.strip().replace('\n', ' ')


def clear_tags(text):
    return re.sub(r'(<.*?>|\n)', '', text).strip()


def merge_json_files(file1, file2, file_output_name):
    #  read file 1
    json_content_1 = {}
    if os.path.exists(file1):
        with open(file1, 'r') as f1:
            json_content_1 = json.load(f1)

    #  read file 2
    json_content_2 = {}
    if os.path.exists(file2):
        with open(file2, 'r') as f2:
            json_content_2 = json.load(f2)

        # Create a new dictionary
    merge = merge_dicts(json_content_1, json_content_2)
    write_json_file(file_output_name, merge)


def merge_dicts(d1, d2):
    merge = d1.copy()
    for key, value in d2.items():
        if key in merge:
            if isinstance(merge[key], dict) and isinstance(value, dict):
                merge[key] = merge_dicts(merge[key], value)
            elif isinstance(merge[key], list) and isinstance(value, list):
                merge[key] = merge[key] + value
            else:
                merge[key] = value
        else:
            merge[key] = value
    return merge
