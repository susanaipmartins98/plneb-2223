# Ex 1. Programa que pergunta ao utilizador o nome e imprime em maiúsculas.
nome = input("Introduza o seu nome?\n")
print("NOME:" , nome.upper())


# Ex 2. Função que recebe array de números e imprime números pares.
def numeropar():
    array = [1,2,3,4,5,6,7,8,9,10]
    for i in array:
        if i% 2 == 0:
            print(i)

numeropar()


# Ex3. Função que recebe nome de ficheiro e imprime linhas do ficheiro em ordem inversa.

filename = input("Nome do ficheiro ")

def reverseorder(filename):

    with open(filename, 'r') as file:
        lines = file.readlines()
        reverselines = lines[::-1]

        for line in reverselines:
            print(line.strip())

reverseorder(filename)


# Ex4. Função que recebe nome de ficheiro e imprime número de ocorrências das 10 palavras mais frequentes no ficheiro




# Ex5. Função que recebe um texto como argumento e o ”limpa”:
# separa palavras e pontuação com espaços,
# converte para minúsculas,
# remove acentuação de caracteres, etc.





# Create a function that:
# Ex 1. given a string “s”, reverse it.


def reverse_string(string):
    print("A string invertida é: ", string[::-1])

reverse_string(string)

# Ex 2. given a string “s”, returns how many “a” and “A” characters are present in it.
def count_aA(s):
    total = 0
    for c in s:
        if c == "a" or c == "A":
            total += 1
    return total


frase = 'O tempo perguntou ao tempo, quanto tempo ele tem! O tempo tem TANTO tempo, que nem tempo o tempo tem.'
print('A frase "{}" tem {} aA(s).'.format(frase, count_aA(frase)))


# Ex 3. given a string “s”, returns the number of vowels there are present in it.



# Ex 4. given a string “s”, convert it into lowercase.
def convert_lowercase(string):
    print(string.lower())

convert_lowercase(string)



# Ex 5. given a string “s”, convert it into uppercase.

def convert_uppercase(string):
    print(string.upper())

convert_uppercase(string)