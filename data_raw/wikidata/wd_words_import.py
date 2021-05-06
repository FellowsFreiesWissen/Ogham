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
csv = dir_path + "\\" + "words.csv"

# read csv file
data = pd.read_csv(
    csv,
    encoding='utf-8',
    sep=',',
    usecols=['word', 'wikidata', 'type', 'translation', 'ref', 'variants', 'context']
)
print(data.info())
lines = []

# https://jsoneditoronline.org/#left=local.rixegu&right=local.fipoze

for index, row in data.iterrows():
    if str(row['wikidata']) == "nan":
        line = "CREATE" + "\r\n"
        line += "" + "LAST" + "\t" + "Len" + "\t" + "\"" + str(row['word']) + "\"" + "\r\n"
        line += "" + "LAST" + "\t" + "Den" + "\t" + "\"" + str(row['translation']) + "\"" + "\r\n"
        alias = str(row['variants']).replace("[", "")
        alias = alias.replace("]", "")
        line += "" + "LAST" + "\t" + "Aen" + "\t" + "\"" + alias + "\"" + "\r\n"
        # instance
        line += "" + "LAST" + "\t" + "P31" + "\t" + str(row['type']) + "\t" + "P248" + "\t" + "Q70310399" + "\r\n"
        # part of
        line += "" + "LAST" + "\t" + "P361" + "\t" + "Q184661" + "\r\n"
        line += "" + "LAST" + "\t" + "P361" + "\t" + "Q70873595" + "\r\n"
        line += "" + "LAST" + "\t" + "P361" + "\t" + "Q100530634" + "\r\n"
        # add line to output array
        lines.append(line)

# write output file
file_out = dir_path + "\\" + "wd_words_import.qs"
file = codecs.open(file_out, "w", "utf-8")
for line in lines:
    file.write(line)
file.close()
