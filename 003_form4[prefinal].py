import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import fileinput

def urlok(endereco):
    try:
        html = urlopen(endereco)
        teste = str(html.info())
        validacaoHTML = 'Content-Type: text/html'
        if re.search(validacaoHTML, teste, re.IGNORECASE):
            return html
        else:
            return 1
    except:
        return 1


def findTag(page, url):
    global get
    global post
    global qtdforms
    global paginasemform
    global paginascomform
    global sem_metodo

    global nome
    global cadastro
    global busca
    global requisicao
    global seminput

    print(str(datetime.datetime.now()) + " FindTag " + url)
    form_1input = 0
    form_mais1input = 0
    form_password = 0
    m_get = 'method="GET"'
    m_post = 'method="POST"'
    bsObj = BeautifulSoup(page.read(), "lxml")
    type_password = 'type="password"'
    hidden = 'class="hidden"'
    lista_nao = ['type="hidden"', 'type="submit"', 'type="image"', 'type="button"', 'type="radio"', 'type="checkbox"', 'type="color"', 'type="file"', 'type="reset"']
    lista_sim = ['type="text"','type="search"', 'type="date"', 'type="datetime-local"', 'type="email"', 'type="month"', 'type="number"', 'type="range"', 'type="time"', 'type="url"', 'type="week"', 'type="textbox"', 'type="txtbusca"', 'type="tel"']

    formSet = bsObj.find_all(name='form')
    if not formSet:
        paginasemform += 1
        with open("%s_sem_forms.txt" % nome, "a", newline="", encoding="UTF-8") as no_form:
            no_form.write((url) + "\n")
            no_form.close()
    else:
        paginascomform += 1
        forms_usuario = len(formSet)
        for child in formSet: # para cada FORM
            if child.find(text=re.compile(hidden, re.IGNORECASE)):  # form hidden
                continue  # 'class="hidden"'
            campos = 0
            cadastrobool = False
            cba = child.find_all("textarea")
            if cba:
                campos += len(cba)
            for campo in child.find_all("input"):
                field = str(campo)
                if re.search(type_password, field, re.IGNORECASE):
                    cadastrobool = True
                    campos += 1
                    break  # proximo formulario... Esse é cadastro
                elif 'type=' not in field or 'type=""' in field:
                    campos += 1
                else:
                    pareNao = False
                    for item in lista_nao:
                        if re.search(item, field, re.IGNORECASE):
                            pareNao = True
                            break
                    if pareNao:
                        continue
                    pareSim = False
                    for item in lista_sim:
                        if re.search(item, field, re.IGNORECASE):
                            campos += 1
                            pareSim = True
                            break
                    if pareSim:
                       continue
                    if not pareSim and not pareNao:
                        with open("%s_forms_nao-escopo.txt" %nome, "a", newline="", encoding="UTF-8") as erro:
                            log = str(datetime.datetime.now())
                            erro.write(log+"\n"+str(url)+"\n"+field+"\n\n")
                            erro.close()

            abc = child.find_all("select")  # busca dentro de todos os filhos dos filhos dos filhos...
            if abc:
                campos += len(abc)

            if cadastrobool:
                cadastro += 1
                form_password += 1
            elif campos == 1:
                busca += 1
                form_1input += 1
            elif campos > 1:
                requisicao += 1
                form_mais1input += 1
            else:  # campos == 0:
                seminput += 1
                forms_usuario -= 1

            if campos > 0:  # só busca métodos nos forms pro usuário  # por causa do cadastro
                qtdforms += 1  # mais um form disponível ao usuário
                akla = str(child)
                if re.search(m_post, akla, re.IGNORECASE):  # método POST  # return NONE
                    post += 1
                elif re.search(m_get, akla, re.IGNORECASE):  # método GET  # return NONE
                    get += 1
                else:
                    sem_metodo += 1

        if form_1input !=0 or form_mais1input != 0 or form_password != 0:
            with open("%s_forms_resultados_links_forms_usuario.txt" % nome, "a", newline="", encoding="UTF-8") as formulario:
                logme = str(datetime.datetime.now())
                formulario.write(logme + " • " + str(forms_usuario) + " Forms: ["+str(form_1input)+"] •• ["+str(form_mais1input)+"] ••• ["+str(form_password)+"]\n" + str(url) + "\n\n")
                formulario.close()
            with open('%s_forms_resultados_links_forms_usuario.csv' % nome, 'a', newline='', encoding="UTF-8") as csvf:
                spamwriter = csv.writer(csvf)
                spamwriter.writerow([str(url)])
                spamwriter.writerow([logme, str(forms_usuario), str(form_1input), str(form_mais1input), str(form_password)])

sem_metodo = 0  # FORM disponível ao usuário sem método de envio
get = 0 # FORM disponível ao usuário, a quantidade total dos que apresentam método de envio como GET
post = 0 # FORM disponível ao usuário, a quantidade total dos que apresentam método de envio como POST
qtdforms = 0 # quantidade total de FORMS disponíveis ao usuário encontrados no TXT
cadastro = 0 # total de forms que foram classificados como cadastro // contém INPUT PASSWORD
busca = 0 # total de forms que foram classificados como busca de dados // contém apenas 1 campo de SEARCH ou TEXT para o usuário interagir
requisicao = 0 # total de forms que foram classificados como requisicao de dados // contém mais de um campo para o usuario interagir e nenhum deles é PASSWORD
seminput = 0 # total de forms que nao apresentam campos para o usuario interagir
analisados = 0 # total de paginas que foram analisadas por este algoritmo de cada arquivo txt
paginascomform = 0  # total de paginas na lista dos possiveis dados de transparencia com tags forms para o usuário
paginasemform = 0 # total de paginas na lista dos possiveis dados de transparencia sem tags form
getfilename = True

with fileinput.input() as portalDados:
    for portal in portalDados:
        if getfilename:
            nome = fileinput.filename()  # variável com o nome do arquivo (OUTPUT)
            nome = str(nome).replace(".txt", "")
            getfilename = False
        link = str(portal)
        link = link.replace("\r", "")
        link = link.replace("\n", "")        
        html = urlok(link)
        if html != 1:
            findTag(html, link)
            analisados += 1
        else:
            print('URLOK 1')
    portalDados.close()

with open("%s_forms_resultados.txt" %nome, "a", newline="", encoding="UTF-8") as final:
    final.write(str(get) + " GET (p/usuario)\r\n")
    final.write(str(post) + " POST (p/usuario)\r\n")
    final.write(str(sem_metodo) + " sem_metodo (p/usuario)\r\n")
    final.write(str(qtdforms) + " Qtd_Forms (p/usuario)\r\n")
    final.write(str(cadastro) + " cadastro (password)\r\n")
    final.write(str(busca) + " busca (1 input)\r\n")
    final.write(str(requisicao) + " requisicao (+1 input)\r\n")
    final.write(str(seminput) + " sem input (n/ usuario)\r\n")
    final.write(str(analisados) + " links analisados\r\n")  # analisado HTML (URL OK)
    final.write(str(paginascomform) + " paginas com form (1 pagina n forms)\r\n")
    final.write(str(paginasemform) + " paginas sem form\r\n")
    final.close()