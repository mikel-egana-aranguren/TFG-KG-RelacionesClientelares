import logging

from SPARQLWrapper import SPARQLWrapper, BASIC, INSERT, POST, JSON
from rdflib import Graph, URIRef, Literal, RDFS
from rdflib.namespace import RDF
import json
import re
import os

#Elementuen hasieraketa
#JSONak
artikuluak = ""
dokumentuak = ""
entitateak = ""
ekitaldiak = ""
pertsonak = ""
lekuak = ""
erlazioak = ""
iturriak = ""

#URIak
uri_base = "http://ehu.eus/"
per = URIRef("https://schema.org/Person")
ekit = URIRef("https://schema.org/Event")
doku = URIRef("https://schema.org/Documentation")
leku = URIRef("https://schema.org/Place")
enti = URIRef("https://schema.org/Organization")
arti = URIRef("https://schema.org/NewsArticle")

#Grafoa
grafo = Graph()

#Log
logging.basicConfig(filename='./logs/log.log', filemode='w', level=logging.DEBUG)

def getPath():
#In: -
#Out: Fitxategian dauden path-a
    cwd = os.getcwd()
    if "test" in cwd: #Test
        cwd = cwd.split("/")[0:-2]
    else:
        cwd = cwd.split("/")[0:-2]

    path = ""
    for i in cwd:
        path += "/" + i
    return path

def jsonakKargatu():
#In: -
#Out: JSONak kargatuta
    global artikuluak,dokumentuak,entitateak,ekitaldiak,pertsonak,lekuak,erlazioak,iturriak

    path = getPath()
    try:
        with open(path + "/data/ladonacion.es/articles.json","r") as a:
            artikuluak = json.load(a)
            logging.info("Artikuluen JSONa kargatu da...\n")
    except:
        logging.error("Artikuluen JSONa ez da kargatu...\n")

    try:
        with open(path + "/data/ladonacion.es/documents.json","r") as d:
            dokumentuak = json.load(d)
            logging.info("Dokumentuen JSONa kargatu da...\n")
    except:
        logging.error("Dokumentuen JSONa ez da kargatu...\n")

    try:
        with open(path + "/data/ladonacion.es/entities.json","r") as e:
            entitateak = json.load(e)
            logging.info("Entitateen JSONa kargatu da...\n")
    except:
        logging.error("Entitateen JSONa ez da kargatu...\n")

    try:
        with open(path + "/data/ladonacion.es/events.json","r") as ek:
            ekitaldiak = json.load(ek)
            logging.info("Ekitaldien JSONa kargatu da...\n")
    except:
        logging.error("Ekitaldien JSONa ez da kargatu...\n")

    try:
        with open(path + "/data/ladonacion.es/persons.json","r") as pe:
            pertsonak = json.load(pe)
            logging.info("Pertsonen JSONa kargatu da...\n")
    except:
        logging.error("Pertsonen JSONa ez da kargatu...\n")

    try:
        with open(path + "/data/ladonacion.es/places.json","r") as pl:
            lekuak = json.load(pl)
            logging.info("Lekuen JSONa kargatu da...\n")
    except:
        logging.error("Lekuen JSONa ez da kargatu...\n")

    try:
        with open(path + "/data/ladonacion.es/relations.json","r") as re:
            erlazioak = json.load(re)
            logging.info("Erlazioen JSONa kargatu da...\n")
    except:
        logging.error("Erlazioen JSONa ez da kargatu...\n")

    try:
        with open(path + "/data/ladonacion.es/sources.json","r") as so:
            iturriak = json.load(so)
            logging.info("Iturrien JSONa kargatu da")
    except:
        logging.error("Iturrien JSONa ez da kargatu")

def filtroaPasatu(comment): #https://www.delftstack.com/es/howto/python/remove-special-characters-from-string-python/
#In: String bat
#Out: String hori baina karaktere okultorik gabe
    return re.sub(r"[^a-zA-Z0-9]"," ",comment)

def setType(uri,typeUrl):
#In: Objektu bati esleitutako URIa / Zein motatako objektua den (pertsona, lekua,...)
#Out: Grafoan objektu horren rdfs:type-aren triplea sartu
    global grafo,logging

    triple = (uri,RDF.type,typeUrl)
    logging.info("Sartuko den triplea hurrengoa da...\n" + str(triple) + "\n")
    grafo.add(triple)

