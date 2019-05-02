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