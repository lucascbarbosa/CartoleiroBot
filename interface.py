from flask import Flask, request, render_template
from extract import *
import editHtml
import pandas as pd
from xml.sax import saxutils as su
import datetime
import cartolafc

api = cartolafc.Api()


url_rodadas="https://api.cartolafc.globo.com/rodadas"
content_rodadas =requests.get(url_rodadas).content #get content of the past rounds, from url

url_partidas = "https://api.cartolafc.globo.com/partidas"
with urllib.request.urlopen(url_partidas) as url:
    data_partidas = json.loads(url.read())  #get content of the past matches, from url(this one has a json)

url_jogadoresDestaque = "https://api.cartolafc.globo.com/mercado/destaques"
with urllib.request.urlopen(url_jogadoresDestaque) as url:
    data_jogadoresDestaque = json.loads(url.read())  #get content of the best players of the last round, from url(this one has a json)

url_jogadores = "https://api.cartolafc.globo.com/atletas/mercado"
with urllib.request.urlopen(url_jogadores) as url:
    data_jogadores = json.loads(url.read())  #get content of the past matches from url(this one has a json)



def novoMercado(rodadaAtual,statusAtual):

    rodada_, status_ = rodadaAtual,statusAtual
    rodada_ = int(rodada_)
    status_ = int(status_)

    if rodada_ != rodada:
        rodada = rodada_

    else:
        return False

    if status_ != status:
        status = status_

        if status == 1:
            return True

        else:
            return False

    else:
        return False
    
    return False

app = Flask(__name__)

@app.route("/")
def hello():

    return render_template('jogadores.html')
    

app.run()
dfPartidas,dfRodadas,dfJogadoresDestaque,dfJogadores = main()
print(dfJogadores.head())

while True:

    if novoMercado(mercado.rodada_atual, mercado.status[1]):

        dfPartidas,dfRodadas,dfJogadoresDestaque,dfJogadores = main()