import re
import fileinput

def rreplace(s, old, new, occurrence):
    n = s.rsplit(old, occurrence)
    return new.join(n)


getfilename = True
for line in fileinput.input():
    if getfilename:
        b = fileinput.filename()
        b = str(b).replace(".txt","")
        getfilename = False
    temp = str(line)
    aux = re.findall(r'(https?://\S+)', line)
    for line in aux:
        link = str(line)
        if link.endswith(":"):
            sizeof = len(link)
            quantos = link.count(':')
            if quantos >= 2:
                link = rreplace(link, ":", "", link.count(':') - (quantos - 1))
        with open("%s_clean.txt" %b, "a", newline="", encoding="UTF-8") as linklimpo:
            linklimpo.write(line+"\n")
            linklimpo.close()
