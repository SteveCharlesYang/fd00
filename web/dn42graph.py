#!/usr/bin/env python
import json
import io
import graphviz as gv
import networkx as nx
from networkx.algorithms import centrality
from networkx.algorithms.community import k_clique_communities
from flask import send_file

def get_graph(nodes, edges):
    #G = pgv.AGraph(strict=True, directed=False, size='10!')
    G = nx.Graph()
    for n in nodes:
        G.add_node(n['id'], label=n['label'])

    for e in edges:
        G.add_edge(e['sourceID'], e['targetID'], len=1.0)

    return G

def as_graph(asn):
    all_nodes, all_edges = load_graph_from_db(60*60*3)
    tier1s = [n['id'] for n in all_nodes if float(n['centrality']) > 0.08]
    #tier2s = [n['id'] for n in all_nodes if 0.03 < float(n['centrality']) < 0.08 ]
    G = get_graph(all_nodes, all_edges)
    paths = [list(nx.all_shortest_paths(G, source=asn, target=k)) for k in tier1s]    
    D = gv.Digraph()
    D.attr(rankdir = 'LR')
    #sub_origin = D.subgraph()
    #sub_tier2 = D.subgraph()
    #sub_tier1 = D.subgraph()
    #sub_origin.attr(rank='same')
    #sub_origin.node(asn)
    sub_origin_list = set()
    sub_tier1_list = set()
    #sub_tier2_list = set()
    sub_ord_list = set()
    sub_origin_list.add(asn)
    for tier1_path in paths:
        #indirect = True
        for each_path in tier1_path:
            isvalid_path = True
            #if each_path[len(each_path) - 2] not in tier1s or asn in tier1s:
            #    indirect = False
            for idx,each_node in enumerate(each_path):
                if idx != (len(each_path) - 1) and each_node in tier1s:
                    if each_path[idx+1] not in tier1s:
                        isvalid_path = False
            if isvalid_path:
            #if True:
                for each_node in each_path:
                #print(each_node)
                    if each_node not in tier1s:
                    #if each_node not in tier2s:
                        sub_ord_list.add(each_node)
                    #else:
                    #    sub_tier2_list.add(each_node)
                    else:
                        #if not indirect:
                        sub_tier1_list.add(each_node)
#with D.subgraph() as sub_origin:
        #sub_origin.attr(rank='999')
        #for node in sub_origin_list:
            #sub_origin.node(node)
    #with D.subgraph() as sub_ord:
        #sub_ord.attr(rank='3')
    D.node(asn)
    for node in sub_ord_list:
        D.node(node, URL="/lookup/AS" + node)
    #with D.subgraph() as sub_tier2:
        #sub_tier2.attr(rank='same')
        #for node in sub_tier2_list:
            #sub_tier2.node(node)
    with D.subgraph() as sub_tier1:
        sub_tier1.attr(rank='sink')
        for node in sub_tier1_list:
            sub_tier1.node(node, shape='box', URL="/lookup/AS" + node)
    edge_pairs = set()
    edge_w = {}
    #tier1_appear = {}
    for tier1_path in paths:
        for each_path in tier1_path:
            isvalid_path = True
            for idx,each_node in enumerate(each_path):
                if idx != (len(each_path) - 1) and each_node in tier1s:
                    if each_path[idx+1] not in tier1s:
                        isvalid_path = False
            if isvalid_path:
            #if True:
                for idx,each_node in enumerate(each_path):
                    if idx is not 0:
                        edge_pair_name = each_node + "." + each_path[idx-1]
                        if edge_pair_name in edge_w:
                            #if each_node not in tier1_appear:
                            edge_w[edge_pair_name] = edge_w[edge_pair_name] + 1
                        else:
                            edge_w[edge_pair_name] = 1
                        #if each_node in tier1s and each_path[idx-1] not in tier1s:
                            #tier1_appear[each_node] = True
                        #edge_pair_name = each_node + "." + each_path[idx-1]
                        edge_pairs.add(edge_pair_name)
    for edge_pair in edge_pairs:
        edge_nodes = edge_pair.split(".")
        w = edge_w[edge_pair]
        w = min(w, 5)
        #if edge_nodes[1] in tier1s and edge_nodes[0] in tier1s:
        #    if edge_nodes[1] not in tier1_appear:
        #        tier1_appear[edge_nodes[1]] = True
        #        D.edge(edge_nodes[1], edge_nodes[0])
        #if edge_nodes[1] not in sub_tier1_list:
        #else:
        if edge_nodes[1] in tier1s and edge_nodes[0] in tier1s:
            D.edge(edge_nodes[1], edge_nodes[0], style="dashed", concentrate='true', constriant='false', arrowsize="0.7", color="grey")
        else:
            D.edge(edge_nodes[1], edge_nodes[0], penwidth=str(w))
    outfile = D.pipe(format='svg')
    #outfile = base64.b64encode(outfile).decode('utf-8')
    return send_file(io.BytesIO(outfile), mimetype='image/svg+xml')

def path_graph(toasn, fromasn):
    all_nodes, all_edges = load_graph_from_db(60*60*3)
    G = get_graph(all_nodes, all_edges)
    paths = list(nx.all_shortest_paths(G, source=fromasn, target=toasn))
    D = gv.Digraph()
    D.attr(rankdir = 'LR')
    sub_asn_list = set()
    edge_pairs = set()
    for ipath in paths:
        for idx,inode in enumerate(ipath):
            sub_asn_list.add(inode)
            if idx != 0:
                edge_pairs.add(inode + "." + ipath[idx-1])
    D.node(fromasn)
    with D.subgraph() as subg:
        for node in sub_asn_list:
            subg.node(node)
    D.node(toasn)
    for edge_pair in edge_pairs:
        edge_nodes = edge_pair.split(".")
        D.edge(edge_nodes[0], edge_nodes[1])

    outfile = D.pipe(format='svg')
    return send_file(io.BytesIO(outfile), mimetype='image/svg+xml')


def load_graph_from_db(time_limit):
    with open('static/graph.json') as f:
        db = json.load(f)
        nodes = db['nodes']
        edges = db['edges']
        return (nodes, edges)


