import pandas as pd

tabela = pd.read_csv("plan\Grupos - Horas - Legenda.csv")

tabela_html = tabela.to_html()

nome_arquivo_html = "tabela.html"

with open(nome_arquivo_html, "w", encoding="utf-8") as arquivo:
    arquivo.write(tabela_html)

print(f"Tabela salva em {nome_arquivo_html}")

