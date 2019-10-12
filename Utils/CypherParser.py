import re

class Parse(object):
    def __init__(self, json_map,  Regex_dict):
        self.regex = Regex_dict
        self.json_map = json_map

    def create(self, what, **kwargs):
        line = self.json_map['create'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line
    
    def remove(self, what, **kwargs):
        line = self.json_map['remove'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line
 
    def page_rank(self, what='query_write', **kwargs):
        line = self.json_map['PageRank'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line
    
    def match(self, what='list_match', **kwargs):
        line = self.json_map['match'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line
    
    def match_unique(self, what='property',**kwargs):
        line = self.json_map['unique'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line
    
    def cluster(self, what='ask',**kwargs):
        line = self.json_map['cluster'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line
    
    def CC(self, what='query_write', **kwargs):
        line = self.json_map['CC'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line
    
    def conductance(self, what, **kwargs):
        line = self.json_map['conductance'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line

class ID_generator(object):
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
        return '_'+self.di[self.cat]+self.di[self.var]+index
    
    def gen_cluster_id(self, i, prev=None):
        if prev==None:
            return '|' + str(i) + '|'
        else:
            return prev+str(i)+'|'


#Examples of using Parse()
#Id = ID_generators('amazon', 'small', di)
# print(parse.create(what='node', uid=Id.uniq_id(0), label=Id.label_gen(), name=Id.name_gen(0), cluster=Id.gen_cluster_id(0)))
# print(parse.create(what='relation', src=Id.uniq_id(0), dst=Id.uniq_id(0), relation='KNOWS'))
# print(parse.create(what='index', label=Id.label_gen(), index='uid'))
# print(parse.page_rank(what='query_write', label=Id.label_gen(), relation='KNOWS', PR_itr='20', PR_df = '0.85'))