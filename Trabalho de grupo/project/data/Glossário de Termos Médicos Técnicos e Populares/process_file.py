import json
import re

file = open("Glossário de Termos Médicos Técnicos e Populares.txt", "r", encoding="utf-8")
text = file.read()

# Definir a expressão regular para extrair explicaçoes e termos
pattern = (r'^(.*?)\s*\((pop)\)\s*,\s*(.*?)$')

# Criar uma lista de tuplas (explicação, termo)
matches = re.findall(pattern, text, re.MULTILINE)

# Ordenar as tuplas por termo
sorted_matches = sorted(matches, key=lambda x: x[2])

file = open('glossario_limpo.txt', 'w')
for match in matches:
    file.write(f"Termo: {match[2]}\n")
    file.write(f"Explicação: {match[0]}\n\n")

glossario = {}
for entry in sorted_matches:
    glossario[entry[2].strip().lower()] = {'pop': entry[0]}

jsonfile = open("glossario.json", "w", encoding="utf-8")

json.dump(glossario, jsonfile, ensure_ascii=False, indent=4)
