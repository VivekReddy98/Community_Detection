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
        self.cid = count(start=1, step=1)

    def PageRank(self, PR_itr='25000', PR_df='0.85', what='query_write'):
        self.graph.run(self.page_rank(what=what, label=self.label_gen(), relation='KNOWS', PR_itr=PR_itr, PR_df=PR_df))
        df_PR = self.graph.run(self.match_unique(what='property_PR', label=self.label_gen())).to_data_frame()
        self.PR_list = df_PR['uid'].tolist()
        return None
    
    def ConnectedComponents(self, what='query_write'):
        self.graph.run(self.CC(what=what, label=self.label_gen()))
        return None
        
    def Conductance(self, cid, node):
        Prev_CS = self.clusters[cid]['C_s']
        Prev_MS = self.clusters[cid]['M_s']
        old_conductance = Prev_CS/(2*Prev_MS+ Prev_CS) 
        edges_inside = self.graph.run(self.match(what='edge_inside',label=self.label_gen(),cid=cid,uid=node)).evaluate()/4.0
        edges_outside = self.graph.run(self.match(what='edge_outside',label=self.label_gen(),cid=cid,uid=node)).evaluate()/4.0
        print(node, cid, edges_inside, edges_outside)
        new_CS = Prev_CS-edges_inside+edges_outside 
        new_MS = Prev_MS+edges_inside   
        new_conductance = new_CS/(2*new_MS+ new_CS) 
        if new_conductance < old_conductance:
            return True
        else:
            return False
    
    def Execute(self):
        self.graph.run("MATCH (n:amazon_small) REMOVE n.C_D;")
        self.graph.run("MATCH (n:amazon_small) SET n.C_D = '0';")
        self.graph.run("MATCH (n:amazon_small) REMOVE n.partition;")
        self.PageRank()
        self.ConnectedComponents()
        for node in self.PR_list:
            #print(self.clusters)
            start = time.time()
            added = False
            CD_chance = self.graph.run(self.match(label=self.label_gen(), what="neighbours", uid=node)).to_ndarray().flatten().tolist()
            #print(CD_chance)
            for cluster in CD_chance:
                if cluster=="0":
                    continue
                added = self.Conductance(cluster, node)
                break
                if  added:
                    self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=node, cid=cluster))
            if not(added):
                cluster_id = next(self.cid)
                print(cluster_id)
                self.clusters[str(cluster_id)] = {}
                self.clusters[str(cluster_id)]['C_s'] = self.graph.run(self.match(what="C_s",label=self.label_gen(), uid=node)).evaluate()/4.0
                self.clusters[str(cluster_id)]['M_s'] = 0
                self.graph.run(self.cluster(what='set',label=self.label_gen(),uid=node,cid=str(cluster_id)))
            #print("The time taken for node {} is {} secs and Cluster is {}".format(node, (time.time()-start), str(cluster_id)))
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