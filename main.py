def inserir_por_percentual(percentual, paginas_totais):
  percentual_decimal = (percentual / 100)
  pagina_atual = paginas_totais * percentual_decimal
  return pagina_atual


print("Programa marca pagina")
import sqlite3

conexão = sqlite3.connect("biblioteca.db")
cursor = conexão.cursor()
#voltar a ser tudo texto
cursor.execute('''
   CREATE TABLE IF NOT EXISTS leitura (
   titulo_livro TEXT,
   paginas_totais TEXT,
   pagina_atual TEXT,
   texto_referencia TEXT
    )
''') 
print("selecione: 01-consultar, 02-registrar, 03-alterar progresso")
op = int(input("seleção: "))

if op == 1:
  #consulta
  from contextlib import closing
  with sqlite3.connect("biblioteca.db") as conexão:
    with closing(conexão.cursor()) as cursor:
      cursor.execute("select * from leitura")
      id = 0
      while True:
        resultado = cursor.fetchone()
        if resultado == None:
          break
        #print("Nome Produto: %s\nPreço: %s" % (resultado))
        print("id: ", id)
        id = id + 1
        print("Titulo: ", resultado[0])
        print("Paginas Totais: ", resultado[1])
        print("pagina Atual: ", resultado[2])
        progressao = (float(resultado[2]) / float(resultado[1]) * 100)
        print("progresso: ", progressao, "%")
        print("texto referencia: ", resultado[3])
        print("-" * 30)

elif op == 2:
  cursor = conexão.cursor()
  titulo = str(input("digite o titulo: "))
  tot_pags = int(input("digite o total de paginas: "))
  pag_atual = int(input("digite a pagina atual: "))
  text_ref= str(input("digite o texto onde parou: "))
  cursor.execute(
      '''
    insert into leitura (titulo_livro, paginas_totais,pagina_atual, texto_referencia)
    values(?, ?, ?, ?)
    ''', (titulo, str(tot_pags), str(pag_atual), text_ref))
  conexão.commit()
  cursor.close()
  conexão.close()
elif op == 3:
  #fazer a famosa consulta
  from contextlib import closing
  with sqlite3.connect("biblioteca.db") as conexão:
    with closing(conexão.cursor()) as cursor:
      cursor.execute("select * from leitura")
      id = 0
      lista_titulos = []
      lista_paginas_totais = []
      while True:

        resultado = cursor.fetchone()
        if resultado == None:
          break
        #print("Nome Produto: %s\nPreço: %s" % (resultado))
        print("id: ", id)
        id = id + 1
        print("Titulo: ", resultado[0])
        lista_titulos.append(resultado[0])
        print("Paginas Totais: ", resultado[1])
        lista_paginas_totais.append(resultado[1])
        print("pagina Atual: ", resultado[2])
        progressao = (float(resultado[2]) / float(resultado[1]) * 100)
        print("progresso: ", progressao, "%")
        print("texto referencia: ", resultado[3])
        print("-" * 30)

      id_select = int(input("digite o id para alterar"))
      titulo = str(lista_titulos[id_select])
      print("voce selecionou alterar: ", titulo)
      print("inserir por: 1-pagina atual, ou 2-percentual")
      escolha = int(input("digite: "))
      if escolha == 2:
        paginas_totais = lista_paginas_totais[id_select]
        perc = float(input("digite o percentual, ex: 40 --> 40%"))
        text_ref = str(input("digite o texto onde parou: "))
        pag_atual_nova = int(inserir_por_percentual(perc, float(paginas_totais)))
        cursor = conexão.cursor()
        #dados = [(pag_atual_nova, alterar)]
        consulta = """
        UPDATE leitura
        SET pagina_atual = ?,
        texto_referencia = ?
        WHERE titulo_livro = ?
        """

        conexão = sqlite3.connect("biblioteca.db")
        cursor = conexão.cursor()
        # Executando a consulta com as variáveis como parâmetros
        cursor.execute(consulta, (str(pag_atual_nova), str(text_ref) ,str(titulo)))

        # Salvando as alterações
        conexão.commit()

        # Fechando a conexão com o banco de dados
        conexão.close()
      else:
        pag_atual_nova = int(input("digite a nova pagina atual: "))
        referencial = str(input("digite o texto onde parou: "))
        cursor = conexão.cursor()
        #dados = [(pag_atual_nova, alterar)]
        consulta = """
        UPDATE leitura
        SET pagina_atual = ?,
        texto_referencia = ?
        WHERE titulo_livro = ?
        """

        conexão = sqlite3.connect("biblioteca.db")
        cursor = conexão.cursor()
        # Executando a consulta com as variáveis como parâmetros
        cursor.execute(consulta, (str(pag_atual_nova), str(referencial), str(titulo)))

        # Salvando as alterações
        conexão.commit()

        # Fechando a conexão com o banco de dados
        conexão.close()

else:
  print("fora das opções")
