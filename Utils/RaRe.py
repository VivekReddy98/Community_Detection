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
        old_conductance = Prev_CS/(2*Prev_MS + Prev_CS)
        edges_inside = self.graph.run(self.match(what='edge_inside',label=self.label_gen(),cid=cid,uid=node)).evaluate()
        edges_outside = self.graph.run(self.match(what='edge_outside',label=self.label_gen(),cid=cid,uid=node)).evaluate()
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

    def PossibleClusters(self, node):
        CD =  self.graph.run(self.match(label=self.label_gen(), what="neighbours", uid=node)).to_ndarray().flatten().tolist()
        #print("CD {}".format(CD))
        CID_set = set()
        for i in CD:
            CID_set.update(i.split("|")[1:-1])
        return CID_set

    def getConductanceDict(self, write=True):
        if write==True:
            with open("Conductance" + "_" + self.label_gen()+".json", 'w') as fp:
                json.dump(self.clusters, fp)
            return None
        else:
            return self.clusters

    def Execute(self):
        self.graph.run("MATCH (n:amazon_small) REMOVE n.C_D;")
        self.graph.run("MATCH (n:amazon_small) SET n.C_D = '|0|';")
        self.graph.run("MATCH (n:amazon_small) REMOVE n.pagerank;")
        self.graph.run("MATCH (n:amazon_small) REMOVE n.partition;")
        self.PageRank()
        self.ConnectedComponents()
        for node in self.PR_list:
            start = time.time()
            added = False
            CID_set = self.PossibleClusters(node)
            prev = None
            for cluster_id in CID_set:
                if cluster_id=="0":
                    continue
                added = self.Conductance(cluster_id, node)
                if  added:
                    prev = self.gen_cluster_id(cluster_id, prev=prev)
                    #print(prev)
                    self.graph.run(self.cluster(what='set',label=self.label_gen(), uid=node, cid=prev))
            if not(added):
                cluster_id = next(self.cid)
                self.clusters[str(cluster_id)] = {}
                self.clusters[str(cluster_id)]['C_s'] = self.graph.run(self.match(what="C_s",label=self.label_gen(), uid=node)).evaluate()
                self.clusters[str(cluster_id)]['M_s'] = 0
                prev = self.gen_cluster_id(cluster_id, prev=None)
                self.graph.run(self.cluster(what='set',label=self.label_gen(),uid=node,cid=prev))
            print("The time taken for node {} is {} secs and Cluster is {}".format(node, (time.time()-start), prev))
        return None


if __name__ == '__main__':
    parent_dir = os.environ["GDMPATH"]
    graph = Graph("bolt:localhost:7474", auth=("neo4j", "vivek1234"))

    category = ['amazon']  #'dblp', 'youtube']
    variant = ['small',] #['medium', 'large']
    di = {'amazon':'1', 'dblp':'2', 'youtube':'3', 'small':'4', 'medium':'5', 'large':'6'}

    with open('query.json') as json_file:
        json_dict = json.load(json_file)

    with open('Regex_dict.json') as json_file:
        regex_dict = json.load(json_file)

    R = RaRe(graph=graph, cat=category[0], var=variant[0], di=di, json_dict=json_dict, regex_dict=regex_dict)
    start = time.time()
    R.Execute()
    print("The time taken for RaRe is {} mins".format((time.time()-start)/60))
    R.getConductanceDict(write=True)
