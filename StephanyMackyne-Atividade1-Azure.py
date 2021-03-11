# ======================================= 
# ATIVIDADE 1 - AZURE (equivalente a Atividade 09)
# Autor: Stephany Mackyne
# Turma: Turma 5 - Engenharia de Dados. Accademia Accenture.
# Data de entrega: até 06/03/2020
# Descrição da atividade: Leitura de dados da API do IBGE, com o uso do package requests, para escrever em Banco de Dados 
# relacional alocado no Azure os seguintes dados: UFs, Municípios (relacionados com UFs) e Distritos (relacionados com Municípios).
# ======================================= 

import requests
import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=sqlserversmsv.database.windows.net;' 
                      'Database=db2;'
                      'UID=sqluser;'
                      'PWD=Pa$$wOrd1234;')

cursor = conn.cursor()

query = {"orderBy": "nome"}

try:
    responseEstados = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados", params=query)
    estados = responseEstados.json()
    for estado in estados:
        idEstado = estado["id"]
        nomeEstado = estado["nome"]
        siglaEstado = estado["sigla"]

        cursor.execute("INSERT INTO ESTADOS VALUES (?, ?, ?)", idEstado, siglaEstado, nomeEstado)
    cursor.commit()
except:
    print("Ocorreu um erro! Os dados dos Estados não foram inseridos no banco. \n")    
else:
    print("Dados dos Estados inseridos com sucesso! \n")

try:
    responseMunicipios = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios", params=query)
    municipios = responseMunicipios.json()
    for municipio in municipios:
        idMunicipio = municipio["id"]
        nomeMunicipio = municipio["nome"]
        idEstado = municipio["microrregiao"]["mesorregiao"]["UF"]["id"]

        cursor.execute("INSERT INTO MUNICIPIOS VALUES (?, ?, ?)", idMunicipio, nomeMunicipio, idEstado)
    cursor.commit()
except:
    print("Ocorreu um erro! Os dados dos Municipios não foram inseridos no banco. \n")    
else:
    print("Dados dos Municipios inseridos com sucesso! \n")

try:
    responseDistritos = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/distritos", params=query, timeout=300)
    distritos = responseDistritos.json()
    for distrito in distritos:
        idDistrito = distrito["id"]
        nomeDistrito = distrito["nome"]
        idMunicipio = distrito["municipio"]["id"]
        cursor.execute("INSERT INTO DISTRITOS VALUES (?, ?, ?)", idDistrito, nomeDistrito, idMunicipio)
    cursor.commit()
except:
    print("Ocorreu um erro! Os dados dos Distritos não foram inseridos no banco. \n")    
else:
    print("Dados dos Distritos inseridos com sucesso! \n")
finally:
    print("Programa finalizado!")

conn.close()
