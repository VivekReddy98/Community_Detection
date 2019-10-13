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
        with open("json_files/Conductance" + "_" + self.label_gen()+".json", 'r') as fp:
            self.clusters = json.load(fp)
            
    def SeedConductance(self, write=True):
        for key in self.clusters:
            self.clusters[key]['M_s'] = self.graph.run(self.conductance(what="M_s",label=self.label_gen(),cid=key)).evaluate() 
            if self.clusters[key]['M_s'] == 0.0:
                self.RemoveStupid(key)
                self.clusters[key]['C_s'] = 0
                continue
            self.clusters[key]['C_s'] = self.graph.run(self.conductance(what="C_s",label=self.label_gen(),cid=key)).evaluate()
        if write:
            with open("json_files/Conductance" + "_" + self.label_gen()+".json", 'w') as fp:
                 json.dump(self.clusters, fp)
        print('Finished')
        return None
                
    def ConductanceScore(self, cid):
        CS = self.clusters[cid]['C_s']
        MS = self.clusters[cid]['M_s']
        return CS/(2*MS+CS) 

    def modify_CD(self, cid, C_D, add):
        if not(add):
            ID = self.gen_cluster_id(cid, None)
            return C_D.replace(ID,"|0|")
        else:
            return self.gen_cluster_id(cid, prev=C_D)

    def RemoveStupid(self, cid):
        list_nodes = self.graph.run(self.cluster(what='nodes',label=self.label_gen(), cid=cid)).to_ndarray().flatten().tolist()
        for node in list_nodes:
            old_cid = self.graph.run(self.cluster(what='ask',label=self.label_gen(), uid=node)).evaluate()
            new_cid = self.modify_CD(cid, old_cid, add=False)
            self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=node, cid=new_cid))
        return None

    def is_inside(self, cid, C_D):
        if C_D.find("|"+str(cid)+"|") == -1:
            return False
        else:
            return True
        
    def ConductanceCheck(self, cid):
        old_score = self.ConductanceScore(cid)
        New_CS = self.graph.run(self.conductance(what="C_s",label=self.label_gen(),cid=cid)).evaluate()
        New_MS = self.graph.run(self.conductance(what="M_s",label=self.label_gen(),cid=cid)).evaluate()
        new_score = New_CS/(2*New_MS+New_CS)
        #print(cid, old_score, new_score)
        if new_score < old_score:
            self.clusters[cid]['C_s'] = New_CS
            self.clusters[cid]['M_s'] = New_MS
            return False
        else:
            return True

    def OneCluster(self, cid):
        self.recursion_depth = self.recursion_depth + 1
        inout_nodes = self.graph.run(self.cluster(what='one_hop_neigh',label=self.label_gen(),cid=cid)).to_data_frame()
        self.initial_score = self.ConductanceScore(cid)
        print("Recursion_Depth: {}, cid: {}, Start_Conductance: {}".format(self.recursion_depth, cid, self.initial_score))
        if self.initial_score == 0.0:
            return None
        while True:
            for index, row in inout_nodes.iterrows():
                old = row['C_D']
                new_cid = old
                if self.is_inside(cid, row['C_D']):
                    new_cid = self.modify_CD(cid, row['C_D'], add=False)
                    self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=row['uid'], cid=new_cid))
                    cannot_remove = self.ConductanceCheck(cid)
                    if cannot_remove:
                        self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=row['uid'], cid=row['C_D']))      
                else:
                    new_cid = self.modify_CD(cid, row['C_D'], add=True)
                    self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=row['uid'], cid=new_cid))
                    cannot_add = self.ConductanceCheck(cid)
                    if cannot_add:
                         self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=row['uid'], cid=row['C_D']))      
            if self.ConductanceScore(cid) < self.initial_score:
                self.OneCluster(cid)
            else:
                break
        return None

    def Execute(self):
        self.SeedConductance()
        for key in self.clusters:
            try: 
                self.ConductanceScore(key)
            except:
                continue
            self.recursion_depth = 0
            self.OneCluster(key)
        pass
      
#if __name__ == '__main__':
#     parent_dir = os.environ['GDMPATH']
#     graph = Graph("bolt:localhost:7474/databases/gdm.db", auth=("neo4j", ""))

#     category = ['amazon']  #'dblp', 'youtube']
#     variant = ['small',] #['medium', 'large'] 
#     di = {'amazon':'1', 'dblp':'2', 'youtube':'3', 'small':'4', 'medium':'5', 'large':'6'}

#     with open('query.json') as json_file:
#         json_dict = json.load(json_file)

#     with open('Regex_dict.json') as json_file:
#         regex_dict = json.load(json_file) 
    
#     start = time.time()
#     #R = RaRe(graph=graph, cat=category[0], var=variant[0], di=di, json_dict=json_dict, regex_dict=regex_dict)
#     #R.Execute()
#     #R.getConductanceDict(write=True)
#     print("The time taken for RaRe is {} mins".format((time.time()-start)/60))
    
#     #start = time.time()
#     I = IS(graph=graph, cat=category[0], var=variant[0], di=di, json_dict=json_dict, regex_dict=regex_dict)
#     I.Execute()
#     print("The time taken for IS is {} mins".format((time.time()-start)/60))
    
    
