from SPARQLWrapper import SPARQLWrapper, BASIC
from rdflib import Graph, URIRef, Literal, RDFS
from rdflib.namespace import RDF
import json
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

def jsonakKargatu():
#In: -
#Out: JSONak kargatuta
    global artikuluak,dokumentuak,entitateak,ekitaldiak,pertsonak,lekuak,erlazioak,iturriak

    with open("./data/ladonacion.es/articles.json","r") as a:
        artikuluak = json.load(a)

    with open("./data/ladonacion.es/documents.json","r") as d:
        dokumentuak = json.load(d)

    with open("./data/ladonacion.es/entities.json","r") as e:
        entitateak = json.load(e)

    with open("./data/ladonacion.es/events.json","r") as ek:
        ekitaldiak = json.load(ek)

    with open("./data/ladonacion.es/persons.json","r") as pe:
        pertsonak = json.load(pe)

    with open("./data/ladonacion.es/places.json","r") as pl:
        lekuak = json.load(pl)

    with open("./data/ladonacion.es/relations.json","r") as re:
        erlazioak = json.load(re)

    with open("./data/ladonacion.es/sources.json","r") as so:
        iturriak = json.load(so)

def setType(uri,typeUrl):
#In: Objektu bati esleitutako URIa / Zein motatako objektua den (pertsona, lekua,...)
#Out: Grafoan objektu horren rdfs:type-aren triplea sartu
    global grafo

    triple = (uri,RDF.type,typeUrl)
    grafo.add(triple)

def setLabel(uri,json,tipoa):
#In: Objektu bati esleitutako URIa / Zein JSONean bilatu behar da informazioa /Zein motatako objektua den (pertsona, lekua,...)
#Out: Grafoan objektu horren rdfs:label-aren triplea sartu
    global grafo

    label = ""
    for i in json[tipoa]:
        if i["id"] == uri.split("/")[-1]:
            label = i["title"]
            break
    triple = (uri,RDFS.label,Literal(label))
    grafo.add(triple)

def setComent(uri,json,tipoa):
# In: Objektu bati esleitutako URIa / Zein JSONean bilatu behar da informazioa /Zein motatako objektua den (pertsona, lekua,...)
# Out: Grafoan objektu horren rdfs:comment-aren triplea sartu
    global grafo
    for i in json[tipoa]:
        if i["id"] == uri.split("/")[-1]:
            if("description" in i.keys()): #Elementu batzuk ez daukate "description" giltza
                comment = i["description"]
                triple = (uri, RDFS.comment, Literal(comment))
                grafo.add(triple)
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
    global grafo, uri_base

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
            grafo.add(triple)

def grafoaEraiki():
#In: -
#Out: Dauden artikuluekin sortutako grafoa
    global grafo, artikuluak,dokumentuak

    for i in artikuluak["articles"]: #Artikuluen artean iteratzeko
        tripleakSortu(i)

    for i in dokumentuak["documents"]:
        tripleakSortu(i)

    grafo.serialize(destination ="./data/ladonacion.es/grafoa.nt", format ="nt")

def zerbitzariraIgo():
#In: -
#Out: Aurretik sortutako fitxategia zerbitzariaren Graphdb instantziara igo
    global grafo

    '''
    datuak = "/data/ladonacion.es/grafoa.nt"
    base_url = "http://localhost:7200"
    repo_id = "Froga"

    eskaera = "curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{fileNames:[" + datuak + "]}' "+base_url+"/rest/data/import/server/"+repo_id
    print(eskaera)
    os.system(eskaera)
    '''

    graphdb_url = "http://localhost:7200/repositories/Froga/statements"
    #graphdb_url = "http://158.227.69.119:7200/repositories/laDonacion/statements"
    for s,p,o in grafo:
        queryStringUpload = 'INSERT DATA {%s,%s,%s}' %(s,p,o)

        print(queryStringUpload)
        sparql = SPARQLWrapper(graphdb_url)
        sparql.setQuery(queryStringUpload)
        sparql.setMethod('POST')
        sparql.setHTTPAuth(BASIC)
        sparql.setCredentials('login', 'password')

        #try:
        ret = sparql.query()
        #except:
            #print("Ha fallado")


        



#Main metodoa
if __name__ == "__main__":
    print("JSONak kargatuko dira...")
    jsonakKargatu()

    print("Grafoa eraikiko da...")
    grafoaEraiki()

    print("Sortutako fitxategia zerbitzariaren graphdb instantziara igoko da...")
    #zerbitzariraIgo()

