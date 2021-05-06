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
__update__ = "2021-05-01"

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
csv = dir_path + "\\" + "os_mac.csv"

# read csv file
data = pd.read_csv(
    csv,
    encoding='utf-8',
    sep=',',
    usecols=['item', 'label', 'desc', 'geo', 'logainm', 'osm']
)
print(data.info())
lines = []

# https://jsoneditoronline.org/#left=local.rixegu&right=local.fipoze

for index, row in data.iterrows():
    line = ""
    line += "" + str(row['item']) + "\t" + "Len" + "\t" + "\"" + str(row['label']) + "\"" + "\r\n"
    line += "" + str(row['item']) + "\t" + "Den" + "\t" + "\"" + str(row['desc']) + "\"" + "\r\n"
    line += "" + str(row['item']) + "\t" + "P361" + "\t" + "Q100530634" + "\r\n"
    line += "-" + str(row['item']) + "\t" + "P31" + "\t" + "Q2151232" + "\r\n"
    line += "-" + str(row['item']) + "\t" + "P31" + "\t" + "Q2221906" + "\r\n"
    if str(row['logainm']) != "nan":
        line += "-" + str(row['item']) + "\t" + "P5097" + "\t" + "\"" + str(row['logainm']).replace(".0", "") + "\"" + "\r\n"
    if str(row['osm']) != "nan":
        line += "-" + str(row['item']) + "\t" + "P402" + "\t" + "\"" + str(row['osm']).replace(".0", "") + "\"" + "\r\n"
    # add line to output array
    lines.append(line)

# write output file
file_out = dir_path + "\\" + "wd_ciic_edit.qs"
file = codecs.open(file_out, "w", "utf-8")
for line in lines:
    file.write(line)
file.close()
