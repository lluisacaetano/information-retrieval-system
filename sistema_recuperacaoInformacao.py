import os
import re
import time
import json
import math
from collections import Counter

def imprimir_cabecalho(titulo="TRABALHO DE RECUPERAÇÃO DE INFORMAÇÃO"):
    """Imprime o cabeçalho da interface."""

    linha = "*" * 76

    print("\n"+linha)
    print(f"************** {titulo} {'*' * (60 - len(titulo))}")
    print(f"******* ALUNO: LUISA CAETANO ARAUJO - MATRÍCULA: 0076937 {'*' * 19}")
    print(linha)
    print(linha)

def imprimir_menu():
    """Imprime as opções do menu."""

    print(f"*************** {'MENU'} {'*' * 55}")
    print(f"*********** 1 - PARA INDEXAR A COLEÇÃO {'*' * 37}")
    print(f"*********** 2 - PARA IMPRIMIR O VOCABULÁRIO {'*' * 32}")
    print(f"*********** 3 - PARA IMPRIMIR A MATRIZ DE OCORRÊNCIAS {'*' * 22}")
    print(f"*********** 4 - PARA IMPRIMIR A MATRIZ DE FREQUENCIAS {'*' * 22}")
    print(f"*********** 5 - PARA IMPRIMIR O ÍNDICE INVERTIDO DE OCORRÊNCIAS {'*' * 12}")
    print(f"*********** 6 - PARA IMPRIMIR O ÍNDICE INVERTIDO DE FREQUÊNCIAS {'*' * 12}")
    print(f"*********** 7 - PARA REALIZAR BUSCA BOOLEANA {'*' * 31}")
    print(f"*********** 8 - PARA IMPRIMIR A MATRIZ DE PESOS TF-IDF {'*' * 21}")
    print(f"*********** 9 - REALIZAR CONSULTA E CALCULAR SIMILARIDADES {'*' * 17}")
    print(f"*********** 0 - SAIR {'*' * 55}")
    print("\nDIGITE A OPÇÃO DESEJADA: ", end="")

def carregar_documentos():
    """Carrega os documentos da coleção."""

    try:
        # Verifica se existe o a pasta documentos, e se existir, carrega todos os arquivos .txt dentro dela como documentos para processamento
        if not os.path.exists("documentos"):
            os.makedirs("documentos")  # Cria o diretório se não existir
            print("Diretório de documentos criado. Por favor, adicione documentos para indexar.")
            return []

        arquivos = [f for f in os.listdir("documentos") if f.endswith('.txt')]
        documentos = []

        for arquivo in arquivos:
            with open(os.path.join("documentos", arquivo), 'r', encoding='utf-8') as f:
                texto = f.read()
                documentos.append({
                    'nome': arquivo,  
                    'texto': texto   
                })

        return documentos
    except Exception as e:
        print(f"Erro ao carregar documentos: {e}")
        return []

def remover_stopwords(texto):
    """Remove stopwords em português e inglês do texto."""

    stopwords = [
        # Português
        "a", "à", "ao", "aos", "aquela", "aquelas", "aquele", "aqueles", "aquilo", "as", "às", "até", "com", "como",
        "da", "das", "de", "dela", "delas", "dele", "deles", "depois", "do", "dos", "e", "é", "ela", "elas", "ele",
        "eles", "em", "entre", "era", "eram", "éramos", "essa", "essas", "esse", "esses", "esta", "estas", "este",
        "estes", "eu", "foi", "fomos", "for", "foram", "forem", "formos", "fosse", "fossem", "fôssemos", "há", "isso",
        "isto", "já", "lhe", "lhes", "mais", "mas", "me", "mesmo", "meu", "meus", "minha", "minhas", "muito", "muitos",
        "na", "não", "nas", "nem", "no", "nos", "nós", "nossa", "nossas", "nosso", "nossos", "num", "numa", "o", "os",
        "ou", "para", "pela", "pelas", "pelo", "pelos", "por", "qual", "quando", "que", "quem", "são", "se", "seja",
        "sejam", "sejamos", "sem", "será", "serão", "serei", "seremos", "seria", "seriam", "seríamos", "seu", "seus",
        "só", "somos", "sou", "sua", "suas", "também", "te", "tem", "tém", "têm", "temos", "tenha", "tenham", "tenhamos",
        "tenho", "terá", "terão", "terei", "teremos", "teria", "teriam", "teríamos", "teu", "teus", "teve", "tinha",
        "tinham", "tínhamos", "tive", "tivemos", "tiver", "tiveram", "tiverem", "tivermos", "tu", "tua", "tuas", "um",
        "uma", "você", "vocês", "vos", "ser", "está",
        # Inglês
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
        "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot",
        "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each",
        "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd",
        "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
        "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me",
        "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
        "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll",
        "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs",
        "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
        "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd",
        "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
        "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
        "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "can", "also", "use", "pages"
    ]

    # Adiciona letras isoladas como stopwords
    stopwords += list("abcdefghijklmnopqrstuvwxyz")

    texto = re.sub(r'[^\w\s]', ' ', texto.lower())  #Remove pontuação e converte para minúsculas
    texto = re.sub(r'\d+', ' ', texto)  # Remove números

    palavras = texto.split()

    # Filtra removendo stopwords e palavras muito curtas (menos de 3 caracteres)
    palavras_filtradas = [p for p in palavras if p not in stopwords and len(p) > 2]

    return palavras_filtradas

