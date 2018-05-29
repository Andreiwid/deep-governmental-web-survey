import re
import fileinput

qtd_paginas = 0
busca = 0
requisicao = 0
cadastro = 0
getfilename = True

with fileinput.input() as file:
    for line in file:
        if getfilename:
            nome = fileinput.filename()
            nome = str(nome).replace("-pronto_transparenciapaginaToda_forms_resultados_links_forms_usuario.csv", "")
            getfilename = False
        line = line.replace("\r","")
        line = line.replace("\n", "")
        if re.match('2', line, re.IGNORECASE):
            qtd_paginas += 1
            a = line.split(',')
            if a[2] != '0':  # busca
                busca += 1
            if a[3] != '0':  # requisicao
                requisicao += 1
            if a[4] != '0':  # cadastro
                cadastro += 1
    file.close()

with open("somaform/%s.txt" %nome, "a", newline="", encoding="UTF-8") as final:
    final.write(str(qtd_paginas) + ' Páginas com forms\r\n')
    final.write(str(busca) + ' Páginas com forms BUSCA\r\n')
    final.write(str(requisicao) + ' Páginas com forms REQUISICAO\r\n')
    final.write(str(cadastro) + ' Páginas com forms CADASTRO\r\n')
    final.close()