#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2020, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "mail@fthiery.de"
__status__ = "beta"
__update__ = "2021-02-23"

# import dependencies
import uuid
import requests
import io
import pandas as pd
import os
import codecs
import datetime
import importlib
import sys
import xml.etree.ElementTree as ET
import pandas_read_xml as pdx
import json
import numpy as np

# set UTF8 as default
# -*- coding: utf-8 -*-
importlib.reload(sys)

# read CSV [filename, inscription, CIIC]

dir_path = os.path.dirname(os.path.realpath(__file__))
csv = dir_path + "\\" + "files.csv"

# read csv file
data = pd.read_csv(
    csv,
    encoding='utf-8',
    sep='|',
    usecols=['filename', 'transliteration', 'ciic', 'ogham']
)
print(data.info())
lines = []

for index, row in data.iterrows():
    file_in = dir_path + "\\xml\\" + str(row['filename'])
    print("filename:" + file_in)
    df = pdx.read_xml(file_in, encoding='utf8')
    json2 = df.to_json()
    line = ""
    line += str(row['filename']) + "|"
    line += str(row['transliteration']) + "|"
    line += str(row['ogham']) + "|"
    line += str(row['ciic']) + "|"
    try:
        label = str(json.loads(json2)['TEI']['teiHeader']['fileDesc']['titleStmt']['title'])
    except KeyError:
        label = ""
    line += label + "|"
    try:
        findspot = str(json.loads(json2)['TEI']['text']['body']['head']['name']['placeName']['#text'])
    except KeyError:
        findspot = ""
    line += findspot + "|"
    try:
        geom = str(json.loads(json2)['TEI']['text']['body']['div'][6]['div'][0]['p']['rs']['geo'])
    except KeyError:
        geom = ""
    line += geom + "|"
    try:
        translation = str(json.loads(json2)['TEI']['text']['body']['div'][3]['p']['q'])
    except KeyError:
        translation = ""
    line += translation + "|"
    try:
        webgis = str(json.loads(json2)['TEI']['text']['body']['ab']['rs']['ref']['#text'])  # webgis.archaeology.ie
    except KeyError:
        webgis = ""
    line += webgis + ""
    lines.append(line)

# write output file
header = "filename|transliteration|ogham|ciic|label|findspot|geom|translation|webgis"
file_out = dir_path + "\\" + "ogham3d.csv"
file = codecs.open(file_out, "w", "utf-8")
file.write(header + "\r\n")
for line in lines:
    file.write(line)
    file.write("\r\n")
file.close()
