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
csv = dir_path + "\\" + "stones_mac5.csv"

# read csv file
data = pd.read_csv(
    csv,
    encoding='utf-8',
    sep=',',
    usecols=['item', 'so']
)
print(data.info())
lines = []

# https://jsoneditoronline.org/#left=local.rixegu&right=local.fipoze

for index, row in data.iterrows():
    line = ""
    if str(row['so']) != "nan":
        line += "-" + str(row['item']) + "\t" + "P1545" + "\t" + "\"" + str(row['so']).replace(".0", "") + "\"" + "\r\n"
    # add line to output array
    lines.append(line)

# write output file
file_out = dir_path + "\\" + "wd_ciic_edit2.qs"
file = codecs.open(file_out, "w", "utf-8")
for line in lines:
    file.write(line)
file.close()
