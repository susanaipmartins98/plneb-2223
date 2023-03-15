import re

file = open("dicionario_medico.txt", "r", encoding="utf-8")
text = file.read()

search_term_ff = re.findall(r"\f.+\n[A-ZÁÉÍÓÚÀÂÊÔÃÕÇ].+", text)
new_text = ""
for entry in search_term_ff:
    new_text += f"""
{entry}
"""


print(new_text)

newfile1 = open("0_search.txt", "w", encoding="utf-8")
newfile1.write(new_text)