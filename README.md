# Sistema de Recuperação de Informação

Sistema desenvolvido para a disciplina de Recuperação de Informação, implementando técnicas clássicas de indexação e busca de documentos.

**Aluna:** Luisa Caetano Araujo
**Matrícula:** 0076937

## Funcionalidades

O sistema oferece as seguintes operações através de um menu interativo:

1. **Indexação da Coleção** - Processa todos os documentos `.txt` na pasta `documentos/`
2. **Vocabulário** - Exibe os 50 termos mais frequentes da coleção
3. **Matriz de Ocorrências** - Mostra presença/ausência de cada termo nos documentos
4. **Matriz de Frequências** - Mostra a frequência de cada termo nos documentos
5. **Índice Invertido de Ocorrências** - Lista quais documentos contêm cada termo
6. **Índice Invertido de Frequências** - Lista documentos e quantidade de ocorrências por termo
7. **Busca Booleana** - Permite consultas usando operadores AND, OR e NOT
8. **Matriz de Pesos TF-IDF** - Calcula e exibe os pesos TF-IDF dos termos
9. **Consulta com Similaridade** - Busca por dois termos e calcula similaridade com documentos

## Conceitos Implementados

### Pré-processamento
- Remoção de stopwords (português e inglês)
- Remoção de pontuação e números
- Conversão para minúsculas
- Filtragem de palavras curtas (< 3 caracteres)

### Estruturas de Dados
- **Vocabulário**: Top 50 termos mais frequentes
- **Matriz Termo-Documento**: Representação matricial da coleção
- **Índice Invertido**: Estrutura otimizada para buscas

### Modelo Vetorial
- **TF (Term Frequency)**: `1 + log₁₀(fᵢⱼ)`
- **IDF (Inverse Document Frequency)**: `log₁₀(N/nᵢ)`
- **TF-IDF**: Peso combinado para ranking de relevância

### Similaridade
- Cálculo de similaridade pelo cosseno entre vetores de documentos e consultas

## Como Usar

### Requisitos
- Python 3.x

### Execução

```bash
cd RecInformcacao
python sistema_recuperacaoInformacao.py
```

### Adicionando Documentos

Coloque arquivos `.txt` na pasta `documentos/` antes de executar a indexação.

## Estrutura do Projeto

```
RecInformcacao/
├── sistema_recuperacaoInformacao.py   # Script principal
├── documentos/                         # Coleção de documentos .txt
│   ├── doc191.txt
│   ├── doc192.txt
│   └── ...
├── vocabulario.json                    # Vocabulário gerado
├── matriz_ocorrencias.json             # Matriz de ocorrências
├── matriz_frequencias.json             # Matriz de frequências
├── matriz_pesos.json                   # Matriz TF-IDF
├── indice_invertido_ocorrencias.json   # Índice invertido (ocorrências)
└── indice_invertido_frequencias.json   # Índice invertido (frequências)
```

## Exemplos de Busca Booleana

```
# Busca simples
computação

# Busca com AND
quantum AND computing

# Busca com OR
algorithm OR optimization

# Busca com NOT
quantum AND NOT classical
```

## Coleção de Documentos

A coleção inclui artigos acadêmicos sobre:
- Computação Quântica
- Complexidade Computacional
- Classes P, NP e BQP
- Algoritmos de Shor e Grover
- Paradigmas Híbridos (Clássico-Quântico)
