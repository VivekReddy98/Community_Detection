"""
To run this code, execute: python3 ClusterFileGenerator.py <node_label>
where:
    <node_label> is the label associated with the nodes in your neo4j database.
        Eg: amazon_small is the label associated with all the nodes that belong to the amazon.graph.small dataset.
"""

from py2neo import Graph, NodeMatcher
import sys

"""
Note: Your neo4j database address, username and password may be different if you ever changed them. Change the arguments to Graph accordingly.
"""
graph = Graph("bolt:localhost:7474", auth=("neo4j", "neo4j"))

matcher = NodeMatcher(graph)
node_name = str(sys.argv[1])
output_file_name = node_name.split("_")[0]+".lacomm."+node_name.split("_")[1]
with open(output_file_name,"w+") as f:
    c_d = 1
    while True:
        uid_list = []
        for i in list(matcher.match(node_name).where("_.C_D CONTAINS '|"+str(c_d)+"|'")):
            uid_list.append(str(int(i["uid"][5:])))
        line = " ".join(uid_list)+"\n"
        if len(uid_list)==0:
            break
        f.write(line)
        c_d = c_d + 1
