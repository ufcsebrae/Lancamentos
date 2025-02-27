
import win32com.client as win32
import os
import pandas as pd
from time import gmtime, strftime


def gerar_corpo_email(dados):
    primeira_linha_lancamentos = dados[0]['detalhes'][0].get("TIPO PAGAMENTO", "Desconhecido")
    primeira_linha_faculdade = dados[8]['detalhes'][0].get("TIPO", "Desconhecido")
    primeira_linha_baixado = dados[7]['detalhes'][0].get("NOME FANTASIA CLIENTE", "Desconhecido")

    valor_total_lancamentos = dados[0]['detalhes'][0].get("VALOR ORIGINAL TOTAL", 0)
    valor_total_faculdade = dados[8]['detalhes'][0].get("ORIGINAL", 0)
    valor_total_baixado = dados[7]['detalhes'][0].get("A_PAGAR", 0)

    valor_total_lancamentos_formatado = f"R$ {valor_total_lancamentos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    valor_total_faculdade_formatado = f"R$ {valor_total_faculdade:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    valor_total_baixado_formatado = f"R$ {valor_total_baixado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    # Gerar a data atual formatada
    data_atual = strftime('%d/%m/%Y', gmtime())
    corpo = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
                font-size: 14px;
                color: #333;
                background-color: #f9f9f9;
            }}
            .container {{
                background: #fff;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                max-width: 800px;
                margin: auto;
                box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
            }}
            h2 {{
                color: #007BFF;
                text-align: center;
                font-size: 22px;
                margin-bottom: 20px;
            }}
            h3 {{
                color: #555;
                font-size: 16px;
                margin-top: 10px;
                margin-bottom: 5px;
            }}
            table {{
                width: 80%;
                border-collapse: collapse;
                margin: 15px auto;
                font-size: 14px;
                background-color: #fff;
                color: #000;
                border: 1px solid #333;
            }}
            th, td {{
                border: 1px solid #333;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f4f4f4;
                color: #333;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>Prezados,</p>
            <p>Encaminhamos informações atualizadas sobre os lançamentos em aberto até a data <strong>{data_atual}</strong>.</p>
            <p>Observa-se que o tipo de pagamento com maior valor é <strong>{primeira_linha_lancamentos}</strong> totalizando <strong>{valor_total_lancamentos_formatado}</strong>, na Faculdade Sebrae <strong>{primeira_linha_faculdade}</strong> tem o maior número de registros totalizando <strong>{valor_total_faculdade_formatado}</strong>, já a <strong>{primeira_linha_baixado}</strong> tem o maior valor de parcelas em aberto totalizando <strong>{valor_total_baixado_formatado}</strong>.</p>

            </div>
            <div class="container">
            <h2>LANÇAMENTOS EM ABERTO</h2>

    """

    #for loop preenche tabela 1
    for resumo in dados[:1]:
        print(type(resumo))  # Verifique se é um dicionário
        print(resumo)  # Verifique o conteúdo de resumo
        # Calcular a quantidade total de registros e o valor total corretamente
        quantidade_total = sum(detalhe.get("QUANTIDADE", 0) for detalhe in resumo['detalhes'])
        valor_total = sum(detalhe.get("VALOR ORIGINAL TOTAL", 0) for detalhe in resumo['detalhes'])
        # Formatar o valor total com separador de milhar no formato brasileiro
        valor_total_formatado = f"{valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        corpo += f"""
       
            <h3>Quantidade de Registros: {quantidade_total}</h3>
            <h3>Valor Total: R$ {valor_total_formatado}</h3>
      
        """

        # Tabela para Tipo de Pagamento, Quantidade e Valor Total
        corpo += """
        <table>
            <thead>
                <tr>
                    <th>Tipo Pagamento</th>
                    <th>Quantidade</th>
                    <th>Valor Total</th>
                </tr>
            </thead>
            <tbody>
        """

        # Criação do dicionário para agrupar por "Tipo de Pagamento"
        tipo_pagamento_resumo = {}
        for detalhe in resumo['detalhes']:
            tipo_pagamento = detalhe.get("TIPO PAGAMENTO", "Desconhecido")
            valor_quantidade = detalhe.get("QUANTIDADE", 0)
            valor_por_tipo = detalhe.get("VALOR ORIGINAL TOTAL", 0)

            if tipo_pagamento not in tipo_pagamento_resumo:
                tipo_pagamento_resumo[tipo_pagamento] = {'quantidade': 0, 'valor_total': 0}

            tipo_pagamento_resumo[tipo_pagamento]['quantidade'] += valor_quantidade
            tipo_pagamento_resumo[tipo_pagamento]['valor_total'] += valor_por_tipo

        for tipo_pagamento, resumo_pago in tipo_pagamento_resumo.items():
            valor_formatado = f"{resumo_pago['valor_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            corpo += f"""
            <tr>
                <td>{tipo_pagamento}</td>
                <td>{resumo_pago['quantidade']}</td>
                <td>R$ {valor_formatado}</td>
            </tr>
            """
        corpo += """
            </tbody>
        </table>
        <br>
        """
    #for loop preenche tabela faculdade
    for resumo in dados[:9]:
            print(type(resumo))  # Verifique se é um dicionário
            print(resumo)  # Verifique o conteúdo de resumo
            quantidade_total_2 = sum(detalhe.get("QUANTIDADE", 0) for detalhe in resumo['detalhes'])
            valor_total_2 = sum(detalhe.get("ORIGINAL", 0) for detalhe in resumo["detalhes"])
            valor_total_formatado_2 = f"{valor_total_2:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    corpo += f"""
        </div>
        <div class="container">
        <h2>FACULDADE SEBRAE</h2>
        
            <h3>Quantidade de Registros: {quantidade_total_2}</h3>
            <h3>Valor Total: R$ {valor_total_formatado_2}</h3>  
        
        """

        # Cabeçalho da tabela
    corpo += """
        <table>
            <thead>
                <tr>
                    <th>Tipo</th>
                    <th>Quantidade de Registros</th>
                    <th>Valor Total</th>
                </tr>
            </thead>
            <tbody>
        """

        # Criação do dicionário para agrupar por "Tipo de Pagamento"
    tipo_pagamento_resumo_2 = {}
    for detalhe in resumo["detalhes"]:
            tipo_pagamento = detalhe.get("TIPO", "Desconhecido")
            valor_quantidade = detalhe.get("QUANTIDADE", 0)
            valor_por_tipo = detalhe.get("ORIGINAL", 0)

            if tipo_pagamento not in tipo_pagamento_resumo_2:
                tipo_pagamento_resumo_2[tipo_pagamento] = {'quantidade': 0,"valor_total": 0}
            
            tipo_pagamento_resumo_2[tipo_pagamento]["valor_total"] += valor_por_tipo
            tipo_pagamento_resumo_2[tipo_pagamento]['quantidade'] += valor_quantidade


        # Loop para preencher a tabela
    for tipo_pagamento, resumo_pago in tipo_pagamento_resumo_2.items():
            valor_formatado = f"{resumo_pago['valor_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            corpo += f"""
            <tr>
                <td>{tipo_pagamento}</td>
                <td>{resumo_pago['quantidade']}</td>
                <td>R$ {valor_formatado}</td>
            </tr>   
            """

    corpo += """
        </tbody>
    </table>
    <br>
"""  
## for loop preenche tabela BAIXADO PARCIAL
    for resumo in dados[:8]:
            print(type(resumo))  # Verifique se é um dicionário
            print(resumo)  # Verifique o conteúdo de resumo
            valor_total_3 = sum(detalhe.get("A_PAGAR", 0) for detalhe in resumo["detalhes"])
            valor_total_formatado_3 = f"{valor_total_3:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


    corpo += f"""
        </div>
        <div class="container">
        <h2>BAIXADO PARCIALMENTE</h2>
        
            <h3>Valor Total a Pagar: R$ {valor_total_formatado_3}</h3> 
        
        """

        # Cabeçalho da tabela
    corpo += """
        <table>
            <thead>
                <tr>
                    <th>Cliente</th>
                    <th>Valor Total a Pagar</th>
                </tr>
            </thead>
            <tbody>
        """

        # Criação do dicionário para agrupar por "Tipo de Pagamento"
    tipo_pagamento_resumo_3 = {}
    for detalhe in resumo["detalhes"]:
            tipo_pagamento = detalhe.get("NOME FANTASIA CLIENTE", "Desconhecido")
            valor_por_tipo = detalhe.get("A_PAGAR", 0)

            if tipo_pagamento not in tipo_pagamento_resumo_3:
                tipo_pagamento_resumo_3[tipo_pagamento] = {"valor_total": 0}
            
            tipo_pagamento_resumo_3[tipo_pagamento]["valor_total"] += valor_por_tipo
            


        # Loop para preencher a tabela
    for tipo_pagamento, resumo_pago in tipo_pagamento_resumo_3.items():
            valor_formatado = f"{resumo_pago['valor_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            corpo += f"""
            <tr>
                <td>{tipo_pagamento}</td>
                <td>R$ {valor_formatado}</td>
            </tr>   
            """

    corpo += """
        </tbody>
    </table>
    <br>
"""  
    corpo += """
        </div>
        <div class="footer">
            <p>Este é um e-mail automático. Por favor, não responda.</p>
        </div>
    </body>
    </html>
    """
    return corpo

 
 
def enviar_email(destinatario, copiar, assunto, corpo, caminho_anexo):
    outlook = win32.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)  
    mail.To = destinatario
    mail.cc = copiar
    mail.Subject = assunto
    mail.HTMLBody = corpo
    if caminho_anexo and os.path.exists(caminho_anexo):
        mail.Attachments.Add(caminho_anexo)
   
    mail.Send()
    print("E-mail enviado com sucesso!")