from bs4 import BeautifulSoup
import re

def ler_nota_teste():
    # 1. Carrega o arquivo HTML
    try:
        with open("nota_teste_1.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Erro: O arquivo 'nota_teste_1.html' não foi encontrado na pasta.")
        return

    # 2. Cria a 'Sopa'
    soup = BeautifulSoup(html_content, "html.parser")

    # --- Extração do Cabeçalho ---
    print("=== DADOS DA NOTA ===")
    
    # Nome do Mercado (Classe txtTopo)
    div_mercado = soup.find("div", class_="txtTopo")
    nome_mercado = div_mercado.text.strip() if div_mercado else "Mercado Desconhecido"
    print(f"Mercado: {nome_mercado}")

    # Data da Emissão (Um pouco mais chato de pegar, pois está no meio de um texto)
    # Procuramos pela tag <strong> que contém "Emissão:"
    data_emissao = "Data desconhecida"
    infos_gerais = soup.find_all("strong")
    for info in infos_gerais:
        if "Emissão:" in info.text:
            # O texto da data está logo depois do fechar da tag </strong>
            # Ex: <strong> Emissão: </strong> 20/12/2025 ...
            data_raw = info.next_sibling
            if data_raw:
                # Pega só os primeiros 19 caracteres (dd/mm/aaaa hh:mm:ss)
                data_emissao = data_raw.strip()[:19]
            break
    
    print(f"Data: {data_emissao}")
    print("-" * 30)

    # --- Extração dos Itens ---
    tabela = soup.find("table", {"id": "tabResult"})
    
    if not tabela:
        print("Erro: Tabela de produtos não encontrada.")
        return

    linhas = tabela.find_all("tr")
    
    itens_processados = []

    for linha in linhas:
        # Encontra os spans principais
        span_nome = linha.find("span", class_="txtTit")
        span_qtd = linha.find("span", class_="Rqtd")
        span_preco = linha.find("span", class_="RvlUnit")

        if span_nome and span_qtd and span_preco:
            # 1. Nome: Pega o texto e remove espaços extras
            nome = span_nome.text.strip()

            # 2. Quantidade: Vem como "Qtde.:1" ou "Qtde.:0,99"
            # .split(':') quebra em ['Qtde.', '0,99']
            qtd_texto = span_qtd.text.split(':')[1].strip()
            qtd_float = float(qtd_texto.replace(',', '.'))

            # 3. Preço Unitário: Vem como "Vl. Unit.:\n 13,59"
            preco_texto = span_preco.text.split(':')[1].strip()
            preco_float = float(preco_texto.replace(',', '.'))

            # Adiciona na lista
            item = {
                "nome": nome,
                "quantidade": qtd_float,
                "preco_unitario": preco_float,
                "total": round(qtd_float * preco_float, 2)
            }
            itens_processados.append(item)
            
            # Mostra no terminal bonitinho
            print(f"Item: {nome} | Qtd: {qtd_float} | $ Unit: {preco_float}")

    print("-" * 30)
    print(f"Total de itens lidos: {len(itens_processados)}")

if __name__ == "__main__":
    ler_nota_teste()