import sys,os,json,re, time
from py2neo import Graph, Node, Relationship, Database
from py2neo.matching import NodeMatcher
from py2neo.database import Schema
from Utils.CypherParser import Parse, ID_generator

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

    def PageRank(self, PR_itr='1000', PR_df='0.85', what='query_write'):
        self.graph.run(self.page_rank(what=what, label=self.label_gen(), relation='KNOWS', PR_itr=PR_itr, PR_df=PR_df))
        return None
    
    def ConnectedComponents(self, what='query_write'):
        self.graph.run(self.CC(what=what, label=self.label_gen(), relation='KNOWS'))
        return None
        
    def ClusterComponent(self):
        pass
    
    def Execute(self, PR_itr, PR_df):
        #self.PageRank(PR_itr=PR_itr, PR_df=PR_df)
        #self.ConnectedComponents(what='query_write')
        df_partitions = self.graph.run(self.match_unique(label=self.label_gen(), prop='partition')).to_data_frame()
        cluster_labels = set(df_partitions['partition'].to_numpy())
        
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
    R.Execute(PR_itr='10000', PR_df='0.85')
    #print("The time taken for Page Rank is {} mins".format((time.time()-start)/60))