def setLabel(uri,json,tipoa):
#In: Objektu bati esleitutako URIa / Zein JSONean bilatu behar da informazioa /Zein motatako objektua den (pertsona, lekua,...)
#Out: Grafoan objektu horren rdfs:label-aren triplea sartu
    global grafo,logging

    label = ""
    for i in json[tipoa]:
        if i["id"] == uri.split("/")[-1]:
            label = filtroaPasatu(i["title"])
            break
    triple = (uri,RDFS.label,Literal(label))
    logging.info("Sartuko den triplea hurrengoa da...\n" + str(triple) + "\n")
    grafo.add(triple)

def setComent(uri,json,tipoa):
# In: Objektu bati esleitutako URIa / Zein JSONean bilatu behar da informazioa /Zein motatako objektua den (pertsona, lekua,...)
# Out: Grafoan objektu horren rdfs:comment-aren triplea sartu
    global grafo,logging
    for i in json[tipoa]:
        if i["id"] == uri.split("/")[-1]:
            if("description" in i.keys()): #Elementu batzuk ez daukate "description" giltza
                comment = i["description"]
                comment = filtroaPasatu(str(comment))
                triple = (uri, RDFS.comment, Literal(comment))
                grafo.add(triple)
                logging.info("Sartuko den triplea hurrengoa da...\n" + str(triple) + "\n")
                break



def setTypeLabelComent(uri, tipoa): # https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html
#In: Objektu bati esleitutako URIa / Zein motatako objektua den (pertsona, lekua,...)
#Out: Grafoan rdfs:type,label eta comment sartu
    global per, ekit, doku, leku, enti, arti,grafo , entitateak,ekitaldiak,pertsonak,lekuak,erlazioak,iturriak, dokumentuak, artikuluak

    #Defektuz pertsona bat bezala hartuko da
    typeUrl = per #Defektuz pertsonen JSONa hartuko da
    json = pertsonak

    if(tipoa == "events"):
        typeUrl = ekit
        json = ekitaldiak
    elif(tipoa == "documents"):
        typeUrl = doku
        json = dokumentuak
    elif(tipoa == "places"):
        typeUrl = leku
        json = lekuak
    elif(tipoa == "entities"):
        typeUrl = enti
        json = entitateak
    elif(tipoa == "articles"):
        typeUrl = arti
        json = artikuluak

    setType(uri,typeUrl)
    setLabel(uri,json,tipoa)
    setComent(uri,json,tipoa)



def forPersonsToPeople(tipoa):
#In: String bat adierazten zein motatako objektua den (place, persons,...)
#Out: String-a "persons" bada "people" bueltatzen du, bestela string bera

    if tipoa == "persons":
        return "people"
    else:
        return tipoa

def erlazioaAldatu(erlazioa):
#In: Erlazioaren URIren azkenengo zatia
#Out: URI hori aldatuta

    #URIak deklaratu
    schema = "https://schema.org/"
    erlazioPropioa = "http://ehu.eus/transparentrelations#"

    #Schema + kasu nabariak
    if erlazioa == "takes_part":
        emaitza = schema + "participant"
    elif erlazioa == "authors":
        emaitza = schema + "author"
    elif erlazioa == "works_for":
        emaitza = schema + "worksFor"

    #Schema + kasu orokorrak
    elif(erlazioa == "mentions" or erlazioa == "parent" or erlazioa == "owns" or erlazioa == "spouse" or erlazioa == "knows"):
        emaitza = schema + erlazioa

    #Lag + kasu orokorrak
    else:
        emaitza = erlazioPropioa + erlazioa

    return emaitza

def subjektuaObjektuaTratatu(uri):
#In:
#Out:
    global uri_base

    tipoa = uri.split("/")[1]
    if tipoa == "entities": tipoa = "entitys"  # Hecha la trampa por que el singular de entities es entity
    entitate = URIRef(uri_base + "id/" + tipoa[0:len(tipoa) - 1] + "/" + uri.split("/")[2])
    setTypeLabelComent(entitate, uri.split("/")[1])
    return entitate

