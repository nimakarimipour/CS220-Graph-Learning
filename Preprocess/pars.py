import json
import xml.etree.ElementTree as ET
import re

G_PATH = '../Samples/alu/alu.xml'
R_PATH = '../Samples/alu/alu.route'
OUTPUT = '../Samples/alu/alu.json'

ROUTERS = []
EDGES = []
CHARGES = {}

def exctract_charges():
    file1 = open(R_PATH, 'r')
    Lines = file1.readlines()
    index = 0
    begin = "Node:	"
    while index < len(Lines):
        if(Lines[index].startswith("Net")):
            src = 0
            dest = 0
            index += 2
            src = [int(i) for i in Lines[index].split() if i.isdigit()][0]
            while((index + 1) < len(Lines) and Lines[index + 1] != "\n"):
                index += 1
            dest = [int(i) for i in Lines[index].split() if i.isdigit()][0]
            CHARGES[src] = str(dest)
        index += 1
        


def pars(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    index = 0
    for node in root.find("./rr_nodes"):
        ROUTERS.append(node.attrib['id'])

    for edge in root.find("./rr_edges"):
        EDGES.append({
            "from": edge.attrib['src_node'],
            "to": edge.attrib['sink_node'],
            "init": 1
        })

exctract_charges()
pars(G_PATH)

GRAPH = {"charges": CHARGES, "routers": ROUTERS, "edges": EDGES}

with open(OUTPUT, 'w') as outfile:
    json.dump(GRAPH, outfile)


