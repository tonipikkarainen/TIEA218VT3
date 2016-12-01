#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgitb
# seuraava rivi aktivoi cgitb-kirjaston, joka osaa heittää virheilmoitukset www-sivulle
# näkyville. Ilman tätä virheet menevät www-palvelimen lokiin jonne ei tavallisella
# käyttäjällä ole pääsyä
# Jos testaa ohjelmaa komentoriviltä niin seuraava rivi kannattaa kommentoida pois käytöstä
cgitb.enable()
import cgi
import os
import urllib
from jinja2 import Template, Environment, FileSystemLoader

# antaa polun alikansiossa olevaan jinja.html-tiedostoon:
# ei tarvitse huolehtia siitä onko polku riippuvainen palvelimenasetuksista
# os.environ['SCRIPT_FILENAME'] palauttaa polun suoritettavaan ohjelmaan (jinja.cgi)
# on syytä huomata, että tämä polku ei ole sama kuin tiedostopolku halava/jalava-palvelimissa
# os.path.dirname tipauttaa polusta muut kuin kansioit pois eli poistaa jinja.cgin
# os.path.join liittää os.path.dirnamen palauttaman polun ja 'templates' yhdeksi toimivaksi poluksi
# jos tätä haluaa kokeilla komentoriviltä niin tuloksena on keyerror. SCRIPT_FILENAME-ympäristömuuttuja löytyy
# vain www-palvelimen CGI-ympäristöstä eikä normaalista shellistä
try:
    tmpl_path = os.path.join(os.path.dirname(os.environ['SCRIPT_FILENAME']), 'templates')
except:
    # jos tänne päädytään www-palvelimessa niin koko sovellus kaatuu...
    tmpl_path = "templates"

# alustetaan jinjan kaipaama ympäristö ja asetetaan myös autoescape käyttöön eli jinja automaattisesti
# korjaa erikoismerkit html:ään kelpaavaan muotoon
try:
    env = Environment(autoescape=True, loader=FileSystemLoader(tmpl_path), extensions=['jinja2.ext.autoescape'])
except:
    # jinja2.ext.autoescape ei toimi halavassa/jalavassa 
    env = Environment(autoescape=True, loader=FileSystemLoader(tmpl_path))

# ladataan oma template
template = env.get_template('jinja.html')


print """Content-type: text/html; charset=UTF-8

"""
# Tähän asti kaikki otettu ohjeistuksesta AS IS.
# Tästä alkaa oma koodi
# Tällä CGI-ohjelmalla luodaan ruudukko
# ja siihen liikuteltavia punaisia ja sinisiä palloja.
# Author: Toni Pikkarainen

# Väriluokka 
# Käytännössä väriluokan olio edustaa tietyn väristen 
# pallojen kokonaisuutta. Pitää sisällään järjestyksessä
# pallojen rivi- ja sarakekoordinaatit.
class Vari:
    def __init__(self,vari):
        self.color=vari
        self.rivit=[]
        self.sarakkeet=[]
        self.vari=""
        self.rivi=""
        self.sarake=""
        

form = cgi.FieldStorage() 


# Funktio dekoodaa listan alkiot ja muuttaa ne vielä
# int-tyyppisiksi.
def dekoodaa_lista(lista):
    if len(lista)>0:
        for i in range(0, len(lista)):
            lista[i] = lista[i].decode("UTF-8")
            lista[i] = int(lista[i])
            
# Funktio, jonka mukaan toimitaan jos klikataan värillistä palloa 
# (punainen tai sininen)
# 1., 4. ja 5. argumentin pitää olla Vari-luokan olio.
# row ja col ovat klikatun ruudun koordinaatit.
def klikattuVaria(v,row, col, vihrea,sin):
    poisto=-1
    for x in range(0, len(v.rivit)):
        if (v.rivit[x] == row and v.sarakkeet[x] == col): 
            poisto=x

    if(poisto >= 0):
        v.rivit.pop(poisto)  # Poistetaan klikattu pallo Vari-oliosta
        v.sarakkeet.pop(poisto)
        
# Vaihdetaan vihreä pallo punaiseksi tai siniseksi
# riippuen siitä mikä vihreä pallo on ollut.    
    if vihrea.vari == v.color:
        v.rivit.append(vihrea.rivi)
        v.sarakkeet.append(vihrea.sarake)
    if vihrea.vari == sin.color:
        sin.rivit.append(vihrea.rivi)
        sin.sarakkeet.append(vihrea.sarake)
        
# Laitetaan vihreä pallo klikattuun ruutuun ja annetaan vihreän väriksi
# sen pallon väri mikä on ollut klikatussa ruudussa.    
    
    vihrea.rivi=row
    vihrea.sarake=col
    vihrea.vari=v.color


# Jos klikataan tyhjää tutkitaan tilanne tällä funktiolla.
def klikattuTyhjaa(vihr, pun, sin, row, col):
    if vihr.rivi != "":
        if vihr.vari == pun.color:
            pun.rivit.append(row)
            pun.sarakkeet.append(col)
        if vihr.vari == sin.color:
            sin.rivit.append(row)
            sin.sarakkeet.append(col)
        vihr.rivi=""
        vihr.vari=""
        vihr.sarake=""
            

# Luetaan ruudukon koko syötteestä
try:
    koko=int(form.getfirst("x",8))
except:
    koko = 8

if koko<8 or koko>16:
    koko=8

