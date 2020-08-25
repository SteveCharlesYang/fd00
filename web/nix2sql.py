import requests
import json
from database import NodeDB
from graph import Node, Edge
import traceback
from flask import Config

def getJSON():
    r = requests.get('http://map.dn42/aspath')
    return r.json()

def insertData(graph_data, config):
    nodes = dict()
    edges = []
    for ind,n in enumerate(graph_data['nodes']):
        node = Node(str(n['asn']))
        nodes[ind] = node
    for e in graph_data['links']:
        edge = Edge(nodes[e['source']], nodes[e['target']])
        edges.append(edge)

    print("Accepted %d nodes and %d links." % (len(nodes), len(edges)))

    if len(nodes) == 0 or len(edges) == 0:
        return 'No valid nodes or edges'

    uploaded_by = "admin"

    try:
        with NodeDB(config) as db:
            db.insert_graph(nodes, edges, uploaded_by)
    except Exception:
        traceback.print_exc()
        return 'Database failure'

    return None


if __name__ == "__main__":
    json = getJSON()
    config = Config("./")
    config.from_pyfile('web_config.cfg')
    insertData(json,config)
