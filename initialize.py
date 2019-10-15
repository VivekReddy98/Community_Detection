import sys,os,json,time
import pandas as pd
from py2neo import Graph, Node, Relationship, Database
from py2neo.matching import NodeMatcher
from py2neo.database import Schema
from Utils.GraphGenerator import GraphGenerator
from Utils.RaRe import RaRe
from Utils.IS import IS
from Utils.ClusterFileGenerator import ClusterFileGenerator
from Utils.CypherParser import Parse,ID_generator
import sys

parent_dir = os.environ['GDMPATH']
graph = Graph("bolt:localhost:7474/", auth=("neo4j", "password"))

categories = ['amazon','dblp','youtube']
variants = ['small', 'medium', 'large' ]  
di = {'amazon':'1', 'dblp':'2', 'youtube':'3', 'small':'4', 'medium':'5', 'large':'6'}

with open('json_files/query.json') as json_file:
    json_dict = json.load(json_file)

with open('json_files/Regex_dict.json') as json_file:
    regex_dict = json.load(json_file) 

cat = str(sys.argv[1])
var = str(sys.argv[2])

if cat not in categories:
    raise Exception('The argument 1 should be one of these [amazon, dblp or youtube]')
if var not in variants:
    raise Exception('The argument 2 should be one of these [small, medium or large]')

filename = "datasets/{}/{}.graph.{}".format(cat, cat, var)  

print(filename)

with open(parent_dir+filename) as fp:
    elements = fp.readline().strip().split(" ")

G = GraphGenerator(graph=graph, cat=cat, var=var, di=di, json_dict=json_dict, regex_dict=regex_dict)
print("Initializing Nodes for the graph {}_{}".format(cat,var))
start = time.time()
#G.NodeInit(int(elements[0]))
print("The time taken for Node initialization is : {} minutes".format((time.time()-start)/60))

print("Initializing Edges for the graph {}_{}".format(cat,var))
start = time.time()
#G.Relation(path=filename)
print("The time taken for Edge initialization is : {} minutes".format((time.time()-start)/60))

R = RaRe(graph=graph, cat=cat, var=var, di=di, json_dict=json_dict, regex_dict=regex_dict)
print("Computing RaRe(or LA) for the graph {}_{}...........".format(cat,var))
start = time.time()
R.Execute()
R.getConductanceDict(write=True)
print("The time taken for RaRe is {} mins".format((time.time()-start)/60))
num_clusters = len(R.getConductanceDict(write=False))
print("The total number of clusters found out by RaRe for the graph {}_{} is {}".format(cat,var,num_clusters))       

F = ClusterFileGenerator(graph=graph) 
F.genFile(cat, var, num_clusters, is_LA_output=True)     

print("Computing IS(or Iterative Scan) for the graph {}_{}".format(cat,var))
start = time.time()
I = IS(graph=graph, cat=cat, var=var, di=di, json_dict=json_dict, regex_dict=regex_dict)
I.Execute()
print("The time taken for IS is {} mins".format((time.time()-start)/60))

F = ClusterFileGenerator(graph=graph) 
F.genFile(cat, var, num_clusters, is_LA_output=False)    
