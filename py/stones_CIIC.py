__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2020-2021, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "mail@fthiery.de"
__status__ = "beta"
__update__ = "2021-01-11"

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

# set UTF8 as default
importlib.reload(sys)

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# set paths
dir_path = os.path.dirname(os.path.realpath(__file__))
file_in = dir_path.replace("\\py", "\\data_raw\\CIIC_Ireland\\csv") + "\\" + "OghamStonesIreland.csv"
file_in2 = "https://github.com/FellowsFreiesWissen/Ogham/blob/main/data_raw/CIIC_Ireland/csv/" + "OghamStonesIreland.csv"
file_out = dir_path.replace("\\py", "\\ttl") + "\\" + "OghamStonesIreland.ttl"

# read csv file
data = pd.read_csv(
    file_in,
    encoding='utf-8',
    sep='|',
    usecols=['label_en', 'P1545_ciic', 'P625_coord', 'P1684', 'WikidataID', 'description_en', 'alias_en', 'P1545_ciic'],
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
    if tmpno % 100 == 0:
        print(tmpno)
    lineNo += 1
    uuid_pre = str.encode(str(row['P1545_ciic']) + "CIIC")
    hash_object = hashlib.sha512(uuid_pre)
    uuid = str(hash_object.hexdigest())[0:12]
    # print(uuid)
    lines.append("ogham:" + uuid + " " + "rdf:type" + " oghamonto:Stone .")
    lines.append("ogham:" + uuid + " " + "rdfs:label" + " " + "'" + str(row['label_en']).replace('\'', '`') + "'@en" + ".")
    lines.append("ogham:" + uuid + " " + "dc:description" + " " + "'" + str(row['description_en']).replace('\'', '`') + "'@en" + ".")
    lines.append("ogham:" + uuid + " " + "oghamonto:alias" + " " + "'" + str(row['alias_en']).replace('\'', '`') + "'@en" + ".")
    lines.append("ogham:" + uuid + " " + "oghamonto:numbering" + " " + "'" + str(row['P1545_ciic']) + "'" + ".")
    lines.append("ogham:" + uuid + " " + "dc:identifier" + " " + "'" + str(row['P1545_ciic']) + "'" + ".")
    lines.append("ogham:" + uuid + " " + "oghamonto:shows" + " " + "'" + str(row['P1684']) + "'" + ".")
    lines.append("ogham:" + uuid + " " + "oghamonto:exactMatch" + " <" + "http://www.wikidata.org/entity/" + str(row['WikidataID']) + ">" + ".")
    # geom
    lines.append("ogham:" + uuid + " " + "geosparql:hasGeometry" + " ogham:" + uuid + "_geom .")
    lines.append("ogham:" + uuid + "_geom " + "rdf:type" + " sf:Point .")
    split = str(row['P625_coord']).split(",")
    point = "POINT(" + str(split[1]) + " " + str(split[0]) + ")"
    point = "\"" + point + "\"^^geosparql:wktLiteral"
    lines.append("ogham:" + uuid + "_geom " + "geosparql:asWKT " + point + ".")
    lines.append("ogham:" + uuid + "_geom " + "oghamonto:hasEPSG " + "<http://www.opengis.net/def/crs/EPSG/0/4326>" + ".")
    # prov-o
    lines.append("ogham:" + uuid + " " + "prov:wasAttributedTo" + " ogham:PythonStonesCIIC .")
    lines.append("ogham:" + uuid + " " + "prov:wasDerivedFrom" + " <https://github.com/FellowsFreiesWissen/Ogham/blob/main/data_raw/CIIC_Ireland/csv/OghamStonesIreland.csv> .")
    lines.append("ogham:" + uuid + " " + "prov:wasGeneratedBy" + " ogham:" + uuid + "_activity .")
    lines.append("ogham:" + uuid + "_activity " + "rdf:type" + " <http://www.w3.org/ns/prov#Activity> .")
    lines.append("ogham:" + uuid + "_activity " + "prov:startedAtTime '" + starttime + "'^^xsd:dateTime .")
    lines.append("ogham:" + uuid + "_activity " + "prov:endedAtTime '" + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "'^^xsd:dateTime .")
    lines.append("ogham:" + uuid + "_activity " + "prov:wasAssociatedWith" + " ogham:PythonStonesCIIC .")
    lines.append("")

files = (len(lines) / 100000) + 1
print("triples", len(lines), "files", int(files))

# write output file
print("start writing turtle file...")
file = codecs.open(file_out, "w", "utf-8")
file.write("# create triples from " + file_in2 + " \r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
prefixes = ""
prefixes += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\r\n"
prefixes += "@prefix owl: <http://www.w3.org/2002/07/owl#> .\r\n"
prefixes += "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\r\n"
prefixes += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\r\n"
prefixes += "@prefix geosparql: <http://www.opengis.net/ont/geosparql#> .\r\n"
prefixes += "@prefix dc: <http://purl.org/dc/elements/1.1/> .\r\n"
prefixes += "@prefix sf: <http://www.opengis.net/ont/sf#> .\r\n"
prefixes += "@prefix prov: <http://www.w3.org/ns/prov#> .\r\n"
prefixes += "@prefix oghamonto: <http://ontology.ogham.link/> .\r\n"
prefixes += "@prefix ogham: <http://lod.ogham.link/data/> .\r\n"
prefixes += "\r\n"
file.write(prefixes)
for line in lines:
    file.write(line)
    file.write("\r\n")
file.close()

print("*****************************************")
print("SUCCESS")
print("closing script")
print(len(lines), "Triples")
print("*****************************************")
