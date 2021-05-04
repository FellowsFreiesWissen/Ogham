#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2021, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "mail@fthiery.de"
__status__ = "1.0"
__update__ = "2021-05-04"

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
csv1 = dir_path + "\\" + "words.csv"
csv2 = dir_path + "\\" + "og_readings.csv"

# read csv file 1
data1 = pd.read_csv(
    csv1,
    encoding='utf-8',
    sep=',',
    usecols=['word', 'wikidata', 'type', 'translation', 'ref', 'variants', 'context', 'id']
)
print(data1.info())
# read csv file 1
data2 = pd.read_csv(
    csv2,
    encoding='utf-8',
    sep='|',
    usecols=['reading_id', 'insc', 'stone_id']
)
print(data2.info())


lines = []
lines.append("stone_id|reading_id|word_id|word|type\r\n")
lauf = 0

'''for index2, row2 in data2.iterrows():
    for index1, row1 in data1.iterrows():
        print(str(row2['reading_id']))
        print(str(row2['insc']))'''

for index2, row2 in data2.iterrows():
    lauf += 1
    print(lauf)
    for index1, row1 in data1.iterrows():
        variants = str(row1['variants'])
        variants = variants.replace("[", "")
        variants = variants.replace("]", "")
        variants_split = variants.split("|")
        for i in variants_split:
            if str(i) in str(row2['insc']):
                stone_id = str(row2['stone_id'])
                reading_id = str(row2['reading_id'])
                word_id = str(row1['id'])
                word_label = str(row1['word'])
                if str(row1['type']) == "Q67381377":
                    word_type = "formula"
                elif str(row1['type']) == "Q67382150":
                    word_type = "nomenclature"
                elif str(row1['type']) == "Q79401991":
                    word_type = "name"
                line = stone_id + "|" + reading_id + "|" + word_id + "|" + word_label + "|" + word_type + "\r\n"
                if line not in lines:
                    lines.append(line)

# write output file
file_out = dir_path + "\\" + "words_readings.csv"
file = codecs.open(file_out, "w", "utf-8")
for line in lines:
    file.write(line)
file.close()
