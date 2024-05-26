import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from ReqSQL import obter_idobra, criarObra, criarRanking, criarLeitura
from config import criarDriver, url1, url2

def extrair_nota(texto):
    try:
        if texto == '':
            return None

        i = texto.find(' ')
        if i >= 0:
            texto = texto[:i]

        return int(10 * float(texto.replace(',', '.')))
    except:
        return 0

def extrair_ano(texto):
    try:
        if texto == '':
            return 0

        i = texto.find(' ')
        if i >= 0:
            texto = texto[:i]

        i = texto.find('-')
        if i >= 0:
            texto = texto[:i]

        i = texto.find('–')
        if i >= 0:
            texto = texto[:i]

        return int(texto)
    except:
        return 0

def extrair_idexterno(texto):
    i = texto.find('title/')
    f = texto.find('/', i + 6)
    return texto[(i + 6):f]

def inserir_obra_e_ranking(idleitura, titulo, idexterno, poster, ano, duracao, classificacao, nota, posicao, tipo):
    idobra = obter_idobra(idexterno)
    
    if idobra is None:        
        idobra = criarObra(titulo, idexterno, poster, ano, duracao, classificacao, nota, tipo)

    criarRanking(idleitura, idobra, posicao)

driver = criarDriver()

obras = []

# Criar uma nova leitura para filmes
leitura_filmes = criarLeitura()

# Usar a mesma leitura para séries
leitura_series = leitura_filmes

for tipo in range(1, 3):
    leitura = leitura_filmes if tipo == 1 else leitura_series

    driver.get(url1 if tipo == 1 else url2)

    imagens = WebDriverWait(driver, 80).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.cli-poster-container img.ipc-image'))
    )

    idsexternos = WebDriverWait(driver, 80).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.cli-poster-container a.ipc-lockup-overlay'))
    )

    metadados_linha = WebDriverWait(driver, 80).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.cli-children div.cli-title-metadata'))
    )

    notas_linha = WebDriverWait(driver, 80).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.cli-children div.cli-ratings-container'))
    )

    titulos = WebDriverWait(driver, 80).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.cli-children h3.ipc-title__text'))
    )

    posicao = 0

    for titulo in titulos:
        if posicao < len(imagens) and posicao < len(idsexternos) and posicao < len(metadados_linha) and posicao < len(notas_linha):
            metadados = metadados_linha[posicao].find_elements(By.CSS_SELECTOR, 'span')

            qtde_dados = len(metadados)

            ano = 0
            duracao = ''
            classificacao = ''

            if qtde_dados > 0:
                ano = extrair_ano(metadados[0].text)

                if qtde_dados == 2:
                    duracao = metadados[1].text
                    classificacao = ''

                    if duracao.find('h') < 0 and duracao.find('ep') < 0:
                        classificacao = duracao
                        duracao = ''

                elif qtde_dados == 3:
                    duracao = metadados[1].text
                    classificacao = metadados[2].text

            obras.append({
                'titulo': titulo.text,
                'idexterno': extrair_idexterno(idsexternos[posicao].get_attribute('href')),
                'poster': imagens[posicao].get_attribute('src'),
                'ano': ano,
                'duracao': duracao,
                'classificacao': classificacao,
                'nota': extrair_nota(notas_linha[posicao].text),
                'posicao': posicao + 1,
                'tipo': tipo
            })

            inserir_obra_e_ranking(leitura, titulo.text, extrair_idexterno(idsexternos[posicao].get_attribute('href')), imagens[posicao].get_attribute('src'), ano, duracao, classificacao, extrair_nota(notas_linha[posicao].text), posicao + 1, tipo)

            posicao = posicao + 1
            
driver.close()
