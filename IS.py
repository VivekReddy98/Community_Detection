import sys,os,json,re,time,copy
import pandas as pd
from py2neo import Graph, Node, Relationship, Database
from py2neo.database import Schema
from Utils.CypherParser import Parse, ID_generator
from Utils.RaRe import RaRe
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
        self.recursion_depth = 0
        with open("Conductance" + "_" + self.label_gen()+".json", 'r') as fp:
            self.clusters = json.load(fp)
            
    def SeedConductance(self, write=True):
        for key in self.clusters:
            self.clusters[key]['C_s'] = self.graph.run(self.conductance(what="C_s",label=self.label_gen(),cid=key)).evaluate()
            self.clusters[key]['M_s'] = self.graph.run(self.conductance(what="M_s",label=self.label_gen(),cid=key)).evaluate()
        if write:
            with open("Conductance" + "_" + self.label_gen()+".json", 'w') as fp:
                 json.dump(self.clusters, fp)
        print('Finished')
        return None
                
    def Conductance_in(self, cid, node):
        Prev_CS = self.clusters[cid]['C_s']
        Prev_MS = self.clusters[cid]['M_s']
        old_conductance = Prev_CS/(2*Prev_MS+Prev_CS) 
        edges_inside = self.graph.run(self.match(what='edge_inside',label=self.label_gen(),cid=cid, uid=node)).evaluate()
        edges_outside = self.graph.run(self.match(what='edge_outside',label=self.label_gen(),cid=cid,uid=node)).evaluate()
        print(node, Prev_CS, Prev_MS, cid, edges_inside, edges_outside, "inside")
        new_CS = Prev_CS+edges_inside-edges_outside 
        new_MS = Prev_MS-edges_inside   
        new_conductance = new_CS/(2*new_MS+new_CS) 
        if new_conductance < old_conductance:
            self.clusters[cid]['C_s'] = new_CS
            self.clusters[cid]['M_s'] = new_MS
            return True
        else:
            return False

    def Conductance_out(self, cid, node):
        Prev_CS = self.clusters[cid]['C_s']
        Prev_MS = self.clusters[cid]['M_s']
        old_conductance = Prev_CS/(2*Prev_MS+ Prev_CS) 
        edges_inside = self.graph.run(self.match(what='edge_inside',label=self.label_gen(),cid=cid,uid=node)).evaluate()
        edges_outside = self.graph.run(self.match(what='edge_outside',label=self.label_gen(),cid=cid,uid=node)).evaluate()
        print(node, Prev_CS, Prev_MS, cid, edges_inside, edges_outside, "outside")
        new_CS = Prev_CS-edges_inside+edges_outside 
        new_MS = Prev_MS+edges_inside   
        new_conductance = new_CS/(2*new_MS+ new_CS) 
        if new_conductance < old_conductance:
            self.clusters[cid]['C_s'] = new_CS
            self.clusters[cid]['M_s'] = new_MS
            return True
        else:  
            
            return False

    def ConductanceScore(self, cid):
        CS = self.clusters[cid]['C_s']
        MS = self.clusters[cid]['M_s']
        return CS/(2*MS+ CS) 

    def modify_CD(self, cid, C_D, add):
        if not(add):
            ID = self.gen_cluster_id(cid, None)
            return C_D.replace(ID,"|")
        else:
            return self.gen_cluster_id(cid, prev=C_D)

    def RemoveStupid(self):
        #Stupid Clusters Removal is yet to be written
        #self.numClust = len(self.clusters)
        return None

    def is_inside(self, cid, C_D):
        if C_D.find("|"+str(cid)+"|") == -1:
            return False
        else:
            return True

    def OneCluster(self, cid):
        self.recursion_depth = self.recursion_depth + 1
        print("Recursion_Depth: {}, cid: {} ".format(self.recursion_depth, cid))
        increased = True
        inout_nodes = self.graph.run(self.cluster(what='one_hop_neigh',label=self.label_gen(),cid=cid)).to_data_frame()
        #print(inout_nodes)
        initial_score = self.ConductanceScore(cid)
        while increased:
            for index, row in inout_nodes.iterrows():
                old = row['C_D']
                new_cid = old
                if self.is_inside(cid, row['C_D']):
                    can_remove = self.Conductance_in(cid, row['uid'])
                    if can_remove:
                        new_cid = self.modify_CD(cid, row['C_D'], add=False)
                        self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=row['uid'], cid=new_cid))
                else:
                    can_add = self.Conductance_out(cid, row['uid'])
                    if can_add:
                        new_cid = self.modify_CD(cid, row['C_D'], add=True)
                        self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=row['uid'], cid=new_cid))    
            if self.ConductanceScore(cid) < initial_score:
                self.OneCluster(cid)
            else:
                increased = False
        return None

    def Execute(self):
        self.RemoveStupid()
        self.SeedConductance()
        for key in self.clusters:
            self.recursion_depth = 0
            self.OneCluster(key)
        pass
      
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
    
    start = time.time()
    R = RaRe(graph=graph, cat=category[0], var=variant[0], di=di, json_dict=json_dict, regex_dict=regex_dict)
    R.Execute()
    R.getConductanceDict(write=True)
    print("The time taken for RaRe is {} mins".format((time.time()-start)/60))
    
    #start = time.time()
    I = IS(graph=graph, cat=category[0], var=variant[0], di=di, json_dict=json_dict, regex_dict=regex_dict)
    I.Execute()
    print("The time taken for IS is {} mins".format((time.time()-start)/60))
    
    