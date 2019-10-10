import sys,os,json,re,time,copy
import pandas as pd
from py2neo import Graph, Node, Relationship, Database
from py2neo.database import Schema
from Utils.CypherParser import Parse, ID_generator
from itertools import count

class RaRe(Parse, ID_generator):
    def __init__(self, graph, cat, var, di, json_dict, regex_dict):
        self.graph = graph
        self.cat = cat
        self.var = var
        self.di = di
        self.json_map = json_dict
        self.regex = regex_dict
        self.graph = graph
        self.schema = Schema(self.graph)
        self.PR_list = []
        self.clusters = {}
        self.cp_map = dict()
        self.cid = count(start=1, step=1)

    def PageRank(self, PR_itr='25000', PR_df='0.85', what='query_write'):
        self.graph.run(self.page_rank(what=what, label=self.label_gen(), relation='KNOWS', PR_itr=PR_itr, PR_df=PR_df))
        df_PR = self.graph.run(self.match_unique(what='property_PR', label=self.label_gen())).to_data_frame()
        self.PR_list = df_PR['uid'].tolist()
        return None
    
    def CC(self, what='query_write'):
        self.graph.run(self.CC(what=what, label=self.label_gen(), relation='KNOWS'))
        return None
        
    def Conductance(self, cid):
        C_s = self.graph.run(self.conductance(what='C_s', cid=cid, label=self.label_gen())).evaluate()/2.0
        M_s = self.graph.run(self.conductance(what='M_s', cid=cid, label=self.label_gen())).evaluate()
        conductance_score = C_s/(M_s+C_s)
        return conductance_score
    
    def Execute(self):
        #self.graph.run("MATCH (n:amazon_small) REMOVE n.C_D")
        #self.graph.run("MATCH (n:amazon_small) SET n.C_D = '|0|';")
        self.PageRank()
        for node in self.PR_list:
            prev_immute = self.graph.run(self.cluster(what='ask', label=self.label_gen(), uid=node)).evaluate()
            added = False
            for cluster_id, score in self.clusters.items():
                part = self.graph.run(self.match_unique(what='Partition',label=self.label_gen(),uid=node)).evaluate()
                if part!=self.cp_map[cluster_id]:
                    continue                 
                cluster = self.gen_cluster_id(cluster_id, prev=prev_immute)
                self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=node, cid=cluster))
                new_score = self.Conductance("|"+str(cluster_id)+"|")
                if  new_score < score:
                    self.clusters[cluster_id] = new_score
                    added = True
                else:
                    self.graph.run(self.cluster(what='set',label=self.label_gen(),uid=node,cid=prev_immute))
            if not(added):
                cluster_id = next(self.cid)                
                self.clusters[cluster_id] = 1 
                partition = self.graph.run(self.match_unique(what='Partition',label=self.label_gen(),uid=node)).evaluate()
                self.cp_map[cluster_id] = partition
                print(node, self.cp_map[cluster_id])
                cluster = self.gen_cluster_id(cluster_id, prev=prev_immute)
                self.graph.run(self.cluster(what='set',label=self.label_gen(),uid=node,cid=cluster))
            print(node, prev_immute, cluster)
        return None
               
    
if __name__ == '__main__':
    parent_dir = os.environ['GDMPATH']
    graph = Graph("bolt:localhost:7474/databases/gdm.db", auth=("neo4j", ""))

    category = ['amazon']  #'dblp', 'youtube']
    variant = ['small',] #['medium', 'large'] 
    di = {'amazon':'1', 'dblp':'2', 'youtube':'3', 'small':'4', 'medium':'5', 'large':'6'}

    with open('query.json') as json_file:
        json_dict = json.load(json_file)

    with open('Regex_dict.json') as json_file:
        regex_dict = json.load(json_file) 
        
    R = RaRe(graph=graph, cat=category[0], var=variant[0], di=di, json_dict=json_dict, regex_dict=regex_dict)
    start = time.time()
    #R.PageRank(PR_itr='10000', PR_df='0.85')
    R.Execute()
    print("The time taken for Page Rank is {} mins".format((time.time()-start)/60))