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
__update__ = "2021-03-14"

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
import hashlib

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
    usecols=['filename', 'transliteration', 'ciic', 'translation', 'ogham', 'o3d']
)
print(data.info())
lines = []

# https://jsoneditoronline.org/#left=local.rixegu&right=local.fipoze

for index, row in data.iterrows():
    file_in = dir_path + "\\xml\\" + str(row['filename'])
    print("filename:" + file_in)
    df = pdx.read_xml(file_in, encoding='utf8')
    json2 = df.to_json()
    if str(row['filename']) == "145._Arraglen.xml":
        print(json2)
    line = ""
    # uuid
    uuid_pre = str.encode(str(row['filename']) + "O3D")
    hash_object = hashlib.sha512(uuid_pre)
    uuid = str(hash_object.hexdigest())[0:12]
    # csv file
    line += str(row['filename']) + "|"
    line += uuid + "|"
    line += str(row['transliteration']) + "|"
    line += str(row['ogham']) + "|"
    line += str(row['translation']) + "|"
    line += str(row['ciic']) + "|"
    line += str(row['o3d']) + "|"
    try:
        label = str(json.loads(json2)['TEI']['teiHeader']['fileDesc']['titleStmt']['title'])
    except KeyError:
        label = ""
    line += label + "|"
    try:
        townland = str(json.loads(json2)['TEI']['text']['body']['div'][6]['div'][0]['p']['rs']['placeName'][0])
        townland = townland.replace("\n", "")
        townland = townland.replace("  ", "")
    except:
        townland = ""
    try:
        townland = str(json.loads(json2)['TEI']['text']['body']['div'][6]['div'][0]['p']['rs']['placeName'][0]['#text'])
        townland = townland.replace("\n", "")
        townland = townland.replace("  ", "")
    except:
        townland = ""
    line += townland + "|"
    try:
        barony = str(json.loads(json2)['TEI']['text']['body']['div'][6]['div'][0]['p']['rs']['placeName'][1])
        barony = barony.replace("\n", "")
        barony = barony.replace("  ", "")
    except:
        barony = ""
    try:
        barony = str(json.loads(json2)['TEI']['text']['body']['div'][6]['div'][0]['p']['rs']['placeName'][1]['#text'])
        barony = barony.replace("\n", "")
        barony = barony.replace("  ", "")
    except:
        barony = ""
    line += barony + "|"
    try:
        geom = str(json.loads(json2)['TEI']['text']['body']['div'][6]['div'][0]['p']['rs']['geo'])
    except KeyError:
        geom = ""
    line += geom + "|"
    try:
        geom2 = str(json.loads(json2)['TEI']['text']['body']['div'][6]['div'][1]['p']['rs']['geo'])
    except KeyError:
        geom2 = ""
    line += geom2 + "|"
    try:
        geom3 = str(json.loads(json2)['TEI']['text']['body']['div'][6]['div'][2]['p']['rs']['geo'])
    except KeyError:
        geom3 = ""
    line += geom3 + "|"
    try:
        webgis = str(json.loads(json2)['TEI']['text']['body']['ab']['rs']['ref']['#text'])  # webgis.archaeology.ie
    except KeyError:
        webgis = ""
    line += webgis + "|"
    '''try:
        height = str(json.loads(json2)['TEI']['text']['body']['div'][1]['div'][1]['p']['rs'][1]['measure'][0]['#text'])
    except KeyError:
        height = "-1.0"
    line += height + "|"
    try:
        width = str(json.loads(json2)['TEI']['text']['body']['div'][1]['div'][1]['p']['rs'][1]['measure'][1]['#text'])
    except KeyError:
        width = "-1.0"
    line += width + "|"
    try:
        depth = str(json.loads(json2)['TEI']['text']['body']['div'][1]['div'][1]['p']['rs'][1]['measure'][2]['#text'])
    except KeyError:
        depth = "-1.0"
    line += depth + "|"'''
    '''try:
        persons_arr = []
        persons = json.loads(json2)['TEI']['text']['body']['div'][2]['ab']['persName']
        for x in range(len(persons)):
            person = json.loads(json2)['TEI']['text']['body']['div'][2]['ab']['persName'][x]['w']['@lemma']
            persons_arr.append(person)
    except KeyError:
        persons_arr = []
    line += str(persons_arr) + "|"
    try:
        formula_arr = []
        formulas = json.loads(json2)['TEI']['text']['body']['div'][2]['ab']['w']
        for x in range(len(formulas)):
            formula = json.loads(json2)['TEI']['text']['body']['div'][2]['ab']['w'][x]['@lemma']
            formula_arr.append(formula)
    except KeyError:
        formula_arr = []
    line += str(formula_arr) + "|"
    try:
        sitetype = str(json.loads(json2)['TEI']['text']['body']['div'][0]['p'])
    except KeyError:
        sitetype = ""
    line += sitetype + "|"
    try:
        recording = str(json.loads(json2)['TEI']['text']['body']['div'][7]['p']['#text']).replace("\n", "").replace("  ", " ")
        recording = recording.replace("  ", " ")
        recording = recording.replace("  ", " ")
        recording = recording.replace("  ", " ")
        recording = recording.replace("  ", " ")
        recording = recording.replace("  ", " ")
        recording = recording.replace("  ", " ")
        recording = recording.replace("  ", " ")
        recording = recording.replace(" .", ".")
    except recording:
        recording = ""
    line += recording + ""'''
    # add line to output array
    lines.append(line)

# write output file
# header = "filename|transliteration|ogham|translation|ciic|o3d|label|townland|barony|geom_found|geom_orig|geom_lastrecorded|webgis|height|width|depth|persons|formula|sitetype|recording"
header = "filename|uuid|transliteration|ogham|translation|ciic|o3d|label|townland|barony|geom_found|geom_orig|geom_lastrecorded|webgis"
file_out = dir_path + "\\" + "ogham3d.csv"
file = codecs.open(file_out, "w", "utf-8")
file.write(header + "\r\n")
for line in lines:
    file.write(line)
    file.write("\r\n")
file.close()
