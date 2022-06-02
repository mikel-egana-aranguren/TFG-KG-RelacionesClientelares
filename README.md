# TFG-KG-RelacionesClientelares - Tutoriala


## Egilea:

Jon Ander Asua \
![jonan_bateria](https://img.shields.io/twitter/follow/jonan_bateria?style=social)
![JonAnderAsua](https://img.shields.io/github/followers/JonAnderAsua?style=social)


## Aurkibidea

- [Informazio orokorra](#informazio-orokorra)
- [Erabilitako teknologiak](#erabilitako-teknologiak)
- [Aurrebaldintzak](#aurrebaldintzak)
- [YAML fitxategiaren konfigurazioa](#yaml-fitxategiaren-konfigurazioa) 
- [Dependentzien instalazioa](#dependentzien-instalazioa)
- [Programaren exekuzioa](#programaren-exekuzioa)

## Informazio orokorra
README honetan programa hau nola konfiguratzen eta exekutatzen den azaltzen da. Programa honek parametro batzuk pasatu ostean era automatiko batean eta _SPARQL_ eskaeri esker datu multzo bat _triple store_ batera igotzen du. Adibide bezala 'la_donacion' proiektua hartu da.

## Erabilitako teknologiak
- Python >= 3.7
- Docker 20.10.7

## Aurrebaldintzak

Programaren exekuzioarekin hasi baino lehen hurrengo aurrebaldintzak betetzen direla kontuan hartuko da:

- Graphdb instantzia bat martxan edukitzea. Honetarako jarraitu _Graphdb_ berak daukan [tutoriala](https://graphdb.ontotext.com/documentation/free/free/run-desktop-installation.html).
- Programa exekutatu nahi den terminalean Python interpretatzaile bat instalatuta izatea (gutxienez 3.7 bertsioa).
- Terminalean proiektu hau klonatuta edukitzea, horretarako exekutatu hurrengo komandoa terminalean:
```bash
git clone -b develop https://github.com/mikel-egana-aranguren/TFG-KG-RelacionesClientelares
```
## YAML fitxategiaren konfigurazioa

Behin aurrebaldintza guztiak bete direnean konfigurazioaren hasi ahal da. Horretarako [YAML fitxategi bat](https://github.com/mikel-egana-aranguren/TFG-KG-RelacionesClientelares/blob/develop/doc/config.yml) aurkitzen da *doc* karpetaren barnean hurrengo parametroekin:

- _project_name_: Proiektuaren izena.
- _data_source_: Erabili beharreko datuen _path-a_.
- _validate_: Datuen balioztasuna bermatzen duen testen _path-a_.
- _named_graph_: Datuak GraphDB barnean egongo diren taldea adierazten duen URIa.
- _run_: Exekutatu nahi den programaren _path-a_. Programa hau _SPARQL_ eskaeren bitartez _triple_store_ aldagaian deklaratutako _triple storean_ datuak igotzeko gaitasuna izan behar du.
- _metadata_file_: Metadatuen _path-a_.
- _delete_graph_: Aurretik _triple store-an_ zegoen grafoa ezabatu nahi den ala ez.
- _triple_store_: Tripleak igo nahi diren _triple storearen_ URIa, ez da beharrezkoa GraphDb instantzia baten URI bat izatea, hau da, SPARQL eskaerak onartzen dituen instantzia baten URIa jarri behar da. 
- _logs_: Programa exekutatzerako orduan sortutako logak non gorde nahi diren _path-a_.
- _rdf_output_: Tripleekin bete nahi den fitxategiaren _path-a_.

_la_donacion_ proiektuaren kasuan hurrengo konfigurazioa jarri da: 
```yaml
 la_donacion: 
    project_name: 'la_donacion_local_JonAnder' 
    data_source: ./data/ladonacion.es 
    validate: ./graphSource/tests/TestJson2rdf.py 
    named_graph: http://ehu.eus/ 
    run: ./procesSource/source/json2rdf.py 
    metadata_file: ./metadata.ttl 
    delete_graph: true 
    triple_store: http://localhost:7200/repositories/LaDonacion/statements 
    logs: ./logs/laDonacion.log 
    rdf_output: ./data/ladonacion.es/graphLaDonacion.nt 
```

## Dependentzien instalazioa
Programa exekutatu baino lehen programaren dependentziak instalatu behar dira, horretarako hurrengo komandoak exekutatu behar dira proiektuko fitxategi nagusitik:
```bash
pip install -r requirements.txt
pip install -e .
```
Lehenengo komandoarekin _requirements.txt_ fitxategiaren barnean adierazitako moduluak instalatuko dira. Aldiz, bigarrenean, modulu lokalak instalatzen dira.
## Programaren exekuzioa 

Programa exekutatu ahal izateko fitxategi nagusian kokatuta hurrengo komandoa exekutatu behar da:
```bash
python3 /procesSource/source/ejecutador.py [sortutako proiektuaren izena]
```

Adibidearen kasuan komandoa hurrengoa izango litzateke:
```bash
python3 /procesSource/source/ejecutador.py la_donacion
```

**Sartutako proiektua ez bada existitzen programa berak argitaratuko ditu eskuragarri dauden proiektuen izenak.**
