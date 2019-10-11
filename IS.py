import sys,os,json,re,time,copy
import pandas as pd
from py2neo import Graph, Node, Relationship, Database
from py2neo.database import Schema
from Utils.CypherParser import Parse, ID_generator
from itertools import count

class IS(Parse, ID_generator):
     def __init__(self, graph, cat, var, di, json_dict, regex_dict):
        self.graph = graph
        self.cat = cat
        self.var = var
        self.di = di
        self.json_map = json_dict
        self.regex = regex_dict
        self.graph = graph
        with open("Conductance" + "_" + self.label_gen()+".json", 'r') as fp:
            self.conductance = json.load(fp)
    
    def Conductance(self, cid, node):
        Prev_CS = self.clusters[cid]['C_s']
        Prev_MS = self.clusters[cid]['M_s']
        old_conductance = Prev_CS/(2*Prev_MS+ Prev_CS) 
        edges_inside = self.graph.run(self.match(what='edge_inside',label=self.label_gen(),cid=cid,uid=node)).evaluate()/4.0
        edges_outside = self.graph.run(self.match(what='edge_outside',label=self.label_gen(),cid=cid,uid=node)).evaluate()/4.0
        #print(node, cid, edges_inside, edges_outside)
        new_CS = Prev_CS-edges_inside+edges_outside 
        new_MS = Prev_MS+edges_inside   
        new_conductance = new_CS/(2*new_MS+ new_CS) 
        if new_conductance < old_conductance:
            self.clusters[cid]['C_s'] = new_CS
            self.clusters[cid]['M_s'] = new_MS
            return True
        else:
            return False
    
    def OneCluster(self)
    
        
    def Execute(self):
        
        return None
        
    