def tripleakSortu(i):
#In: Dokumentu bat
#Out: Dokumentu horren erlazio guztiak grafoan sartu
    global grafo, uri_base, logging

    aldatu = False

    for j in i["relations"]:  # Artikulu/dokumentu bakoitzak dauzkan erlazioak atera

        #Subjektua
        subjektu = subjektuaObjektuaTratatu(j["subject"])

        #Predikatua
        erlazioa = erlazioaAldatu((uri_base +"prop/" + j["type"].split("/")[2]).split("/")[-1])
        predikatu = URIRef(erlazioa)
        if("author" in erlazioa): #Aldatu behar da triplearen ordena
            aldatu = True

        #Objektua
        objektu = subjektuaObjektuaTratatu(j["object"])

        #Triplea sortu eta grafoan ez badago sartu
        if(aldatu):
            triple = (objektu,predikatu,subjektu)
        else:
            triple = (subjektu, predikatu, objektu)

        if ("mohamed_vi" not in subjektu and "gives" not in predikatu and "marrakech" not in objektu):  # Tripleak ez bikoizteko
            logging.info("Sartuko den triplea hurrengoa da...\n" + str(triple) + "\n")
            grafo.add(triple)

def grafoaEraiki():
#In: -
#Out: Dauden artikuluekin sortutako grafoa
    global grafo, artikuluak,dokumentuak,logging

    logging.info("Artikuluen tripleak sortuko dira...\n")
    for i in artikuluak["articles"]: #Artikuluen artean iteratzeko
        logging.info("Hurrengo artikulua kudeatujo da...\n" + str(i) + "\n")
        tripleakSortu(i)


    logging.info("Dokumentuen tripleak sortuko dira...\n")
    for i in dokumentuak["documents"]:
        tripleakSortu(i)

    grafo.serialize(destination = getPath() + "/data/ladonacion.es/grafoa.nt", format ="nt")

def zerbitzariraIgo():
#In: -
#Out: Aurretik sortutako fitxategia zerbitzariaren Graphdb instantziara igo
    global grafo

    graphdb_url = "http://localhost:7200/repositories/LaDonacion/statements"
    #graphdb_url = "http://158.227.69.119:7200/repositories/laDonacion/statements"
    for s,p,o in grafo:
        if("http://ehu.eus" in o or "https://schema.org" in o):
            queryStringUpload = 'INSERT DATA  { <%s> <%s> <%s> }' %(s,p,o)
        else:
            queryStringUpload = 'INSERT DATA  { <%s> <%s> "%s" }' % (s, p, o)
        sparql = SPARQLWrapper(graphdb_url)
        sparql.setQuery(queryStringUpload)
        sparql.queryType = INSERT
        sparql.method = POST
        sparql.setHTTPAuth(BASIC)

        try:
            ret = sparql.query()
        except:
            logging.error("Ezin izan da " + str((s, p, o)) + " triplea grafoan sartu...\n")


# Testearako metodoak

def getGrafoa():
    # In: -
    # Out: Proiektu honen grafoa
    global grafo
    return grafo


def getJsonak():
    # In: -
    # Out: Proiektuaren JSONak
    global artikuluak, dokumentuak, entitateak, ekitaldiak, pertsonak, lekuak, erlazioak, iturriak
    return [artikuluak, dokumentuak, entitateak, ekitaldiak, pertsonak, lekuak, erlazioak, iturriak]


def getLabelFromGraph(id):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/LaDonacion")

    sparql.setQuery('''
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?label
                WHERE
                {
                    <%s> rdfs:label ?label .
                }           
                ''' % (id))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings'][0]["label"]['value']


def getCommentFromGraph(id):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/LaDonacion")

    sparql.setQuery('''
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?comment
                WHERE
                {
                    <%s> rdfs:comment ?comment .
                }           
                ''' % (id))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings'][0]["comment"]['value']


def getTypeFromGraph(id):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/LaDonacion")

    sparql.setQuery('''
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?type
                WHERE
                {
                    <%s> rdf:type ?type .
                }           
                ''' % (id))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings'][0]["type"]['value']


#Main metodoa
if __name__ == "__main__":

    logging.info("JSONak kargatuko dira...\n")
    jsonakKargatu()

    logging.info("Grafoa eraikiko da...\n")
    grafoaEraiki()

    logging.info("Sortutako fitxategia zerbitzariaren graphdb instantziara igoko da...\n")
    zerbitzariraIgo()