def construir_vocabulario(documentos, top_n=50): 
    """Constrói o vocabulário limitado aos 50 termos mais frequentes na coleção."""

    todas_palavras = []

    for doc in documentos:
        palavras = remover_stopwords(doc['texto'])
        todas_palavras.extend(palavras)

    contador = Counter(todas_palavras)

    # Seleciona os 50 termos mais frequentes para formar o vocabulário
    vocabulario = [palavra for palavra, _ in contador.most_common(top_n)]

    return vocabulario

def criar_matriz_ocorrencias(documentos, vocabulario):
    """Cria matriz de ocorrências (presença/ausência do termo no documento)."""

    matriz = []

    for termo in vocabulario:
        linha = []
        for doc in documentos:
            palavras = remover_stopwords(doc['texto'])
            # 1 se o termo estiver presente, 0 caso contrário
            linha.append(1 if termo in palavras else 0)
        matriz.append(linha)

    return matriz

def criar_matriz_frequencias(documentos, vocabulario):
    """Cria matriz de frequências (frequência do termo no documento)."""

    matriz = []

    for termo in vocabulario:
        linha = []
        for doc in documentos:
            palavras = remover_stopwords(doc['texto'])
            linha.append(palavras.count(termo))
        matriz.append(linha)

    return matriz

def salvar_vocabulario(vocabulario):
    """Salva o vocabulário em um arquivo."""

    with open('vocabulario.json', 'w', encoding='utf-8') as f:
        json.dump(vocabulario, f, ensure_ascii=False, indent=4)
    print("Vocabulário salvo com sucesso!")

def salvar_matriz(matriz, nome_arquivo):
    """Salva a matriz em um arquivo."""

    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(matriz, f, ensure_ascii=False, indent=4)
    print(f"Matriz salva com sucesso em {nome_arquivo}!")

