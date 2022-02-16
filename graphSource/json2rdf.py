from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF
import json
import Sinpleak
import Erlaziodunak

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

#Grafoa
g = Graph()
g.bind("foaf",FOAF)

#Miscelanea
uri_base = "http://ehu.eus/"
tuplak = []


def jsonakKargatu():#JSONak kargatu
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


def tuplakSortu(i):
#In: Dokumentu bat
#Out: Dokumentu horren erlazio guztiak grafoan sartu
    global tuplak,g, uri_base

    for j in i["relations"]:  # Artikulu bakoitzak dauzkan erlazioak
        a = URIRef(uri_base + j["subject"].split("/")[1] + "/" + j["subject"].split("/")[2])  # Subjektua
        b = URIRef(uri_base + j["type"].split("/")[1] + "/" + j["type"].split("/")[2])  # Predikatua
        c = URIRef(uri_base + j["object"].split("/")[1] + "/" + j["object"].split("/")[2])  # Objektua
        print("A: " + str(a))
        print("B: " + str(b))
        print("C: " + str(c))
        tupla = (a, b, c)
        if (tupla not in tuplak):  # Tuplak ez bikoizteko
            g.add((a, b, c))

def grafoaEraiki():
#In: -
#Out: Dauden artikuluekin sortutako grafoa
    global g, artikuluak,dokumentuak #,entitateak,ekitaldiak,pertsonak,lekuak,erlazioak,iturriak

    for i in artikuluak["articles"]: #Artikuluen artean iteratzeko
        tuplakSortu(i)

    for i in dokumentuak["documents"]:
        tuplakSortu(i)

    g.serialize(destination = "./data/ladonacion.es/grafoa.nt", format = "nt")



#Main metodoa
if __name__ == "__main__":
    print("JSONak kargatuko dira")
    jsonakKargatu()

    print("Grafoa eraikiko da")
    grafoaEraiki()

