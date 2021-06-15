# Import das Bibliotecas Utilizadas
import sys, re
import pandas as pd
from os import system, name
# Colocando número máx de recurções
sys.setrecursionlimit(200)

end = False

# Definindo Cores Para O Terminal
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
END = "\033[m"

# Código para limpar o terminal
def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

# Definindo a função do calculo do Conjunto First
def first_calc(caracteres):
    # Iniciando a Variável first
    first = set()

    # Verificando se o caractere recebido é terminal ou não
    if caracteres in n_terminal:
        alters = regras_dict[caracteres]
        # Verificando se o caractere recebido é o primeiro ou não e une first2 a first
        for alter in alters:
            first2 = first_calc(alter)
            first = first | first2

    # Se o caractere for terminal atribui ao first
    elif caracteres in terminal:
        first = {caracteres}
    # Se o caractere for '' ou 'ε', logo será atribuído ao first
    elif caracteres == '' or caracteres == 'ε':
        first = {'ε'}

        # Se o caractere não for terminal
    else:
        # Faz uma chamada recursiva da função no indice '0'
        first2 = first_calc(caracteres[0])
        if 'ε' in first2:
            # inicializa o contador
            i = 1
            # Enquanto existir 'ε' em first2 retira {'ε'} unindo first com first2
            while 'ε' in first2:
                first = first | (first2 - {'ε'})

                 # Se o caractere no indice i for terminal insere o caractere em first
                if caracteres[i:] in terminal:
                    first = first | {caracteres[i:]}
                    break
                # Ou se o caractere no indice i for '' o first será a união first | {'ε'}
                elif caracteres[i:] == '':
                    first = first | {'ε'}
                    break
                # Chama recursivamente a função de first_calc() no caractere de indice i, atribui ele a variável first, incrementa i
                first2 = first_calc(caracteres[i:])
                first = first | first2 - {'ε'}
                i += 1
        # Senão first será first|first2
        else:
            first = first | first2
    # Retorna a variável first
    return first

def follow_calc(nT):
    # Setando a variavel follow
    follow = set()
    
    # Atribuindo os intens de regra_dict em regras
    reg = regras_dict.items()

    # Se o Símbolo Inicial for igual a um não terminal ele une follow com epsilon
    if nT == simbolo_inicio:
        follow = follow | {'$'}
    
    # Loop para os itens do dicionario regras
    for nt,rhs in reg:
        # Loop para os para cada item em rhs
        for alt in rhs:
            # Loop dos caracteres em alt
            for char in alt:
                # Se o char for igual a nT atribui alt no index+1 a str_follow e então pega o proximo
                if char == nT:
                    str_follow = alt[alt.index(char) + 1:]
                    # Se str_follow for ifual a vazio ele testa se o nt for não terminal caso sim ele continua 
                    # senão ele atribui uma união de follow com follow(nt)
                    if str_follow == '':
                        if nt == nT:
                            continue
                        else:
                            follow = follow | follow_calc(nt)
                    # Senão str_follow não for vazio ele calcula o primeiro de str_follow e coloca em follow2
                    else:
                        follow2 = first_calc(str_follow)
                        # Se tiver epsilon em follow2 ume follow com follow2 menos epsilon
                        # Depois une isso com follow(nt)
                        if 'ε' in follow2:
                            follow = follow | follow2 - {'ε'}
                            follow = follow | follow_calc(nt)
                        # Senão ele une follow com follow 2
                        else:
                            follow = follow | follow2
    # Depois de tudo ele retorna follow
    return follow

# Criação da tabela a partir do FIRST e FOLLOW achados da gramatica
def criaTabela(tabela):

    table = {}
    
    for key in tr:
        for valor in tr[key]:
            if not ('ε' in valor) and not ('$' in valor):
                for element in FIRST[key]:
                    if element == 'ε':
                        pass
                    else:
                        table[key, element] = valor
            if 'ε' in FIRST[key]:
                for element in FOLLOW[key]:
                    # print(element)
                    table[key, element] = valor
            if ('ε' in FIRST[key]) and ('$' in FOLLOW[key]):
                table[key, '$'] = valor

    tabela = table
    return tabela

def criaTabela2(tabela):

    table = {}
    
    for key in tr2:
        for valor in tr2[key]:
            if not ('ε' in valor) and not ('$' in valor):
                for element in FIRST[key]:
                    if element == 'ε':
                        pass
                    else:
                        table[key, element] = valor
            if 'ε' in FIRST[key]:
                for element in FOLLOW[key]:
                    # print(element)
                    table[key, element] = valor
            if ('ε' in FIRST[key]) and ('$' in FOLLOW[key]):
                table[key, '$'] = valor

    tabela = table
    return tabela

# Print da Tabela
def printaTable(tabela):
    nova_tabela = {}
    for tupla in tabela:
        nova_tabela[tupla[1]] = {}

    for tupla in tabela:
        nova_tabela[tupla[1]][tupla[0]] = tabela[tupla]

    print(pd.DataFrame(nova_tabela).fillna('ERROR'))



