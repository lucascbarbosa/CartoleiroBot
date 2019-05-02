import pandas as pd
import cartolafc
import pandas as pd
import io
import requests
import json
import urllib.request
import ast
from xml.sax import saxutils as su
def editHtml():
    arqJogadores = open('Templates\jogadores.html','r')
    arqDestaques = open('Templates\destaques.html','r')
    arqClubes = open('Templates\clubes.html','r')

    jogadores = arqJogadores.readlines()
    destaques = arqDestaques.readlines()
    clubes = arqClubes.readlines()

    i = 1
    newJogadores = []
    newDestaques = []
    newClubes = []
    for lines in jogadores:
        if (i-27) % 17 == 0:
            newJogadores.append(su.unescape(lines))
        else:
            newJogadores.append(lines)
        i+=1

    i = 1
    for lines in destaques:
        if (i-23) % 14 == 0 or (i-29) % 14 == 0:
            newDestaques.append(su.unescape(lines))
        else:
            newDestaques.append(lines)


        i += 1

    i = 1
    for lines in clubes:
        if (i-23) % 11 == 0 or (i-24) % 11 == 0 or (i-25) % 11 == 0: 
            newClubes.append(su.unescape(lines))

        else:
            newClubes.append(lines)
            
        i += 1


    newClubes = '\n'.join(newClubes)
    newDestaques = '\n'.join(newDestaques)
    newJogadores = '\n'.join(newJogadores)
    arqJogadores = open('Templates\jogadores.html','w')
    arqDestaques = open('Templates\destaques.html','w')
    arqClubes = open('Templates\clubes.html','w')
    arqJogadores.write(newJogadores)
    arqDestaques.write(newDestaques)
    arqClubes.write(newClubes)

api = cartolafc.Api()
mercado = api.mercado()
api =  cartolafc.Api(email='lucas.barbosa.0899@gmail.com', password='08101999')

url_rodadas="https://api.cartolafc.globo.com/rodadas"
with urllib.request.urlopen(url_rodadas) as url:
    data_rodadas = json.loads(url.read()) #get content of all the rounds of the competition, from url

url_partidas = "https://api.cartolafc.globo.com/partidas"
with urllib.request.urlopen(url_partidas) as url:
    data_partidas = json.loads(url.read())  #get content of the past matches, from url

url_jogadoresDestaque = "https://api.cartolafc.globo.com/mercado/destaques"
with urllib.request.urlopen(url_jogadoresDestaque) as url:
    data_jogadoresDestaque = json.loads(url.read())  #get content of the best players of the last round

url_jogadores = "https://api.cartolafc.globo.com/atletas/mercado"
with urllib.request.urlopen(url_jogadores) as url:
    data_jogadores = json.loads(url.read())  #get content of the past matches from url

#Auxiliary Functions
def format(url):
    url = str(url)
    p = url.split('_')
    new_url = p[0]+'_140x140.png'
    return new_url

def path_to_image_html(path):
    '''
     This function essentially convert the image url to 
     '<img src="'+ path + '"/>' format. And one can put any
     formatting adjustments to control the height, aspect ratio, size etc.
     within as in the below example. 
    '''

    return '<img src="'+ path + '" style=max-height:124px;"/>'


#DataFrame functions
def createDataFrameRodadas(data):
    dfRodadas = pd.DataFrame(data)
    return dfRodadas

def createDataFramePartidas(data):#Create a df with the matches
    dfPartidas = pd.DataFrame(data) 
    dfApVis = dfPartidas['aproveitamento_visitante'].apply(pd.Series)
    dfApMan = dfPartidas['aproveitamento_mandante'].apply(pd.Series)
    colunas_mandante=[('Aproveitamento Mandante',str(i+1))for i in range(5)]#Starting at 1 instead of 0
    dfApMan.columns=pd.MultiIndex.from_tuples(colunas_mandante)
    colunas_visitante=[('Aproveitamento Visitante',str(i+1))for i in range(5)]
    dfApVis.columns=pd.MultiIndex.from_tuples(colunas_visitante)
    dfPartidas = pd.concat([dfPartidas,dfApVis,dfApMan], axis = 1).drop(['aproveitamento_visitante','aproveitamento_mandante'],axis = 1)
    dfPartidas.head()
    return dfPartidas