# Alustetaan ruudukon kokoinen 2-ulotteinen taulukko
# täyteen nollia.    
taulukko =[[0 for x in range(koko)] for y in range(koko)]  

# Luodaan variluokasta oliot pun ja sin ja vihr
pun=Vari("red")
sin=Vari("blue")
vihr=Vari("green")

# Kysytään käyttäjältä valinnainen teksti
teksti = form.getfirst("teksti","").decode("UTF-8")

# otetaan talteen klikatun pallon rivi ja sarake
rivi = form.getfirst("rivi","").decode("UTF-8")
sarake = form.getfirst("sarake","").decode("UTF-8")


# otetaan talteen vihreän pallon rivi ja sarake ja väri
vihr.rivi = form.getfirst("vihrrivi","").decode("UTF-8")
vihr.sarake = form.getfirst("vihrsarake","").decode("UTF-8")
vihr.vari = form.getfirst("vihrvari","").decode("UTF-8")


# Kysytään kaikkien punaisten ja sinisten osoitteet

pun.rivit = form.getlist("punrivit")
pun.sarakkeet = form.getlist("punsarakkeet")

sin.rivit = form.getlist("sinrivit")
sin.sarakkeet = form.getlist("sinsarakkeet")


# dekoodataan rivi- ja sarakelistat
dekoodaa_lista(pun.rivit)
dekoodaa_lista(pun.sarakkeet)
dekoodaa_lista(sin.rivit)
dekoodaa_lista(sin.sarakkeet)


# Otetaan klikatun väri talteen
klikvari = form.getfirst("klikvari","").decode("UTF-8")


# Tehdään eri toimintoja riippuen, onko klikattu ruutua
# jossa on sininen, punainen tai vihreä pallo tai
# joka on tyhjä.
if klikvari == "red":
    klikattuVaria(pun, int(rivi), int(sarake), vihr, sin)
    
if klikvari == "blue":
    klikattuVaria(sin, int(rivi), int(sarake), vihr, pun)
    
if klikvari == "empty":
    klikattuTyhjaa(vihr, pun, sin, int(rivi), int(sarake))
    
if klikvari == "":
    pun.rivit=[]
    pun.sarakkeet=[]
    sin.rivit=[]
    sin.sarakkeet=[]       

# Pistetään taulukkoon 1 merkkaamaan punaisia ja -1 sinisiä palloja
# Tehdään vain ekalla kierroksella.
if len(pun.rivit)==0:
    for i in range(0,koko):
        for j in range(0,koko):
            if j <= 1:
                taulukko[i][j]=1
            if j >= (koko-2):
                taulukko[i][j]=-1
               
    
# Asetetaan taulukkoon luku 1 niihin paikkoihin
# joiden koordinaatit löytyvät riveistä ja sarakkeista.
# Esim. jos rivit=[1,2] ja sarakkeet=[0,3] ->
# Taulukkoon tulee luvut 1 paikkoihin taulukko[1][0] ja taulukko[2][3]

# Laitetaan punaiset ykkösiksi, ekalla kiekalla ei tee mitään.
for x in range(len(pun.rivit)):    
    for i in range(koko):
        for j in range(koko):
            if (int(pun.rivit[x])==i and int(pun.sarakkeet[x])==j):
                taulukko[i][j]=1
            

# Laitetaan siniset miinus ykkösiksi, ekalla kiekalla ei tee mitään.
for x in range(len(sin.rivit)):    
    for i in range(koko):
        for j in range(koko):
            if (int(sin.rivit[x])==i and int(sin.sarakkeet[x])==j):
                taulukko[i][j]=-1

# Laitetaan vihreän kohdalle taulukkoon luku 2.
if vihr.rivi != "":
    for i in range(0,koko):
        for j in range(0,koko):
            if (int(vihr.rivi)==i and int(vihr.sarake)==j):
                taulukko[i][j]=2

             
# jos ollaan eka kierroksella tehdään tämä, eli lisätään piilotettuun listaan punaiset 
# ja siniset koordinaatit
if len(pun.rivit)==0:                
    for i in range(0,koko):
        for j in range(0,koko):
            if taulukko[i][j]==1:
                pun.rivit.append(i)
                pun.sarakkeet.append(j)
            if taulukko[i][j]==-1:
                sin.rivit.append(i)
                sin.sarakkeet.append(j)

# Haetaan annettu ruudunkoko. Oletuksena koko on 50.
# Koko viedään css-tiedoston luovalle cgi-ohjelmalle parametrina
try:
    ruutu=int(form.getfirst("ruutu",50))
except:
    ruutu = 50
    
if ruutu<50 or ruutu>200:
    ruutu=50

ruutuKoko=str(ruutu)

ruudunKokoVienti = "ruutu="+ruutuKoko

# Myös teksti kuljetetaan linkeissä parametrina, joten se
# sen erikoismerkit täytyy koodata tätä varten.
urlTeksti = urllib.quote(teksti.encode('utf8'))     

# Renderoidaan Jinjan template
print template.render(urlTeksti=urlTeksti,koko=koko,teksti=teksti,punrivit=pun.rivit, punsarakkeet=pun.sarakkeet,
 taul=taulukko, sinrivit=sin.rivit, sinsarakkeet=sin.sarakkeet, vihrrivi=vihr.rivi,
 vihrsarake=vihr.sarake,vihrvari=vihr.vari,ruudunKoko=ruudunKokoVienti).encode("UTF-8")