while not end:
    clear()

    print(CYAN+'-'*115)
    print('Aqui será feita a função para calcular o conjunto first: \n\"O valor de epsilon é dado pelo caractere ε\"')
    print('Lembre-se Insira apenas símbolos maiúsculos para os não terminais e não insira simbolos maiúsculos nos terminais')
    print('Siga os passos mandados no programa para fazer o cálculo do conjunto first'+END)
    print('')

    # Declarando a lista de simbolos terminais
    terminal = []
    num_terminal = int(input(BLUE+'Digite o número de símbolos terminais: '+END))
    # terminal = ['+', '*', 'a', '(', ')']
    # num_terminal = 5
    for i in range(num_terminal):
        x = i + 1
        terminal.append(input(RED+f'Digite o {x}º terminal: '+END))

    # Declarando a lista de simbolos não terminais
    n_terminal = []
    num_n_terminal = int(input(BLUE+'Digite a quantidade de simbolos não terminais: '+END))
    # n_terminal = ['E', 'B', 'T', 'Y', 'F']
    # num_n_terminal = 5
    for i in range(num_n_terminal):
        x = i + 1
        n_terminal.append(input(RED+f'Digite o {x}º não terminal: '+END))

    # Verificando se os símbolos são aceitos
    terminais = ''
    n_terminais = ''
    conta_simbolo_n_terminal = 0

    for i in range(len(terminal)):
        terminais = terminais + terminal[i]
    for i in range(len(n_terminal)):
        n_terminais = n_terminais + n_terminal[i]
        if(re.search(r'[A-Z]', n_terminal[i])):
            conta_simbolo_n_terminal += 1
            if (re.search(r'[A-Z]\'', n_terminal[i])):
                conta_simbolo_n_terminal += 1

    # Exceções caso tenha sìmbolos errados
    if (re.search(r'[A-Z]', terminais)):
        raise Exception(RED+'Existem símbolos maiúsculos nos terminais\n--------------------------------------------------------------'+END)
    if (conta_simbolo_n_terminal != len(n_terminais)):
        raise Exception(RED+'Existem símbolos não aceitos nos não terminais\n--------------------------------------------------------------'+END)

    # Delcarando o simbolo que dá inicio a lista de Regras
    simbolo_inicio = input(BLUE+'Digite qual será o símbolo inicial: '+END)
    # simbolo_inicio = 'E'
    # Declarando a quantidade e as Regras
    # Regras são declaradas normalmente do seguinte jeito:
    # S->AB|ε
    num_regras = int(input(BLUE+'Digite o número de regras: '+END))
    regras = []
    # num_regras = 5  
    clear()
    print(GREEN+'-'*115+END)

    print(BLUE+'Digite as regras da linguagem: ')
    for i in range(num_regras):
        regras.append(input())
    print(END)

    # regras = ['E->TB','B->+TB|ε','T->FY','Y->*FY|ε','F->a|(E)']
    regras_dict = {}

    # Variáveis utilizadas pela tabela
    alter_indices = []
    div_regra = []
    tr = dict()
    
    tr2 = dict()
    div_regra2 = []
    alter_indices2 = []

    for nT in n_terminal:
        regras_dict[nT] = []
    
    # Verificando se a regra possui '->' ou '|'
    for regra in regras:
        n_term_regra = regra.split('->')
        alters = n_term_regra[1].split('|')
        for alter in alters:
            e = n_term_regra[0] + '->' + alter
            # print(e)
            div_regra.append(e)
            alter_indices.append(e)
            regras_dict[n_term_regra[0]].append(alter)
    
    for i in range(len(div_regra)):
        div_regra[i] = div_regra[i].split('->')
    
    # print(div_regra)
    for i in div_regra:
        tr[i[0]] = []
        tr2[i[0]] = []
    # print(tr)

    for key in tr:
        for reg in alter_indices:
            if key == reg[0]:
                tr[key].append(reg)
    for key in tr2:
        for reg in div_regra:
            if key == reg[0]:
                tr2[key].append(reg[1])

    
    print(tr2)

    # Declarando a variável que irá conter os símbolos do conjunto First e Follow
    FIRST = {}
    FOLLOW = {}

    # Inicializando a variável FIRST e FOLLOW com o número de indices que ela terá
    for n_term in n_terminal:
        FIRST[n_term] = set()

    for term in terminal:
        FIRST[term] = term
    
    for n_term in n_terminal:
        FOLLOW[n_term] = set()

    # Colocando os indices na variável FIRST por meio da chamada da função first_calc()
    for n_term in n_terminal:
        FIRST[n_term] = FIRST[n_term] | first_calc(n_term)
    
    # Colocando $ ao FOLLOW do sìmbolo inicial
    FOLLOW[simbolo_inicio] = FOLLOW[simbolo_inicio] | {'$'}
    # Colocando os índices na variável FOLLOW com a função follow_calc()
    for n_term in n_terminal:
        FOLLOW[n_term] = FOLLOW[n_term] | follow_calc(n_term)

    print(GREEN)
    print('-'*115)
    print('')

    # print(FIRST)
    # print(FOLLOW)

    # Print dos tipos de colunas
    print('{: ^25}|{: ^25}|{: ^25}'.format('Não Terminais', 'Primeiro', 'Próximo'))
    # Print dos Terminais e não Terminais junto com os FIRST e FOLLOW
    for n_term in n_terminal:
        print('{: ^25}|{: ^25}|{: ^25}'.format(n_term, str(FIRST[n_term]), str(FOLLOW[n_term])))
            

    print('')
    print('-'*115+END)

    for chave, valor in FIRST.items():
        FIRST[chave] = list(valor)

    for chave, valor in FOLLOW.items():
        FOLLOW[chave] = list(valor)

    # print(FIRST)

    # Criação do dicionário da tabela
    TABELA = {}
    TABELA2 = {}

    # Criação da tabela pela função criaTabela()
    TABELA = criaTabela(TABELA)
    TABELA2 = criaTabela2(TABELA2)

    # print(TABELA)
    print('')
    printaTable(TABELA2)
    print('')

    # Condição de Parada do Loop Inicial
    q = input(RED+'Se quiser fazer mais uma análise digite 1 senão digite 2, e aperte enter, ou apenas Aperte Enter: '+END)

    if q == '1':
        end = False
        clear()
    elif q == '2' or q == '':
        end = True
    else:
        print(RED+'Digito Invalido!!'+END)
        quit()
