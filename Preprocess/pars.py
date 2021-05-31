import json
import xml.etree.ElementTree as ET

NODES = []
PATH = '../Samples/sample.xml'
OUTPUT = '../Samples/sample.json'

NODES = []
EDGES = []

def pars(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    index = 0
    for node in root.find("./rr_nodes"):
        NODES.append(node.attrib['id'])

    for edge in root.find("./rr_edges"):
        EDGES.append({
            "from": edge.attrib['src_node'],
            "to": edge.attrib['sink_node']
        })

pars(PATH)

GRAPH = {"nodes": NODES, "edges": EDGES}

######## ADD CHARGES LATER ########


with open(OUTPUT, 'w') as outfile:
    json.dump(GRAPH, outfile)
