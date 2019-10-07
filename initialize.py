import sys,os, json
from py2neo import Graph, Node, Relationship, Database
from py2neo.matching import NodeMatcher
from py2neo.database import Schema
from Utils.GraphGenerator import GraphGenerator

parent_dir = os.environ['GDMPATH']
graph = Graph("bolt:localhost:7474/databases/gdm.db", auth=("neo4j", ""))

category = ['amazon']  #'dblp', 'youtube']
variant = ['small',] #['medium', 'large'] 
di = {'amazon':'1', 'dblp':'2', 'youtube':'3', 'small':'4', 'medium':'5', 'large':'6'}

with open('query.json') as json_file:
    json_dict = json.load(json_file)

with open('Regex_dict.json') as json_file:
    regex_dict = json.load(json_file) 

filename = "datasets/{}/{}.graph.{}".format(category[0], category[0], variant[0])
with open(parent_dir+filename) as fp:
    elements = fp.readline().strip().split(" ")

G = GraphGenerator(graph=graph, cat=category[0], var=variant[0], di=di, json_dict=json_dict, regex_dict=regex_dict)
import time 
start = time.time()
G.NodeInit(int(elements[0]))
print("The time taken for Node initialization is : {} minutes".format((time.time()-start)/60))

start = time.time()
filename = "datasets/{}/{}.graph.{}".format(category[0], category[0], variant[0])
G.Relation(path=filename)
print("The time taken for Edge initialization is : {} minutes".format((time.time()-start)/60))
