from data import util

"""
Criação do dicionário base de dados
"""
database = {}

"""
 Fazer merge dos glossários adicioná-los à base de dados
"""
glossary1 = util.read_json("data/WIPOPearl_COVID-19_Glossary/output/glossary.json")
glossary2 = util.read_json("data/RU5HW615037/output/glossary.json")
glossary3 = util.read_json("data/CIH Bilingual Medical Glossary English-Spanish/output/glossary.json")

glossary = util.merge_dicts(glossary1, glossary2)
glossary = util.merge_dicts(glossary, glossary3)

database['Glossary'] = glossary

"""
 prefixos, sufixos, roots
"""
prefix_root_suffix_glossary = util.read_json(
    "data/CIH Bilingual Medical Glossary English-Spanish/output/prefix_root_suffix_glossary.json")

database.update(prefix_root_suffix_glossary)

"""
 Dicionários
"""
# dicionario_termos_medicos
terms_en_es_pt = util.read_json("data/dicionario_termos_medicos/output/dicionario_termos_medicos_en_es_pt.json")
terms_es_en_pt = util.read_json("data/dicionario_termos_medicos/output/dicionario_termos_medicos_es_en_pt.json")
terms_pt_en_es = util.read_json("data/dicionario_termos_medicos/output/dicionario_termos_medicos_pt_en_es.json")
#
terms_pt = util.read_json("data/Dicionario_de_termos_medicos_e_de_enfermagem/output/terms.json")
merged_terms_pt_en_es = util.merge_dicts(terms_pt, terms_pt_en_es)

# Glossário de Termos Médicos Técnicos e Populares
pop = util.read_json("data/Glossário de Termos Médicos Técnicos e Populares/glossario.json")
merged_terms_pt_en_es = util.merge_dicts(merged_terms_pt_en_es, pop)

database['dictionary'] = {'pt': merged_terms_pt_en_es, 'en': terms_en_es_pt, 'es': terms_es_en_pt}

"""
Anatomia
"""
anatomia = util.read_json("data/anatomia/output/anatomia geral.json")
database['anatomy'] = anatomia

"""
Ossos
"""
ossos = util.read_json("data/ossos/output/ossos.json")
database['bones'] = ossos

"""
 Escrever o ficheiro JSON com o dicionário
"""
util.write_json_file('output/database.json', database)
