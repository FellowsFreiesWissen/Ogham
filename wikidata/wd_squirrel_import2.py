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
__update__ = "2021-05-02"

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
csv = dir_path + "\\" + "squirrel_stones2_qs.csv"

# read csv file
data = pd.read_csv(
    csv,
    encoding='utf-8',
    sep='|',
    usecols=['label', 'desc', 'country', 'site', 'county', 'representing_insc', 'ino', 'st_astext', 'ciic_wd', 'cisp_wd', 'o3d_wd']
)
print(data.info())
lines = []

for index, row in data.iterrows():
    line = "CREATE" + "\r\n"
    line += "" + "LAST" + "\t" + "Len" + "\t" + "\"" + str(row['label']) + "\"" + "\r\n"
    line += "" + "LAST" + "\t" + "Den" + "\t" + "\"" + str(row['desc']) + "\"" + "\r\n"
    # instance
    line += "" + "LAST" + "\t" + "P31" + "\t" + "Q2016147" + "\r\n"
    line += "" + "LAST" + "\t" + "P31" + "\t" + "Q106602575" + "\r\n"
    line += "" + "LAST" + "\t" + "P31" + "\t" + "Q106602643" + "\r\n"
    # part of
    line += "" + "LAST" + "\t" + "P361" + "\t" + "Q67978809" + "\r\n"
    line += "" + "LAST" + "\t" + "P361" + "\t" + "Q70873595" + "\r\n"
    line += "" + "LAST" + "\t" + "P361" + "\t" + "Q100530634" + "\r\n"
    # country
    line += "" + "LAST" + "\t" + "P17" + "\t" + "" + str(row['country']) + "" + "\r\n"
    line += "" + "LAST" + "\t" + "P276" + "\t" + "" + str(row['country']) + "" + "\r\n"
    # site
    line += "" + "LAST" + "\t" + "P189" + "\t" + "" + str(row['site']) + "" + "\r\n"
    point = str(row['st_astext']).replace("POINT(", "")
    point = point.replace(")", "")
    point_split = point.split(" ")
    if str(row['st_astext']) != "nan":
        line += "" + "LAST" + "\t" + "P625" + "\t" + "@" + point_split[1] + "/" + point_split[0] + "" + "\r\n"
    # county
    line += "" + "LAST" + "\t" + "P131" + "\t" + "" + str(row['county']) + "" + "\r\n"
    # inscription
    if str(row['representing_insc']) != "nan":
        line += "" + "LAST" + "\t" + "P1684" + "\t" + "ga:\"" + str(row['representing_insc']).replace("\r\n", "") + "\"" + "\t" + "P248" + "\t" + "Q70873595" + "\r\n"
    # inventory number
    line += "" + "LAST" + "\t" + "P195" + "\t" + "" + "Q70873595" + "" + "\r\n"
    line += "" + "LAST" + "\t" + "P217" + "\t" + "\"" + str(row['ino']).replace(".0", "") + "\"" + "\t" + "P195" + "\t" + "Q70873595" + "\r\n"
    # other stones
    if str(row['ciic_wd']) != "nan":
        line += "" + "LAST" + "\t" + "P1382" + "\t" + "" + str(row['ciic_wd']) + "" + "\t" + "P195" + "\t" + "Q70256237" + "\r\n"
    if str(row['cisp_wd']) != "nan":
        line += "" + "LAST" + "\t" + "P1382" + "\t" + "" + str(row['cisp_wd']) + "" + "\t" + "P195" + "\t" + "Q106628017" + "\r\n"
    if str(row['o3d_wd']) != "nan":
        line += "" + "LAST" + "\t" + "P1382" + "\t" + "" + str(row['o3d_wd']) + "" + "\t" + "P195" + "\t" + "Q106674066" + "\r\n"
    # add line to output array
    lines.append(line)

# write output file
file_out = dir_path + "\\" + "wd_squirrel_import2.qs"
file = codecs.open(file_out, "w", "utf-8")
for line in lines:
    file.write(line)
file.close()
