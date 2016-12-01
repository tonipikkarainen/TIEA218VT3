#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgitb
cgitb.enable()
import cgi
import os
from jinja2 import Template, Environment, FileSystemLoader
try:
    tmpl_path = os.path.join(os.path.dirname(os.environ['SCRIPT_FILENAME']), 'templates')
except:
    # jos tänne päädytään www-palvelimessa niin koko sovellus kaatuu...
    tmpl_path = "templates"

try:
    env = Environment(autoescape=True, loader=FileSystemLoader(tmpl_path), extensions=['jinja2.ext.autoescape'])
except: 
    env = Environment(autoescape=True, loader=FileSystemLoader(tmpl_path))

# Tähän asti kaikki otettu ohjeistuksesta AS IS.
# Tästä alkaa oma koodi
# Tällä cgi-ohjelmalla luodaan muutettava css-tiedosto.
# Author: Toni Pikkarainen
    
    
# ladataan oma template

template = env.get_template('jinja.css')

form = cgi.FieldStorage() 

print """Content-type: text/css; charset=UTF-8

"""
try:
    ruutu=int(form.getfirst("ruutu",50))
except:
    ruutu = 50
    
if ruutu<50 or ruutu>200:
    ruutu=50

ruutuKoko=str(ruutu)+"px"


print template.render(koko=ruutuKoko).encode("UTF-8")