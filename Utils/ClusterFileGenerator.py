from py2neo import Graph, NodeMatcher
from Utils.CypherParser import ID_generator
'''
Given a graph with some generated cluster ID's in the format specified in CypherParser.py, 
this class is used to generate a a text file of communities identified in the preditions folder.
'''
class ClusterFileGenerator(ID_generator):
    
    def __init__(self, graph, out_dir="predictions/"):
        self.graph = graph
        self.graph = graph
        self.out_dir = out_dir
    
    def genFile(self, cat, var, num_clusters, is_LA_output=True):
        self.cat = cat
        self.var = var
        node_name = self.label_gen()
        name = node_name.split("_")
        matcher = NodeMatcher(self.graph)
        if is_LA_output:
            output_file_name = name[0]+".LApred."+name[1]
        else:
            output_file_name = name[0]+".ISpred."+name[1]
        print("The file will be written to {}".format(self.out_dir+output_file_name))
        with open(self.out_dir+output_file_name,"w+") as f:
            c_d = 0
            for i in range(0,num_clusters):
                c_d = c_d + 1
                uid_list = []
                for i in list(matcher.match(node_name).where("_.C_D CONTAINS '|"+str(c_d)+"|'")):
                    uid_list.append(str(int(i["uid"][3:])))
                line = " ".join(uid_list)+"\n"
                if len(uid_list)==0:
                    continue
                f.write(line)
                
            
        
    