def createDataFrameClubes(data): #create a df with the teams 
    dfClubes = pd.DataFrame(data).T #transpose because the id was the collumns
    #but we need to expand 'escudos' column, so we create a df from it, and then join with dfClubes
    dfEscudos = pd.DataFrame(list(dfClubes['escudos'])).set_index(dfClubes.index) #create df with escudos info
    dfClubes = pd.concat([dfClubes,dfEscudos], axis = 1)
    dfClubes = dfClubes.drop(['escudos'],axis = 1)
    return dfClubes

def createDataFrameJogadoresDestaque(data):
    dfJogadoresDestaque = pd.DataFrame(data)
    pd.set_option('display.max_colwidth',-1)#visualize the entire url
    dfAtleta = pd.DataFrame(list(dfJogadoresDestaque['Atleta'])) #as well as in dfClubes, here we have to expand 'atletas' column in a df with player's info
    dfJogadoresDestaque = pd.concat([dfAtleta,dfJogadoresDestaque],axis=1)
    dfJogadoresDestaque = dfJogadoresDestaque.drop(['Atleta'],axis=1)
    return dfJogadoresDestaque

def createDataFrameJogadores(data):
    dfJogadores = pd.DataFrame(data['atletas'])
    dfStatus= pd.DataFrame(data['status']).T.set_index('id')#create a dic to convert 'status_id' cells from an id to the status
    dic = dfStatus.to_dict()['nome']
    dfJogadores['status_id'].replace(dic,inplace = True)#replace 
    dfJogadores.rename(columns = {'status_id':'status'},inplace = True) #rename column
    dfScouts = dfJogadores['scout'].apply(pd.Series)
    dfJogadores = pd.concat([dfJogadores, dfScouts], axis=1).drop('scout', axis=1)
    return dfJogadores

def main():
    dfRodadas = createDataFrameRodadas(content_rodadas) #create 3 dataframes
    dfPartidas = createDataFramePartidas(data_partidas['partidas'])
    dfClubes = createDataFrameClubes(data_partidas['clubes'])
    dfClubes['30x30'] = dfClubes['30x30'].apply(format)
    dfClubes['30x30'] = dfClubes['30x30'].apply(path_to_image_html)
    dfClubes['45x45'] = dfClubes['45x45'].apply(format)
    dfClubes['45x45'] = dfClubes['45x45'].apply(path_to_image_html)
    dfClubes['60x60'] = dfClubes['60x60'].apply(format)
    dfClubes['60x60'] = dfClubes['60x60'].apply(path_to_image_html)
    dfJogadoresDestaque = createDataFrameJogadoresDestaque(data_jogadoresDestaque)
    dfJogadoresDestaque['foto'] = dfJogadoresDestaque['foto'].apply(format)
    dfJogadoresDestaque['foto'] = dfJogadoresDestaque['foto'].apply(path_to_image_html)
    dfJogadoresDestaque['escudo_clube'] = dfJogadoresDestaque['escudo_clube'].apply(format)
    dfJogadoresDestaque['escudo_clube'] = dfJogadoresDestaque['escudo_clube'].apply(path_to_image_html)
    dfJogadores = createDataFrameJogadores(data_jogadores)
    dfJogadores['foto'] = dfJogadores['foto'].apply(format)
    dfJogadores['foto'] = dfJogadores['foto'].apply(path_to_image_html)

    #Convert to html
    dfPartidas.to_html('Templates\Partidas.html')
    dfRodadas.to_html('Templates\Rodadas.html')
    dfClubes.to_html('Templates\Clubes.html')
    dfJogadoresDestaque.to_html('Templates\Destaques.html')
    dfJogadores.to_html('Templates\Jogadores.html')
    
    editHtml()

    return dfPartidas,dfRodadas,dfJogadoresDestaque,dfJogadores    
