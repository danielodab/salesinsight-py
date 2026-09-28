# SalesInsight PY

## Sobre o projeto

Analise de dados de vendas feita em Python. O script carrega um arquivo CSV,
limpa os registros com problema, cria colunas novas, calcula metricas por mes,
produto, categoria e regiao, separa os clientes em Bronze/Prata/Ouro e salva
os resultados em CSV e JSON.

## O que o projeto analisa

- Receita, quantidade e numero de vendas por mes
- Top 5 produtos e receita por categoria
- Receita e ticket medio por regiao
- Segmentacao de clientes por nivel de gasto (Bronze, Prata, Ouro)
- Quantas vendas ficaram acima da media geral

## Conceitos aplicados (Modulo 01 - Semanas 01 a 05)

- Variaveis, tipos, operadores e condicionais if/elif/else
- Lacos for
- Listas, dicionarios e estruturas compostas
- Funcoes com parametros, retorno e docstring
- Funcoes lambda (classificacao de clientes, ordenacao e processar_coluna)
- Funcao que recebe outra funcao como argumento (processar_coluna)
- Leitura e escrita de CSV e JSON
- Modulo datetime (validar data, extrair mes e ano)
- Expressoes regulares com re.sub() e re.compile()
- Git e GitHub com branches e commits

## Como executar

Nao precisa instalar nada alem do Python 3.10+.

### Localmente (VS Code ou terminal)

```
python salesinsight.py
```

### Google Colab

1. Faca upload do salesinsight.py
2. Execute: `!python salesinsight.py`

O arquivo vendas.csv e gerado automaticamente na primeira execucao,
com alguns dados "sujos" de proposito (valores vazios, datas invalidas,
espacos extras e nomes de cliente errados) para a etapa de limpeza.

## Estrutura do projeto

```
salesinsight-py/
|-- salesinsight.py
|-- vendas.csv
|-- README.md
|-- outputs/
|   |-- metricas_por_mes.csv
|   |-- segmentacao_clientes.csv
|   |-- estatisticas_gerais.json
|-- planejamento/
    |-- tarefas-kanban.md
```

## Decisoes tecnicas

Escolhi remover os registros invalidos em vez de manter. Uma venda sem
quantidade ou sem preco nao tem como gerar receita, e uma venda com data
invalida nao entra em nenhum mes. Como ainda nao vimos imputacao de valores,
remover e a opcao mais segura. O relatorio de limpeza mostra quantos
registros sairam e por qual motivo.

Para o nome do cliente, uso re.sub() para tirar os caracteres estranhos e
depois monto de novo o formato Cliente_NNN a partir do numero. Assim
"CLIENTE-016", "cliente#016" e "Cliente_016!!" viram o mesmo cliente,
senao a segmentacao contaria a mesma pessoa mais de uma vez.

## O que pode melhorar

- Aceitar mais de um formato de data
- Separar o codigo em mais de um arquivo
- Deixar a saida no console mais organizada, em formato de tabela

## Ferramentas utilizadas

- Python 3.10+
- VS Code
- Bibliotecas padrao: csv, json, re, datetime, os, random
- Git / GitHub
- GitHub Projects (Kanban)

## Video de demonstracao

