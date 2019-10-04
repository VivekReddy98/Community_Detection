import sys,os,json,re
from py2neo import Graph, Node, Relationship, Database
from py2neo.matching import NodeMatcher
from py2neo.database import Schema

class RaRe(Graph):
    def __init__(self, graph, qry_jsn_path=None):
        self.graph = graph
        self.query_dict = json.load(qry_jsn_path)

    def parse_query(self, query=None):
        

    def PageRank(self, in_mem=false):
        '''
        Returns a Cursor Object to the Page Rank results
        if in_mem = true, a list of dicts in returned
        '''
        if (not(in_mem)):
            tx = self.graph.begin()
            cursor = tx.run(self.query['PageRank'])
            return cursor 
        else:
            tx = self.
