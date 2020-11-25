__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2020, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "mail@fthiery.de"
__status__ = "beta"
__update__ = "2020-11-25"

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

# set UTF8 as default
importlib.reload(sys)

# set paths
dir_path = os.path.dirname(os.path.realpath(__file__))
file_in = dir_path.replace("\\py", "\\data_raw\\CIIC_Ireland\\csv") + "\\" + "OghamStonesIreland.csv"
file_out = dir_path.replace("\\py", "\\ttl") + "\\" + "OghamStonesIreland.ttl"

# read csv file
data = pd.read_csv(
    file_in,
    encoding='utf-8',
    sep='|',
    usecols=['label_en', 'P1545_ciic', 'P625_coord'],
    na_values=['.', '??']  # take any '.' or '??' values as NA
)
print(data.info())

# create triples from dataframe
lineNo = 2
outStr = ""
lines = []
for index, row in data.iterrows():
    # print(lineNo)
    tmpno = lineNo - 2
    if tmpno % 10 == 0:
        print(tmpno)
    lineNo += 1
    lines.append("ogham:stone_ciic_" + str(row['P1545_ciic']) + " " + "rdf:type" + " oghamonto:Stone .")
    lines.append("ogham:stone_ciic_" + str(row['P1545_ciic']) + " " + "rdfs:label" + " " + "'" + str(row['label_en']).replace('\'', '`') + "'@en" + ".")
    lines.append("ogham:stone_ciic_" + str(row['P1545_ciic']) + " " + "dc:identifier" + " " + "'" + str(row['P1545_ciic']) + "'" + ".")
    # geom
    lines.append("ogham:stone_ciic_" + str(row['P1545_ciic']) + " " + "geosparql:hasGeometry" + " ogham:stone_ciic_" + str(row['P1545_ciic']) + "_geom .")
    lines.append("ogham:stone_ciic_" + str(row['P1545_ciic']) + "_geom " + "rdf:type" + " sf:the_geom .")
    split = str(row['P625_coord']).split(",")
    point = "POINT(" + str(split[1]) + " " + str(split[0]) + ")"
    point = "\"<http://www.opengis.net/def/crs/EPSG/0/4326> " + point + "\"^^geosparql:wktLiteral"
    lines.append("ogham:stone_ciic_" + str(row['P1545_ciic']) + "_geom " + "geosparql:asWKT " + point + ".")
    lines.append("")

files = (len(lines) / 100000) + 1
print("lines", len(lines), "files", int(files))

# write output file
print("start writing turtle file...")
file = codecs.open(file_out, "w", "utf-8")
file.write("# create triples from " + file_in + " \r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX geosparql: <http://www.opengis.net/ont/geosparql#> \r\nPREFIX dc: <http://purl.org/dc/elements/1.1/> \r\nPREFIX sf: <http://www.opengis.net/ont/sf#> \r\n"
prefixes += "PREFIX oghamonto: <http://ontology.ogham.link#> \r\nPREFIX ogham: <http://lod.ogham.link/data/> \r\n"
prefixes += "\r\n"
file.write(prefixes)
for line in lines:
    file.write(line)
    file.write("\r\n")

print("Yuhu!")
file.close()
print("*****************************************")
print("SUCCESS")
print("closing script")
print("*****************************************")