def carregar_vocabulario():
    """Carrega o vocabulário do arquivo."""

    try:
        with open('vocabulario.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Arquivo de vocabulário não encontrado.")
        return []

def carregar_matriz(nome_arquivo):
    """Carrega uma matriz do arquivo."""

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return []

def indexar_colecao():
    """Função para indexar a coleção."""

    imprimir_cabecalho()
    print("\nIndexando a coleção...\n")

    documentos = carregar_documentos()

    if not documentos:
        print("Nenhum documento encontrado para indexar!")
        input("\nPressione ENTER para voltar ao menu principal...")
        return

    print(f"Encontrados {len(documentos)} documentos.")

    print("Construindo vocabulário...")
    vocabulario = construir_vocabulario(documentos)

    print("Criando matriz de ocorrências...")
    matriz_ocorrencias = criar_matriz_ocorrencias(documentos, vocabulario)

    print("Criando matriz de frequências...")
    matriz_frequencias = criar_matriz_frequencias(documentos, vocabulario)

    print("Criando índice invertido de ocorrências...")
    indice_ocorrencias = criar_indice_invertido_ocorrencias(documentos, vocabulario)

    print("Criando índice invertido de frequências...")
    indice_frequencias = criar_indice_invertido_frequencias(documentos, vocabulario)

    print("Calculando matriz de pesos TF-IDF...")
    matriz_pesos = calcular_tf_idf(documentos, vocabulario, matriz_frequencias)

    salvar_vocabulario(vocabulario)
    salvar_matriz(matriz_ocorrencias, 'matriz_ocorrencias.json')
    salvar_matriz(matriz_frequencias, 'matriz_frequencias.json')
    salvar_indice_invertido(indice_ocorrencias, 'indice_invertido_ocorrencias.json')
    salvar_indice_invertido(indice_frequencias, 'indice_invertido_frequencias.json')
    salvar_matriz(matriz_pesos, 'matriz_pesos.json')

    print("\nIndexação concluída com sucesso!")
    input("\nPressione ENTER para voltar ao menu principal...")

def imprimir_vocabulario():
    """Função para imprimir o vocabulário."""

    imprimir_cabecalho()
    print("\nImprimindo o vocabulário...\n")

    vocabulario = carregar_vocabulario()

    if not vocabulario:
        print("Vocabulário não encontrado. Execute a indexação primeiro.")
        input("\nPressione ENTER para voltar ao menu principal...")
        return

    print("\nVOCABULÁRIO:")
    for idx, palavra in enumerate(vocabulario, 1):
        print(f"{idx}. {palavra}")

    input("\nPressione ENTER para voltar ao menu principal...")

def imprimir_matriz_ocorrencias():
    """Função para imprimir a matriz de ocorrências em formato tabular"""

    imprimir_cabecalho()
    print("\nImprimindo a matriz de ocorrências...\n")

    vocabulario = carregar_vocabulario()
    matriz = carregar_matriz('matriz_ocorrencias.json')

    if not vocabulario or not matriz:
        print("Dados não encontrados. Execute a indexação primeiro.")
        input("\nPressione ENTER para voltar ao menu principal...")
        return

    documentos = carregar_documentos()
    nomes_docs = [doc['nome'] for doc in documentos]

    print("\nMATRIZ DE OCORRÊNCIAS:")
    print("           ", end="  | ")
    for doc in nomes_docs:
        nome_curto = doc[:6] 
        print(f"{nome_curto:>6}", end=" | ")
    print()

    for i, termo in enumerate(vocabulario):
        print(f"{termo[:12]:>12}", end=" | ")
        for j in range(len(nomes_docs)):
            print(f"{matriz[i][j]:>6}", end=" | ")
        print()

    input("\nPressione ENTER para voltar ao menu principal...")

def imprimir_matriz_frequencias():
    """Função para imprimir a matriz de frequências em formato tabular."""

    imprimir_cabecalho()
    print("\nImprimindo a matriz de frequências...\n")

    vocabulario = carregar_vocabulario()
    matriz = carregar_matriz('matriz_frequencias.json')

    if not vocabulario or not matriz:
        print("Dados não encontrados. Execute a indexação primeiro.")
        input("\nPressione ENTER para voltar ao menu principal...")
        return

    documentos = carregar_documentos()
    nomes_docs = [doc['nome'] for doc in documentos]

    print("\nMATRIZ DE FREQUÊNCIAS:")
    print("           ", end="  | ")
    for doc in nomes_docs:
        nome_curto = doc[:6] 
        print(f"{nome_curto:>6}", end=" | ")
    print()

    for i, termo in enumerate(vocabulario):
        print(f"{termo[:12]:>12}", end=" | ")
        for j in range(len(nomes_docs)):
            print(f"{matriz[i][j]:>6}", end=" | ")
        print()

    input("\nPressione ENTER para voltar ao menu principal...")

def criar_indice_invertido_ocorrencias(documentos, vocabulario):
    """Cria índice invertido indicando presença/ausência do termo nos documentos."""
    
    indice = {}
    
    for termo in vocabulario:
        docs_com_termo = []
        for i, doc in enumerate(documentos):
            palavras = remover_stopwords(doc['texto'])
            if termo in palavras:
                docs_com_termo.append(doc['nome'])
        indice[termo] = docs_com_termo
    
    return indice

def criar_indice_invertido_frequencias(documentos, vocabulario):
    """Cria índice invertido com frequência do termo nos documentos."""
    
    indice = {}
    
    for termo in vocabulario:
        freq_docs = {}
        for doc in documentos:
            palavras = remover_stopwords(doc['texto'])
            freq = palavras.count(termo)
            if freq > 0:
                freq_docs[doc['nome']] = freq
        indice[termo] = freq_docs
    
    return indice

def salvar_indice_invertido(indice, nome_arquivo):
    """Salva o índice invertido em um arquivo."""
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(indice, f, ensure_ascii=False, indent=4)
    print(f"Índice invertido salvo com sucesso em {nome_arquivo}!")

def imprimir_indice_invertido_ocorrencias():
    """Função para imprimir o índice invertido de ocorrências."""
    
    imprimir_cabecalho()
    print("\nImprimindo o índice invertido de ocorrências...\n")

    try:
        with open('indice_invertido_ocorrencias.json', 'r', encoding='utf-8') as f:
            indice = json.load(f)
            
        print("\nÍNDICE INVERTIDO DE OCORRÊNCIAS:")
        for termo, documentos in indice.items():
            print(f"\n{termo}: ")
            print(f"  Aparece em {len(documentos)} documento(s):")
            for doc in documentos:
                print(f"    - {doc}")
                
    except FileNotFoundError:
        print("Índice não encontrado. Execute a indexação primeiro.")
    
    input("\nPressione ENTER para voltar ao menu principal...")

def imprimir_indice_invertido_frequencias():
    """Função para imprimir o índice invertido de frequências."""
    
    imprimir_cabecalho()
    print("\nImprimindo o índice invertido de frequências...\n")

    try:
        with open('indice_invertido_frequencias.json', 'r', encoding='utf-8') as f:
            indice = json.load(f)
            
        print("\nÍNDICE INVERTIDO DE FREQUÊNCIAS:")
        for termo, documentos in indice.items():
            print(f"\n{termo}:")
            print(f"  Aparece em {len(documentos)} documento(s):")
            for doc, freq in documentos.items():
                print(f"    - {doc}: {freq} vez(es)")
                
    except FileNotFoundError:
        print("Índice não encontrado. Execute a indexação primeiro.")
    
    input("\nPressione ENTER para voltar ao menu principal...")

def realizar_busca_booleana():
    """Função para realizar busca booleana."""
    
    imprimir_cabecalho()
    print("\nBUSCA BOOLEANA")
    print("\nOperadores disponíveis: AND, OR, NOT")
    print("Exemplos válidos:")
    print("  - termo1 AND termo2")
    print("  - termo1 OR termo2")
    print("  - termo1 AND NOT termo2")
    print("  - termo1 OR NOT termo2")
    
    # Carrega o índice invertido de ocorrências
    try:
        with open('indice_invertido_ocorrencias.json', 'r', encoding='utf-8') as f:
            indice = json.load(f)
    except FileNotFoundError:
        print("\nÍndice não encontrado. Execute a indexação primeiro.")
        input("\nPressione ENTER para voltar ao menu principal...")
        return
    
    todos_documentos = set()
    for docs in indice.values():
        todos_documentos.update(docs)
    
    while True:
        print("\nDigite sua consulta (ou 'SAIR' para voltar ao menu):")
        consulta = input().strip().upper()
        
        if consulta == 'SAIR':
            break
            
        termos = consulta.split()
        
        # Verifica se a consulta é válida
        if len(termos) not in [1, 3, 4]:
            print("\nFormato de consulta inválido!")
            continue
            
        # Busca simples com um termo
        if len(termos) == 1:
            termo = termos[0].lower()
            if termo not in indice:
                print(f"\nTermo '{termo}' não encontrado no vocabulário.")
                continue
            resultado = set(indice[termo])
            
        # Busca com operador AND ou OR
        elif len(termos) == 3:
            termo1, operador, termo2 = termos[0].lower(), termos[1], termos[2].lower()
            
            if termo1 not in indice or termo2 not in indice:
                print("\nUm ou mais termos não encontrados no vocabulário.")
                continue
                
            conjunto1 = set(indice[termo1])
            conjunto2 = set(indice[termo2])
            
            if operador == 'AND':
                resultado = conjunto1.intersection(conjunto2)
            elif operador == 'OR':
                resultado = conjunto1.union(conjunto2)
            else:
                print("\nOperador inválido! Use AND ou OR.")
                continue
                
        # Busca com NOT
        elif len(termos) == 4:
            termo1, operador1, operador2, termo2 = termos
            termo1, termo2 = termo1.lower(), termo2.lower()
            
            if operador2 != 'NOT' or operador1 not in ['AND', 'OR']:
                print("\nFormato inválido para operação com NOT!")
                continue
                
            if termo1 not in indice or termo2 not in indice:
                print("\nUm ou mais termos não encontrados no vocabulário.")
                continue
                
            conjunto1 = set(indice[termo1])
            conjunto2 = todos_documentos - set(indice[termo2])  # Complemento do conjunto2
            
            if operador1 == 'AND':
                resultado = conjunto1.intersection(conjunto2)
            else:  # OR
                resultado = conjunto1.union(conjunto2)
        
        if resultado:
            print(f"\nEncontrados {len(resultado)} documento(s):")
            for doc in sorted(resultado):
                print(f"  - {doc}")
        else:
            print("\nNenhum documento encontrado para esta consulta.")
            
    print("\nRetornando ao menu principal...")
    input("\nPressione ENTER para continuar...")

def calcular_tf_idf(documentos, vocabulario, matriz_frequencias):
    """
    Calcula os pesos TF-IDF para cada termo em cada documento.
    TF = 1 + log(fi,j) onde fi,j é a frequência do termo i no documento j
    IDF = log(N/ni) onde N é o número total de documentos e ni é o número de documentos com o termo i
    TF-IDF = TF * IDF
    """

    N = len(documentos)  # Número total de documentos
    matriz_pesos = []
    
    for i, termo in enumerate(vocabulario):
        linha_pesos = []
        
        # Calcula ni (número de documentos que contém o termo)
        ni = sum(1 for freq in matriz_frequencias[i] if freq > 0)
        
        if ni == 0:
            ni = 1
            
        for j in range(N):
            fi_j = matriz_frequencias[i][j]  # Frequência do termo i no documento j
            
            if fi_j > 0:
                # Calcula TF usando 1 + log(fi,j)
                tf = 1 + math.log10(fi_j)
                # Calcula IDF usando log(N/ni)
                idf = math.log10(N/ni)
                # Calcula o peso TF-IDF
                peso = tf * idf
            else:
                peso = 0
                
            linha_pesos.append(round(peso, 4))  
            
        matriz_pesos.append(linha_pesos)
    
    return matriz_pesos

def imprimir_matriz_pesos():
    """Função para imprimir a matriz de pesos TF-IDF."""
    
    imprimir_cabecalho()
    print("\nImprimindo a matriz de pesos TF-IDF...\n")

    vocabulario = carregar_vocabulario()
    matriz_pesos = carregar_matriz('matriz_pesos.json')
    documentos = carregar_documentos()

    if not vocabulario or not matriz_pesos or not documentos:
        print("Dados não encontrados. Execute a indexação primeiro.")
        input("\nPressione ENTER para voltar ao menu principal...")
        return

    print("\nMATRIZ DE PESOS TF-IDF:\n")
    
    print("           ", end="  | ")
    for doc in documentos:
        nome_curto = doc['nome'][:6]
        print(f"{nome_curto:>8}", end=" | ")
    print()

    for i, termo in enumerate(vocabulario):
        print(f"{termo[:12]:>12}", end=" | ")
        for peso in matriz_pesos[i]:
            print(f"{peso:>8.4f}", end=" | ")
        print()

    input("\nPressione ENTER para voltar ao menu principal...")

def calcular_similaridade(vetor_doc, vetor_consulta):
    """
    Calcula a similaridade entre o vetor do documento e o vetor de consulta.
    Fórmula: Σ(w_i,j × w_i,q) / (√Σ(w_i,j²) × √Σ(w_i,q²))
    onde w_i,j são os pesos dos termos no documento e w_i,q são os pesos na consulta
    """
    
    # Calcula o numerador (produto dos pesos)
    numerador = sum(d * q for d, q in zip(vetor_doc, vetor_consulta))
    
    # Calcula os denominadores
    soma_quadrados_doc = sum(d * d for d in vetor_doc)
    soma_quadrados_consulta = sum(q * q for q in vetor_consulta)
    
    # Calcula as raízes
    if soma_quadrados_doc == 0 or soma_quadrados_consulta == 0:
        return 0
        
    denominador = math.sqrt(soma_quadrados_doc) * math.sqrt(soma_quadrados_consulta)
    
    # Retorna a similaridade
    return numerador / denominador if denominador != 0 else 0

def realizar_consulta():
    """Recebe dois termos de consulta, mostra sua tabela TF-IDF e calcula similaridades."""
    
    imprimir_cabecalho()
    print("\nCONSULTA POR TERMOS E SIMILARIDADE\n")
    
    vocabulario = carregar_vocabulario()
    matriz_pesos = carregar_matriz('matriz_pesos.json')
    documentos = carregar_documentos()
    
    if not vocabulario or not matriz_pesos or not documentos:
        print("\nDados não encontrados. Execute a indexação primeiro.")
        input("\nPressione ENTER para voltar ao menu principal...")
        return
    
    print("Digite até dois termos para consulta.")
    print("\nDigite o primeiro termo: ", end="")
    termo1 = input().strip().lower()
    print("Digite o segundo termo: ", end="")
    termo2 = input().strip().lower()
    
    if termo1 not in vocabulario or termo2 not in vocabulario:
        print("\nUm ou mais termos não encontrados no vocabulário!")
        input("\nPressione ENTER para voltar ao menu principal...")
        return
    
    idx1 = vocabulario.index(termo1)
    idx2 = vocabulario.index(termo2)
    
    # Imprime a tabela TF-IDF apenas para os termos selecionados
    print("\nTABELA TF-IDF DOS TERMOS CONSULTADOS:\n")
    
    print("           ", end="  | ")
    for doc in documentos:
        nome_curto = doc['nome'][:6]
        print(f"{nome_curto:>8}", end=" | ")
    print()
    
    print(f"{termo1[:12]:>12}", end=" | ")
    for peso in matriz_pesos[idx1]:
        print(f"{peso:>8.4f}", end=" | ")
    print()
    
    print(f"{termo2[:12]:>12}", end=" | ")
    for peso in matriz_pesos[idx2]:
        print(f"{peso:>8.4f}", end=" | ")
    print()
    
    print("\nSIMILARIDADES COM OS DOCUMENTOS:\n")
    print("Documento                  Similaridade")
    print("-" * 45)
    
    similaridades = []
    for j in range(len(documentos)):
        # Cria vetor do documento j 
        vetor_doc = [matriz_pesos[i][j] for i in range(len(vocabulario))]
        
        # Cria vetor da consulta 
        vetor_consulta = [0] * len(vocabulario)
        vetor_consulta[idx1] = matriz_pesos[idx1][j]
        vetor_consulta[idx2] = matriz_pesos[idx2][j]
        
        # Calcula similaridade
        sim = calcular_similaridade(vetor_doc, vetor_consulta)
        similaridades.append((documentos[j]['nome'], sim))
    
    similaridades.sort(key=lambda x: x[1], reverse=True)
    for doc, sim in similaridades:
        if sim > 0:
            print(f"{doc[:25]:<25} {sim:>10.4f}")
    
    input("\nPressione ENTER para voltar ao menu principal...")

def menu_principal():
    """Exibe o menu principal e processa as opções."""

    while True:
        imprimir_cabecalho()
        imprimir_menu()

        try:
            opcao = int(input())

            if opcao == 1:
                indexar_colecao()
            elif opcao == 2:
                imprimir_vocabulario()
            elif opcao == 3:
                imprimir_matriz_ocorrencias()
            elif opcao == 4:
                imprimir_matriz_frequencias()
            elif opcao == 5:
                imprimir_indice_invertido_ocorrencias()
            elif opcao == 6:
                imprimir_indice_invertido_frequencias()
            elif opcao == 7:
                realizar_busca_booleana()
            elif opcao == 8:
                imprimir_matriz_pesos()
            elif opcao == 9:
                realizar_consulta()
            elif opcao == 0:
                print("Saindo do sistema...")
                break
            else:
                print("\nOpção inválida! Tente novamente.")
                time.sleep(1.5)
        except ValueError:
            print("\nEntrada inválida! Digite um número.")
            time.sleep(1.5)

def verificar_pasta_documentos():
    """Verifica se a pasta de documentos existe, se não, cria e adiciona instruções."""

    if not os.path.exists("documentos"):
        os.makedirs("documentos")
        with open("documentos/LEIA-ME.txt", 'w', encoding='utf-8') as f:
            f.write("Adicione seus arquivos de texto (.txt) nesta pasta para indexação.\n")
            f.write("Cada arquivo será tratado como um documento separado na coleção.\n")

if __name__ == "__main__":
    verificar_pasta_documentos()
    menu_principal()