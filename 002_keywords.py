import re
import io
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import fileinput


def urlok(endereco):
    try:
        paginahtml = urlopen(endereco)
        test = str(paginahtml.info())
        validacaoHTML = 'Content-Type: text/html'
        if re.search(validacaoHTML, test, re.IGNORECASE):
            return paginahtml
        else:
            return 2
    except:
        return 1


def soupfinder(url, urlopenresult):

    global keywords
    achou_pagina = False
    achou_tag = False
    soup = BeautifulSoup(urlopenresult, "lxml")
    listadeloslinks = soup.find_all(['a', 'iframe', 'link'])

    for keyword in keywords:
        if not achou_pagina:
            if soup.find(text=re.compile(keyword, re.IGNORECASE)):
                with open("%s_transparenciapaginaToda.txt" %nombre, "a", newline="", encoding="UTF-8") as transparencia:
                    transparencia.write(str(url) + "\n")
                    transparencia.close()
                with open("%s_transparenciapaginaToda_date.txt" %nombre, "a", newline="", encoding="UTF-8") as logger:
                    log = str(datetime.datetime.now())
                    logger.write(log + "•" + str(url) + "\n")
                    logger.close()
                achou_pagina = True
        if not achou_tag:
            for item in listadeloslinks:
                if re.search(keyword, str(item), re.IGNORECASE):
                    if "<a" in str(item) or "<link" in str(item):
                        url = item.get('href')
                    elif '<iframe' in str(item):
                        url = item.get('src')
                    with open("%s_transparenciaTags.txt" %nombre, "a", newline="", encoding="UTF-8") as tpc_tag:
                        tpc_tag.write(str(url) + "\n")
                        tpc_tag.close()
                    with open("%s_transparenciaTags_date.txt" %nombre, "a", newline="", encoding="UTF-8") as marcador:
                        logg = str(datetime.datetime.now())
                        marcador.write(logg + "•" + str(url) + "\n")
                        marcador.close()
                    achou_tag = True
        if achou_pagina and achou_tag:  # cada iteracao de palavra-chave
            return 0  # achou na pagina inteira e numa tag
    if achou_tag or achou_pagina:  # depois de todas palavras-chave
        return 0  # achou na pagina inteira ou numa tag
    else:
        return 1  # nao achou nada nesta pagina


transparencia = 0
naoTransparencia = 0
naofuncionando = 0
naoInteressante = 0
getfilename = True

with io.open("keywords\OGD.txt", "rt", newline="", encoding="UTF-8") as key:
    keywords = key.readlines()
    key.close()

with fileinput.input() as file:
    for item in file:
        line = item.replace("\n","")
        if getfilename:
            nombre = fileinput.filename()  # variável com o nome do arquivo (OUTPUT)
            nombre = str(nombre).replace(".txt","")
            getfilename = False
        html = urlok(line)
        if html != 1 and html != 2:
            try:
                b = soupfinder(line, html)
                if b == 0:
                    transparencia += 1
                elif b == 1:
                    naoTransparencia += 1
            except:
                with open("%s_SoupError.txt" %nombre, "a", newline="", encoding="UTF-8") as n_luck:
                    n_luck.write(str(line) + "\n")
                    n_luck.close()
        elif html == 2:
            naoInteressante += 1
            with open("%s_naoInteressante.txt" %nombre, "a", newline="", encoding="UTF-8") as f:
                f.write(str(line) + "\r\n")
                f.close()
            continue
        else:
            naofuncionando += 1
            with open("%s_naoFuncionando.txt" %nombre, "a", newline="", encoding="UTF-8") as g:
                g.write(str(line) + "\r\n")
                g.close()
            continue

with open("%s_transparencia-resultados.txt" %nombre, "a", newline="", encoding="UTF-8") as final:
    final.write(str(transparencia) + " Transparencia\r\n")
    final.write(str(naoTransparencia) + " Nao Transparencia\r\n")
    final.write(str(naofuncionando) + " Nao Funcionando\r\n")
    final.write(str(naoInteressante) + " Nao Interessante\r\n")
    final.write(str(transparencia+naoInteressante+naoTransparencia+naofuncionando) + " SOMA\r\n")
    final.close()