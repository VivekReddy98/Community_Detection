import sys,os
from py2neo import Graph, Node, Relationship, Database
from py2neo.matching import NodeMatcher
from py2neo.database import Schema

class ID_generators(object):
    def __init__(self, category, variant, dict_identify):
        self.cat = category
        self.var = variant
        self.di = dict_identify
        
    def label_gen(self):
        return self.cat+"_"+self.var
    
    def name_gen(self,i):
        return self.cat+"_"+self.var+"_"+str(i)
    
    def uniq_id(self, i):
        index = str(i)
        index = ''.join(["0" for i in range(0,6-len(index))]) + index
        return int(di[self.cat]+di[self.var]+index)

if __name__ == "__main__":
    category = ['amazon', 'dblp', 'youtube']
    variant = ['small', 'medium', 'large'] #omitted original for now
    di = {'amazon':'1', 'dblp':'2', 'youtube':'3', 'small':'4', 'medium':'5', 'large':'6'}
    
    parent_dir = os.environ['GDMPATH']  #set this variable in your local environment
    #graph = Graph("bolt:localhost:7474", auth=("neo4j", "xxxxxx")) #Use your password.
    schema = Schema(graph) #Schema definition is optional in neo4j
    findNode = NodeMatcher(graph) 
    
    #For creating node labels
    for cat in category:
        for var in variant:
            filename = "datasets/{}/{}.graph.{}".format(cat, cat, var)
            ID = ID_generators(cat,var,di)
            tx = graph.begin()
            with open(parent_dir+filename) as fp:
                elements = fp.readline().strip().split(" ")
                for i in range(0, int(elements[0])):
                    tx.create(Node(ID.label_gen(), name=ID.name_gen(i),uid=ID.uniq_id(i),cluster=0))
                tx.commit()
            schema.create_index(ID.label_gen(), 'uid')
            print(filename)  
            
    #For creating node relationships
    for cat in category:
        for var in variant:
            filename = "datasets/{}/{}.graph.{}".format(cat, cat, var)
            ID = ID_generators(cat,var,di)
            tx = graph.begin()
            with open(parent_dir+filename) as fp:
                elements = fp.readline().strip().split(" ")
                for j in range(0, int(elements[1])):
                    nodes = fp.readline().strip().split(" ")
                    Node1 = findNode.match(ID.label_gen(), uid=ID.uniq_id(int(nodes[0]))).first()
                    Node2 = findNode.match(ID.label_gen(), uid=ID.uniq_id(int(nodes[1]))).first()
                    tx.create(Relationship(Node1, "KNOWS", Node2))
                    tx.create(Relationship(Node2, "KNOWS", Node1))
                tx.commit()
            print(filename)
    
    
