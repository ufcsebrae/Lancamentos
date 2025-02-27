import sqlalchemy
import os
import pandas as pd
from query_lancamentos_abertos import queries 
from enviaremail_lancamentos import gerar_corpo_email, enviar_email
from time import gmtime, strftime
import logging

# Configuração do logger para facilitar o debug
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def consulta_sql():
    servername = "spsvsql39\\metas"
    dbname = "HubDados"
    engine = sqlalchemy.create_engine(
        f'mssql+pyodbc://@{servername}/{dbname}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    )

    resultados = {}
    dados_para_email = []

    try:
        with engine.connect() as connection:
            for nome_query, query in queries.items():
                
                logging.info(f"Executando consulta: {nome_query}")
                resultado = pd.read_sql(query, connection)
                logging.info(f"Consulta '{nome_query}' concluída com {len(resultado)} registros.")
                resultados[nome_query] = resultado

                # Resumo para o e-mail
                resumo = {
                    "nome_da_tabela": nome_query,
                    "quantidade": len(resultado),
                    "valor_total": resultado.get("VALOR ORIGINAL", pd.Series()).sum(),
                    "detalhes": resultado.to_dict(orient="records")[:50],  # Limitar os detalhes para e-mail
                    "data": strftime("%d/%m/%Y", gmtime())
                }
                dados_para_email.append(resumo)
    except Exception as e:
        logging.error(f"Erro ao executar consultas SQL: {e}")
        raise

    return dados_para_email, resultados

def salvar_arquivo_excel(resultados):
    data = strftime('%d-%m-%Y', gmtime())
    arquivo_excel = os.path.join(os.getcwd(), "lancamentos_abertos_" + data + ".xlsx")

    try:
        with pd.ExcelWriter(arquivo_excel, engine='xlsxwriter') as writer:
            for nome_query, dataframe in resultados.items():
                logging.info(f"Salvando resultados da consulta '{nome_query}' no Excel.")
                dataframe.to_excel(writer, sheet_name=nome_query[:30], index=False)
    except Exception as e:
        logging.error(f"Erro ao salvar arquivo Excel: {e}")
        raise

    logging.info(f"Arquivo Excel salvo em: {arquivo_excel}")
    return arquivo_excel

def main():
    try:
        # Etapa 1: Consultas SQL
        logging.info("Iniciando execução das consultas SQL.")
        dados, resultados = consulta_sql()

        # Etapa 2: Gerar corpo do e-mail
        logging.info("Gerando corpo do e-mail.")
        corpo_email = gerar_corpo_email(dados)

        # Etapa 3: Salvar resultados no Excel
        logging.info("Salvando resultados em arquivo Excel.")
        caminho_anexo = salvar_arquivo_excel(resultados)

        # Etapa 4: Enviar e-mail
        destinatario = "SP-ContasaReceber@sp.sebrae.com.br"
        copiar = "cesargl@sebraesp.com.br; douglasc@sebraesp.com.br; marcelocp@sebraesp.com.br; contabilidade@sp.sebrae.com.br; orcamento@sp.sebrae.com.br"
        assunto = f"Posição sobre lançamentos em aberto - {strftime('%d/%m/%Y', gmtime())}"
        logging.info(f"Enviando e-mail para {destinatario}.")
        enviar_email(destinatario, copiar, assunto, corpo_email, caminho_anexo)

        logging.info("Processo concluído com sucesso.")
    except Exception as e:
        logging.error(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    main()