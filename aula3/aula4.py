import re

def limpa (text):
    re.sub(r"\s+", "", text)
    return text.strip()

ficheiro = open("dicionario_medico.xml", "r", encoding="utf-8")
text = ficheiro.read()
text = re.sub(r"<\?page.*>","", text)
text = re.sub(r"</?text.*?>","", text)
lista = re.findall(r"<b>(.*)</b>([^<]*)", text)
lista = [(designacao, limpa(descricao)) for designacao, descricao in lista]
dicionario = {}
print(lista)

