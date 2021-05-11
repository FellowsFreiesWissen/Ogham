__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2021, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "mail@fthiery.de"
__status__ = "beta"
__update__ = "2021-05-11"

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
import hashlib
import _config

# set UTF8 as default
importlib.reload(sys)
print("*****************************************")

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# set paths
file_name = "og_stones_references"
dir_path = os.path.dirname(os.path.realpath(__file__))
file_in = dir_path.replace("\\py", "\\data_v1\\csv\\ogham") + "\\" + file_name + ".csv"

# read csv file
data = pd.read_csv(
    file_in,
    encoding='utf-8',
    sep=',',
    usecols=['g_id', 'id', 'original_id', 'stone_type', 'cisp_id', 'o3d', 'macalister_1945', 'macalister_1907', 'mcmanus_1991', 'macalister_1902', 'macalister_1897', 'cuppage_1986', 'macalister_1949', 'brash_1879', 'osullivan_1996', 'power_1992', 'macalister_1909', 'petrie_1872', 'brikil_1993', 'raftery_1960', 'okasha_forsyth_2001', 'ferguson_1887', 'power_1997', 'ciic_stone', 'cisp_stone', 'o3d_stone'],
    na_values=['.', '??', 'NULL']  # take any '.' or '??' values as NA
)
print(data.info())

# create triples from dataframe
lineNo = 2
outStr = ""
lines = []
for index, row in data.iterrows():
    tmpno = lineNo - 2
    if tmpno % 1000 == 0:
        print(tmpno)
    lineNo += 1
    # info
    lines.append("_:" + str(row['g_id']) + " " + "rdf:type" + " oghamonto:ReferenceChain .")
    if int(str(row['id'])) > 10000000 and int(str(row['id'])) < 20000000:
        lines.append("ogham:ciic:" + str(row['id']) + " " + "rdf:type" + " oghamonto:" + "macalister_1945" + " .")
        lines.append("ogham:ciic:" + str(row['id']) + " " + "rdfs:label" + " 'ciic:" + str(row['id']) + "' .")
    if int(str(row['id'])) > 20000000 and int(str(row['id'])) < 30000000:
        lines.append("ogham:cisp:" + str(row['id']) + " " + "rdf:type" + " oghamonto:" + "CISP" + " .")
        lines.append("ogham:cisp:" + str(row['id']) + " " + "rdfs:label" + " 'cisp:" + str(row['id']) + "' .")
    if int(str(row['id'])) > 30000000 and int(str(row['id'])) < 40000000:
        lines.append("ogham:o3d:" + str(row['id']) + " " + "rdf:type" + " oghamonto:" + "OghamIn3D" + " .")
        lines.append("ogham:o3d:" + str(row['id']) + " " + "rdfs:label" + " 'o3d:" + str(row['id']) + "' .")
    if int(str(row['id'])) > 50000000 and int(str(row['id'])) < 60000000:
        lines.append("ogham:squirrel:" + str(row['id']) + " " + "rdf:type" + " oghamonto:" + "SquirrelOgham" + " .")
        lines.append("ogham:squirrel:" + str(row['id']) + " " + "rdfs:label" + " 'squirrel:" + str(row['id']) + "' .")
    if str(row['macalister_1945']) != 'nan':
        if str(row['macalister_1945']) != 'undefined':
            lines.append("ogham:macalister_1945:" + str(row['macalister_1945']) + " " + "rdf:type" + " oghamonto:" + "macalister_1945" + " .")
            lines.append("ogham:macalister_1945:" + str(row['macalister_1945']) + " " + "rdfs:label" + " 'macalister_1945:" + str(row['macalister_1945']) + "' .")
            lines.append("ogham:ciic:" + str(row['id']) + " " + "oghamonto:equals" + " " + "ogham:macalister_1945:" + str(row['macalister_1945']) + "" + ".")
    lines.append("")

files = (len(lines) / 100000) + 1
print("triples", len(lines), "files", int(files))
thiscount = len(lines)
_config.count(thiscount)

# write output files
f = 0
step = 100000
fileprefix = file_name + "_"
prefixes = ""
prefixes += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\r\n"
prefixes += "@prefix owl: <http://www.w3.org/2002/07/owl#> .\r\n"
prefixes += "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\r\n"
prefixes += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\r\n"
prefixes += "@prefix geosparql: <http://www.opengis.net/ont/geosparql#> .\r\n"
prefixes += "@prefix dc: <http://purl.org/dc/elements/1.1/> .\r\n"
prefixes += "@prefix dct: <http://purl.org/dc/terms/> .\r\n"
prefixes += "@prefix sf: <http://www.opengis.net/ont/sf#> .\r\n"
prefixes += "@prefix prov: <http://www.w3.org/ns/prov#> .\r\n"
prefixes += "@prefix oghamonto: <http://ontology.ogham.link/> .\r\n"
prefixes += "@prefix ogham: <http://lod.ogham.link/data/> .\r\n"
prefixes += "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\r\n"
prefixes += "@prefix wd: <http://www.wikidata.org/entity/> .\r\n"
prefixes += "\r\n"

for x in range(1, int(files) + 1):
    strX = str(x)
    filename = dir_path.replace("\\py", "\\data_v1\\rdf\\ogham") + "\\" + fileprefix + strX + ".ttl"
    file = codecs.open(filename, "w", "utf-8")
    file.write("# create triples from " + file_name + ".csv \r\n")
    file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
    file.write(prefixes)
    i = f
    for i, line in enumerate(lines):
        if (i > f - 1 and i < f + step):
            file.write(line)
            file.write("\r\n")
    f = f + step
    print(" > " + fileprefix + strX + ".ttl")
    file.close()

print("*****************************************")
print("SUCCESS: closing script")
print("*****************************************")
