import csv
import json
import os
import random
import re
from datetime import datetime, timedelta


def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """Gera um dataset sintetico de vendas com dados sujos e grava em CSV."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor",
                "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares",
                  "Tablet": "Celulares", "Monitor": "Computadores",
                  "Teclado": "Perifericos", "Mouse": "Perifericos",
                  "Headset": "Perifericos"}
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
              "Monitor": 1200, "Teclado": 250, "Mouse": 120,
              "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    colunas = ["id_venda", "data_venda", "cliente", "produto",
               "categoria", "regiao", "quantidade", "preco_unitario"]

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()

        for i in range(n_registros):
            produto = random.choice(produtos)
            categoria = categorias[produto]
            quantidade = random.randint(1, 10)
            preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
            data = data_inicio + timedelta(days=random.randint(0, 364))
            data_txt = data.strftime("%Y-%m-%d")
            cliente = f"Cliente_{random.randint(1, 50):03d}"

            # sujeira proposital para a etapa de limpeza
            if random.random() < 0.05:
                quantidade = ""
            if random.random() < 0.04:
                preco = ""
            if random.random() < 0.06:
                produto = " " + produto + " "
            if random.random() < 0.03:
                data_txt = "DATA INVALIDA"
            if random.random() < 0.10:
                cliente = random.choice([
                    cliente.upper().replace("_", "-"),
                    cliente + "!!",
                    " " + cliente,
                    cliente.replace("Cliente_", "cliente#"),
                ])

            escritor.writerow({
                "id_venda": i + 1,
                "data_venda": data_txt,
                "cliente": cliente,
                "produto": produto,
                "categoria": categoria,
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco,
            })

    print(f"Dataset gerado com {n_registros} registros em {caminho_csv}.")


def carregar_dataset(caminho_csv):
    """Le o CSV e retorna uma lista de dicionarios (um por registro)."""
    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        registros = list(leitor)
    return registros


def inspecionar_dados(registros):
    """Exibe as informacoes estruturais da lista de registros."""
    total = len(registros)
    colunas = list(registros[0].keys())

    nulos = {}
    for coluna in colunas:
        nulos[coluna] = 0

    for linha in registros:
        for coluna in colunas:
            if linha[coluna].strip() == "":
                nulos[coluna] += 1

    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Total de registros: {total}")
    print(f"Total de colunas: {len(colunas)}")
    print(f"\nColunas: {colunas}")
    print(f"\nValores ausentes por coluna:\n{nulos}")
    print("\nPrimeiros registros:")
    for linha in registros[:5]:
        print(linha)
    return registros


def limpar_dados(registros):
    """
    Limpa e trata a lista de registros de vendas.
    Retorna (registros_limpos, relatorio), onde relatorio e um dicionario
    com as contagens de registros iniciais, removidos e finais.
    """
    relatorio = {"iniciais": len(registros), "removidos_data": 0,
                 "removidos_nulos": 0, "fora_do_padrao": 0, "finais": 0}
    padrao_cliente = re.compile(r"^Cliente_\d{3}$")
    limpos = []

    for linha in registros:
        # tira espacos extras dos campos de texto
        linha["cliente"] = linha["cliente"].strip()
        linha["produto"] = linha["produto"].strip()
        linha["categoria"] = linha["categoria"].strip()
        linha["regiao"] = linha["regiao"].strip()

        # data invalida -> descarta o registro
        try:
            linha["data_venda"] = datetime.strptime(linha["data_venda"], "%Y-%m-%d")
        except ValueError:
            relatorio["removidos_data"] += 1
            continue

        # quantidade ou preco vazio -> descarta o registro
        if linha["quantidade"] == "" or linha["preco_unitario"] == "":
            relatorio["removidos_nulos"] += 1
            continue

        linha["quantidade"] = int(linha["quantidade"])
        linha["preco_unitario"] = float(linha["preco_unitario"])

        # limpa o nome do cliente com regex
        nome_limpo = re.sub(r"[^A-Za-z0-9_]", "", linha["cliente"])
        if padrao_cliente.match(nome_limpo):
            linha["cliente_fora_do_padrao"] = False
        else:
            linha["cliente_fora_do_padrao"] = True
            relatorio["fora_do_padrao"] += 1
            # pega so os numeros e monta de novo no formato Cliente_NNN
            numero = re.sub(r"\D", "", nome_limpo)
            nome_limpo = "Cliente_" + numero
        linha["cliente"] = nome_limpo

        limpos.append(linha)

    relatorio["finais"] = len(limpos)
    print("\n=== RELATORIO DE LIMPEZA ===")
    print(f"Registros iniciais: {relatorio['iniciais']}")
    print(f"Removidos por data invalida: {relatorio['removidos_data']}")
    print(f"Removidos por valor ausente: {relatorio['removidos_nulos']}")
    print(f"Clientes fora do padrao (corrigidos): {relatorio['fora_do_padrao']}")
    print(f"Registros finais: {relatorio['finais']}")
    return limpos, relatorio


def criar_colunas_derivadas(registros):
    """Cria receita_total, mes, mes_nome, trimestre, ano e faixa_receita_item."""
    meses = {1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril",
             5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
             9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}

    for linha in registros:
        receita = linha["quantidade"] * linha["preco_unitario"]
        mes = linha["data_venda"].month

        if mes <= 3:
            trimestre = "Q1"
        elif mes <= 6:
            trimestre = "Q2"
        elif mes <= 9:
            trimestre = "Q3"
        else:
            trimestre = "Q4"

        if receita < 500:
            faixa = "Baixo Valor"
        elif receita < 5000:
            faixa = "Medio Valor"
        else:
            faixa = "Alto Valor"

        linha["receita_total"] = round(receita, 2)
        linha["mes"] = mes
        linha["mes_nome"] = meses[mes]
        linha["trimestre"] = trimestre
        linha["ano"] = linha["data_venda"].year
        linha["faixa_receita_item"] = faixa

    return registros


def processar_coluna(registros, coluna, funcao_transformacao, nome_saida=None):
    """
    Aplica uma funcao de transformacao a um campo de cada registro.
    Demonstra o uso de funcoes como argumento (funcao de ordem superior).
    """
    if nome_saida is None:
        nome_saida = coluna + "_transformado"
    for linha in registros:
        linha[nome_saida] = funcao_transformacao(linha[coluna])
    return registros


def calcular_metricas(registros):
    """
    Calcula as metricas agregadas da lista de registros.
    Retorna um dicionario no formato {nome_da_metrica: lista_de_linhas}.
    """
    por_mes = {}
    por_produto = {}
    por_categoria = {}
    por_regiao = {}

    for linha in registros:
        receita = linha["receita_total"]
        mes = linha["mes"]
        produto = linha["produto"]
        categoria = linha["categoria"]
        regiao = linha["regiao"]

        if mes not in por_mes:
            por_mes[mes] = {"mes": mes, "receita_total": 0, "quantidade": 0, "n_vendas": 0}
        por_mes[mes]["receita_total"] += receita
        por_mes[mes]["quantidade"] += linha["quantidade"]
        por_mes[mes]["n_vendas"] += 1

        por_produto[produto] = por_produto.get(produto, 0) + receita
        por_categoria[categoria] = por_categoria.get(categoria, 0) + receita

        if regiao not in por_regiao:
            por_regiao[regiao] = {"regiao": regiao, "receita_total": 0, "n_vendas": 0}
        por_regiao[regiao]["receita_total"] += receita
        por_regiao[regiao]["n_vendas"] += 1

    # por mes: lista ordenada pelo numero do mes
    lista_mes = sorted(por_mes.values(), key=lambda m: m["mes"])
    for m in lista_mes:
        m["receita_total"] = round(m["receita_total"], 2)

    # top 5 produtos: ordena do maior para o menor e pega os 5 primeiros
    top_produtos = []
    for produto, receita in sorted(por_produto.items(), key=lambda x: x[1], reverse=True)[:5]:
        top_produtos.append({"produto": produto, "receita_total": round(receita, 2)})

    lista_categoria = []
    for categoria, receita in sorted(por_categoria.items(), key=lambda x: x[1], reverse=True):
        lista_categoria.append({"categoria": categoria, "receita_total": round(receita, 2)})

    lista_regiao = []
    for r in por_regiao.values():
        r["ticket_medio"] = round(r["receita_total"] / r["n_vendas"], 2)
        r["receita_total"] = round(r["receita_total"], 2)
        lista_regiao.append(r)

    metricas = {
        "por_mes": lista_mes,
        "top_produtos": top_produtos,
        "por_categoria": lista_categoria,
        "por_regiao": lista_regiao,
    }

    for nome, linhas in metricas.items():
        print(f"\n=== {nome.upper()} ===")
        for l in linhas:
            print(l)

    return metricas


def segmentar_clientes(registros):
    """
    Agrupa por cliente, soma a receita e classifica em
    Bronze / Prata / Ouro usando uma funcao lambda.
    Retorna uma lista de dicionarios: cliente, total_gasto, segmento.
    """
    classificar = lambda total: (
        "Ouro" if total > 15000 else "Prata" if total >= 5000 else "Bronze"
    )

    total_por_cliente = {}
    for linha in registros:
        nome = linha["cliente"]
        total_por_cliente[nome] = total_por_cliente.get(nome, 0) + linha["receita_total"]

    clientes = []
    for nome, total in total_por_cliente.items():
        clientes.append({
            "cliente": nome,
            "total_gasto": round(total, 2),
            "segmento": classificar(total),
        })
    clientes.sort(key=lambda c: c["total_gasto"], reverse=True)

    contagem = {"Bronze": 0, "Prata": 0, "Ouro": 0}
    for c in clientes:
        contagem[c["segmento"]] += 1

    print("\n=== TOP 10 CLIENTES ===")
    for c in clientes[:10]:
        print(c)
    print("\n=== CLIENTES POR SEGMENTO ===")
    print(contagem)

    return clientes


def calcular_estatisticas(registros):
    """Calcula estatisticas gerais, incluindo vendas acima da media."""
    soma = 0
    for linha in registros:
        soma += linha["receita_total"]
    media = soma / len(registros)

    acima_da_media = 0
    for linha in registros:
        if linha["receita_total"] > media:
            acima_da_media += 1

    estatisticas = {
        "total_vendas": len(registros),
        "receita_total": round(soma, 2),
        "receita_media_por_venda": round(media, 2),
        "vendas_acima_da_media": acima_da_media,
    }

    print("\n=== ESTATISTICAS GERAIS ===")
    print(estatisticas)
    return estatisticas


def exportar_resultados(metricas, clientes, estatisticas):
    """Exporta os resultados do projeto em CSV e JSON."""
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/metricas_por_mes.csv", "w", newline="",
              encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=metricas["por_mes"][0].keys())
        escritor.writeheader()
        escritor.writerows(metricas["por_mes"])

    with open("outputs/segmentacao_clientes.csv", "w", newline="",
              encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=clientes[0].keys())
        escritor.writeheader()
        escritor.writerows(clientes)

    caminho = "outputs/estatisticas_gerais.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(estatisticas, f, indent=4, ensure_ascii=False)

    # le de volta para confirmar que gravou
    with open(caminho, "r", encoding="utf-8") as f:
        conferencia = json.load(f)
    print(f"\nJSON gravado e lido: {conferencia}")


def main():
    """Executa o fluxo completo do SalesInsight PY."""
    print("=" * 60)
    print(" SALESINSIGHT PY - Analise de Dados de Vendas")
    print("=" * 60)

    if not os.path.exists("vendas.csv"):
        gerar_dataset_vendas("vendas.csv")

    registros = carregar_dataset("vendas.csv")
    inspecionar_dados(registros)
    registros_limpos, relatorio = limpar_dados(registros)
    registros_limpos = criar_colunas_derivadas(registros_limpos)

    # duas lambdas em contextos diferentes
    registros_limpos = processar_coluna(registros_limpos, "receita_total",
                                        lambda x: round(x / 1000, 2),
                                        nome_saida="receita_em_milhares")
    registros_limpos = processar_coluna(registros_limpos, "quantidade",
                                        lambda q: "Alto Volume" if q > 5 else "Baixo Volume",
                                        nome_saida="perfil_volume")

    metricas = calcular_metricas(registros_limpos)
    clientes = segmentar_clientes(registros_limpos)
    estatisticas = calcular_estatisticas(registros_limpos)
    exportar_resultados(metricas, clientes, estatisticas)

    print("\n[CONCLUIDO] Fluxo finalizado com sucesso.")


if __name__ == "__main__":
    main()
