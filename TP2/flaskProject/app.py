import json
import re

from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

with open("database_files/database.json", encoding="UTF8") as file:
    db = json.load(file)

with open("database_files/anatomia_atualizado.json", encoding="UTF8") as file:
    anatomy_db = json.load(file)

with open("database_files/bones.json", encoding="UTF8") as file:
    bd_bones = json.load(file)

with open("database_files/bones_definition.json", encoding="UTF8") as file:
    bd_bones_definition = json.load(file)


# Rota para a página principal
@app.route('/')
def home():
    return render_template('home.html', title="Home")


# Rota para a o glossário
@app.route('/glossary', methods=['GET', 'POST'])
def glossary():
    glossary = db['Glossary']
    if request.method == 'POST':
        search_text = request.form.get("search_text")
        result = {}
        if search_text:
            for designation, content in glossary.items():
                if re.search(search_text, designation, flags=re.I):
                    result[designation] = content
            return render_template('glossary.html', glossary=result, search_text=search_text, title="Glossary")

    return render_template('glossary.html', glossary=db['Glossary'], title="Glossary")


@app.route('/glossary/<term>')
def glossary_term(term):
    term_data = db['Glossary'].get(term, {"term": term, 'notfound': 'Does not exist!'})

    return render_template('term.html', term=term, term_data=term_data, title="Glossary Term")


@app.route('/glossary/edit/<term>', methods=['GET', 'POST'])
def edit_term(term):
    glossary = db['Glossary']

    if request.method == 'POST':
        data = request.get_json()
        syn = data.get('syn')
        descr = data.get('descr')
        tag = data.get('tag')
        translations = data.get('i18n')

        term_data = glossary.get(term)
        if term_data:
            term_data['syn'] = syn
            term_data['descr'] = descr
            term_data['tag'] = tag
            term_data['i18n'] = translations
        return {term: term_data}
    else:
        # Renderizar o formulário de edição com os dados atuais do termo
        term_data = glossary.get(term, {"term": term, 'notfound': 'Does not exist!'})
        return render_template('edit_term.html', term=term, term_data=term_data)


@app.route("/glossary/<term>", methods=["DELETE"])
def delete_glossary_term(term):
    glossary = db['Glossary']
    content = glossary.get(term)
    if content:
        print(content)
        del glossary[term]
        print(glossary.get(term))
        file_save = open("database_files/database.json", "w")
        json.dump(db, file_save, ensure_ascii=False, indent=4)
        file_save.close()

    return {term: content}


@app.route('/dictionary')
def dictionary():
    dic = db['dictionary']
    return render_template('dictionary.html', dictionary=dic, title="Dictionary")


@app.route('/dictionary/<lang>')
def dictionary_lang(lang):
    lang_dict = db['dictionary'].get(lang)
    return render_template('dictionary.html', dictionary=db['dictionary'].keys(), lang_dict=lang_dict, lang=lang,
                           title="Dictionary")


# Rota para a página de anatomia
@app.route('/anatomy')
def anatomy():
    terms = []
    for term, data in anatomy_db.items():
        term_data = {
            'term': term,
            'descr': data['description'],
            'image_urls': data['image_urls']
        }
        terms.append(term_data)
    return render_template('anatomy.html', terms=terms, title="Anatomy")


@app.route('/anatomy/<term>')
def anatomy_term(term):
    term_data = anatomy_db.get(term, {})
    return render_template('anatomy_term.html', term=term, term_data=term_data, title="Anatomy Term")


# Rota para a página de ossos
@app.route('/bones')
def bones():
    return render_template('bones.html', bones=bd_bones, title="Bones")


@app.route('/bones/<category>/<groupName>')
def bone_image_route(category, groupName):
    sections = bd_bones.get(category)
    if sections:
        groupData = sections.get(groupName)
        return render_template('bone_image.html', category=category, groupName=groupName, groupData=groupData,
                               title="Bones")
    return render_template('bone_image.html', category=category, groupName=groupName, groupData={}, title="Bones")


@app.route('/bones/definition/<name>')
def bone_definition_route(name):
    bone = bd_bones_definition.get(name)
    if bone:
        return render_template('bone_definition.html', bone=bone, name=name, title="Definition")
    return render_template('bone_definition.html', name=name,
                           bone={"notfound": "Definition not available at the moment!"},
                           title="Definition")


if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)