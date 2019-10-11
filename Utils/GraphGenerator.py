import json
from py2neo import Graph, Node, Relationship, Database
from py2neo.matching import NodeMatcher
from py2neo.database import Schema
from Utils.CypherParser import Parse, ID_generator

class GraphGenerator(Parse, ID_generator):
    def __init__(self, graph, cat, var, di, json_dict, regex_dict):
        self.cat = cat
        self.var = var
        self.di = di
        self.json_map = json_dict
        self.regex = regex_dict
        self.graph = graph
        self.schema = Schema(self.graph)
        
    def NodeInit(self, node_count, Index_gen=True):
        if Index_gen:  
             self.schema.create_index(self.label_gen(), 'uid','cid')
        tx = self.graph.begin()
        for i in range(0,node_count):
            tx.create(Node(self.label_gen(),name=self.name_gen(i),uid=self.uniq_id(i),cid='|0|')) 
        tx.commit()
        return self.graph
    
    def Relation(self, path, itr_limit=1000):
        gen = self.__giveout(path, itr_limit, overrite=True)
        dict_nodes = next(gen)
        while True:
            for key, vals in dict_nodes.items():
                self.graph.run(self.create(what='relation', label=self.label_gen(), uid=key, sets=str(vals)))
            dict_nodes = next(gen)
            if dict_nodes == None:
                print("The Job is Complete")
                break
        return None
    
    def gen_adj_list(self, itr_limit, path):
        gen = self.__giveout(path, itr_limit, overrite=True)
        dict_nodes = next(gen)
        with open('Adj_list' + '_' + self.label_gen() + '.json', 'w') as fp:
             json.dump(dict_nodes, fp)
        return dict_nodes
        
    def __giveout(self, path, itr_limit, overrite=False):
        with open(path) as fp:
            elements = fp.readline().strip().split(" ")
            dict_nodes = dict()
            if overrite:
                itr_limit=int(elements[1])
            for j in range(1, int(elements[1])+1):
                nodes = list(map(int, fp.readline().strip().split(" ")))
                nodes = [self.uniq_id(nodes[0]),self.uniq_id(nodes[1])]
                if nodes[0] in dict_nodes:
                    dict_nodes[nodes[0]].append(nodes[1])
                else:
                    dict_nodes[nodes[0]] = [nodes[1]]
                if nodes[1] in dict_nodes:
                    dict_nodes[nodes[1]].append(nodes[0])
                else:
                    dict_nodes[nodes[1]] = [nodes[0]]
                    
                if j%itr_limit==0:
                    print(j)
                    yield dict_nodes
                    dict_nodes = dict()
                    sets = set()       
            yield dict_nodes
            yield None
                    

        
        
