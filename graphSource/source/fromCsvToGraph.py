import logging
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, RDFS
from rdflib.namespace import RDF
import os
import unidecode
import sys
from csv import reader


class FromCsvToGraph:

    def __init__(self):
        #CSVak
        self.helbideak = ""
        self.entitateak = ""
        self.bitartekariak = ""
        self.ofizialak = ""
        self.bestelakoak = ""
        self.erlazioak = ""

        #URIak
        self.uri_base = 'http://ehu.eus/'
        self.per = URIRef('https://schema.org/Person')
        self.ekit = URIRef('https://schema.org/Event')
        self.doku = URIRef('https://schema.org/Documentation')
        self.leku = URIRef('https://schema.org/Place')
        self.enti = URIRef('https://schema.org/Organization')
        self.arti = URIRef('https://schema.org/NewsArticle')

        self.grafo = Graph()

        if not '/home/runner/work/' in os.path.dirname(os.path.abspath(__file__)):
            logging.basicConfig(filename = '/home/jonander/PycharmProjects/TFG-KG-RelacionesClientelares/logs/unekoLog.log', filemode = 'w', level = logging.DEBUG)
        self.data = '/home/jonander/PycharmProjects/TFG-KG-RelacionesClientelares/data/leaks'
        self.triple_store = 'http://localhost:7200/repositories/LaDonacion'

        uriTest = self.triple_store.split("/")[:len(self.triple_store.split("/")) - 1]
        self.testTripleStore = ""
        for i in uriTest:
            self.testTripleStore += i + "/"
        self.testTripleStore = self.testTripleStore[:len(self.testTripleStore) - 1]

    def csvakKargatu(self):
    #In: -
    #Out: CSVak kargatuta
        try:
            with open(self.data + '/nodes-addresses.csv') as helb:
                self.helbideak = reader(helb)
        except:
            logging.error('Helbideen CSVa ez da kargatu, programaren exekuzioa bukatuko da...\n')
            sys.exit(1)

        try:
            with open(self.data + '/nodes-entities.csv') as enti:
                self.entitateak = reader(enti)
        except:
            logging.error('Entitateen CSVa ez da kargatu, programaren exekuzioa bukatuko da...\n')
            sys.exit(1)

        try:
            with open(self.data + '/nodes-intermediaries.csv') as bit:
                self.bitartekariak = reader(bit)
        except:
            logging.error('Bitartekarien CSVa ez da kargatu, programaren exekuzioa bukatuko da...\n')
            sys.exit(1)

        try:
            with open(self.data + '/nodes-officers.csv') as of:
                self.ofizialak = reader(of)
        except:
            logging.error('Ofizialen CSVa ez da kargatu, programaren exekuzioa bukatuko da...\n')
            sys.exit(1)

        try:
            with open(self.data + '/nodes-others.csv') as best:
                self.bestelakoak = reader(best)
        except:
            logging.error('Bestelakoen CSVa ez da kargatu, programaren exekuzioa bukatuko da...\n')
            sys.exit(1)

        try:
            with open(self.data + '/nodes-relationships.csv') as erl:
                self.erlazioak = reader(erl)
        except:
            logging.error('Erlazioen CSVa ez da kargatu, programaren exekuzioa bukatuko da...\n')
            sys.exit(1)

    def setLabel(self,csv):
        for lerro in csv:
            triple = (self.uri_base + '/' + lerro[0], RDFS.label, Literal(lerro[2]))
            logging.info("Sartutako triplea hurrengoa da...\n" + str(triple) + '\n')
            self.grafo.add(triple)

    def setType(self,csv):
        for lerro in csv:
            type = ''
            if (int(lerro[0]) % 1000000 == 1): #Entitate bat da
                type = self.enti
            elif int(lerro[0]) % 100000 == 24:
                type = self.leku
            else:
                type = self.per

            triple = (self.uri_base + '/' + lerro[0], RDF.type, type)
            logging.info("Sartutako triplea hurrengoa da...\n" + str(triple) + '\n')
            self.grafo.add(triple)

    def getErlazioa(self,erlazioa):
        schema = 'https://schema.org/'
        erlazioPropioa = 'http://ehu.eus/transparentrelations#'

    def erlazioakAtera(self):
        for lerro in self.erlazioak:
            erlazioa = self.getErlazioa(lerro[3])
            triple = (self.uri_base + '/' + lerro[0], URIRef(erlazioa), self.uri_base + '/' + lerro[1])
            logging.info("Sartutako triplea hurrengoa da...\n" + str(triple) + '\n')
            self.grafo.add(triple)

    def main(self):
        #CSVak kargatu
        self.csvakKargatu()

        #Labelak ezarri
        self.setLabel(self.helbideak)
        self.setLabel(self.entitateak)
        self.setLabel(self.ofizialak)
        self.setLabel(self.bitartekariak)
        self.setLabel(self.bestelakoak)

        #Typeak ezarri
        self.setType(self.helbideak)
        self.setType(self.entitateak)
        self.setType(self.ofizialak)
        self.setType(self.bitartekariak)
        self.setType(self.bestelakoak)

        #Erlazioak ezarri
        self.erlazioakAtera()