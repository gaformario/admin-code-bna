from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from datetime import datetime
from config import popular

engine = create_engine(popular)

def criarLeitura():
    with Session(engine) as sessao, sessao.begin():
        sessao.execute(text("INSERT INTO leitura (data) VALUES (curdate())"))

        resultado = sessao.execute(text("SELECT last_insert_id() idleitura"))
        return resultado.fetchone()[0]

def criarObra(titulo, idexterno, poster, ano, duracao, classificacao, nota, tipo):
    with Session(engine) as sessao, sessao.begin():
        obra = {
            'titulo': titulo,
            'idexterno': idexterno,
            'poster': poster,
            'ano': ano,
            'duracao': duracao,
            'classificacao': classificacao,
            'nota': nota,
            'tipo': tipo
        }

        sessao.execute(text("INSERT INTO obra (titulo, idexterno, poster, ano, duracao, classificacao, nota, tipo) VALUES (:titulo, :idexterno, :poster, :ano, :duracao, :classificacao, :nota, :tipo)"), obra)

        resultado = sessao.execute(text("SELECT last_insert_id() idobra"))
        return resultado.fetchone()[0]

def criarRanking(idleitura, idobra, posicao):
    with Session(engine) as sessao, sessao.begin():
        ranking = {
            'idobra': idobra,
            'posicao': posicao,
            'idleitura': idleitura
        }
        sessao.execute(text("INSERT INTO ranking (idobra, posicao, idleitura) VALUES (:idobra, :posicao, :idleitura)"), ranking)

def obter_idobra(idexterno):
    with engine.connect() as conexao:
        consulta = text("SELECT idobra FROM obra WHERE idexterno = :idexterno")
        
        resultado = conexao.execute(consulta, {'idexterno': idexterno})
        idobra = resultado.fetchone()

        if idobra:
            return idobra[0]  
        else:
            return None 

def listarRanking():
    with engine.connect() as conexao:
        resultado = conexao.execute(text("""
            SELECT ranking.posicao, obra.titulo, leitura.data, obra.poster,
                   obra.ano, obra.duracao, obra.classificacao, obra.nota, obra.tipo
            FROM ranking
            INNER JOIN obra ON ranking.idobra = obra.idobra
            INNER JOIN leitura ON ranking.idleitura = leitura.idleitura
        """))
        
        filmes = []
        for linha in resultado:
            filmes.append({
                'posicao': linha.posicao,
                'titulo': linha.titulo,
                'data_leitura': linha.data.strftime('%Y-%m-%d'),
                'poster': linha.poster,
                'ano': linha.ano,
                'duracao': linha.duracao,
                'classificacao': linha.classificacao,
                'nota': linha.nota,
                'tipo': linha.tipo
            })

        return filmes

