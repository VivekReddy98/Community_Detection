import re, json

def gen_dict():
    Regex_dict = {}
    Regex_dict['label'] = ['<label>']
    Regex_dict['uid'] = ['<uid>']
    Regex_dict['name'] = ['<name>']
    Regex_dict['cluster'] = ['<cluster>']
    Regex_dict['relation'] = ['<rltn>']
    Regex_dict['index'] = ['<index>']
    Regex_dict['PR_iterations'] = ['<itr>']
    Regex_dict['PR_dampingFactor'] = ['<df>']
    return Regex_dict

with open('query.json') as json_file:
    text = json_file.read()
    json_data = json.load(text)

class Parse():
    def __init__(self, Regex_dict=gen_dict(), json_map=json_data):
        self.regex = Regex_dict
        self.json_map = json_map

    def create(self, what='node', **kwargs):
        line = self.json_map['create'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line
    
    def page_rank(self, what='query_write', **kwargs):
        line = self.json_map['page_rank'][what]
        for key, value in kwargs.items():
            line = re.sub(self.regex[key],value,line)
        return line