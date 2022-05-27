import pandas as pd
from nltk import CFG, ChartParser

class Parser:
    def __init__(self):
        self.cp = ChartParser(CFG.fromstring("""
            S   ->  CN VN | CN |  VN | OTH S | S OTH
            CN  ->  DN | P | CN OTH
            VN  ->  DDN DN | DDN S | DDN | TN DN | TN S | TN

            DN  ->  DN P | DN N | N DN | L DN | N | P | L | OTH DN | DN OTH
            DDN ->  V TN | DDN V | V | DDN OTH | OTH
            TN  ->  TN A | A | TN OTH | OTH TN

            N   ->  'N'
            V   ->  'V'
            A   ->  'A'
            P   ->  'P'
            L   ->  'L'
            OTH ->  'OTH'
        """))
        self.tags_name = {
            'CN': 'Chu ngu', 
            'VN': 'Vi ngu', 
            'DN': 'Danh ngu', 
            'DDN': 'Dong ngu',
            'TN': 'Tinh ngu',
            'N': 'Danh tu',
            'V': 'Dong tu',
            'A': 'Tinh tu',
            'P': 'Dai tu',
            'L': 'So tu/Luong tu',
            'OTH': 'Khac'
        }
        self.complex_tags = ['CN', 'VN', 'DN', 'DDN', 'TN']
        self.pos_dict = self.init_pos_dict()
        
    def init_pos_dict(self):
        df = pd.read_csv('kriem_pos.csv')
        pos_simple = {
            'Adjective': 'A', 
            'Unit noun': 'N',
            'Noun': 'N',
            'Verb': 'V',
            'Pronoun': 'P',
            'Numeral/Quantity': 'L',
            'Classifier noun': 'L',
            'Determiner': 'L'
        }
        pos_dict = dict(
            [(i,pos_simple.setdefault(j, 'OTH')) 
            for i,j in zip(df['Bahnaric'], df['PoS tag'])])
        return pos_dict
    
    def pos_tag(self, word):
        return self.pos_dict.setdefault(word, 'OTH')
        
    
    def preprocess_tag(self, pos_tag):
        pos_tag_dict = {
            'Np': 'N', 'Nc': 'N', 'Nu': 'N', 'N': 'N', 'Ny': 'N', 'Nb': 'N',
            'V': 'V', 'Vb': 'V',
            'A': 'A',
            'P': 'P',
            'L': 'L', 'M': 'L',
        }
        return pos_tag_dict.setdefault(pos_tag, 'OTH')
    
    def preorder_postprocess(self, tree, args={}):
        root = tree[0]
        children = tree[1:]
        ret_tree = tuple([root])
        for child in children:
            if type(child[1]) is tuple:
                ret_tree += tuple([self.preorder_postprocess(child, args)])
            else:
                if len(args['init_tags'])==0: break
                ret_tree += tuple([args['init_tags'][0]])
                args['init_tags'] = args['init_tags'][1:]
        return ret_tree
    
    def pipeline(self, init_text):
        ### translate to Viet
        text = init_text
        
        init_pos_tags = [self.pos_tag(i) for i in text.split(' ')]
        pos_tags = [self.preprocess_tag(i) for i in init_pos_tags]
        # print(pos_tags)       
        tree_str = [str(i) for i in self.cp.parse(pos_tags)][0]
        tree = eval(','.join(tree_str.split()),  dict([(i,i) for i in ['S', 'CN', 'VN', 'DDN', 'DN', 'TN', 'N', 'V', 'A', 'P', 'L', 'OTH'] ])   )
        init_tags = [i for i in zip(init_pos_tags,text.split(' '))]

        tree_str = [str(i) for i in self.cp.parse(pos_tags)][0]
        tree = eval(','.join(tree_str.split()),  dict([(i,i) for i in ['S', 'CN', 'VN', 'DDN', 'DN', 'TN', 'N', 'V', 'A', 'P', 'L', 'OTH'] ])   )
        init_tags = [i for i in zip(init_pos_tags,init_text.split(' '))]

        return self.preorder_postprocess(tree, {'init_tags':init_tags})
    
    def preorder_get_text(self, tree):
        children = tree[1:]
        res = []
        for child in children:
            if type(child) is tuple:
                res += self.preorder_get_text(child)
            else:
                res += [child]
        return res
        
    def preorder_result(self, tree):
        root = tree[0]
        children = tree[1:]
        
        res = [(root, self.preorder_get_text(tree))]
        
        for child in children:
            if type(child) is tuple:
                res += self.preorder_result(child)
        return res
    
    def __call__(self, text):
        ### return 2 objs, 1 for complex tags, 1 for simple tags
        tree = self.pipeline(text)
        print(tree)
        result = self.preorder_result(tree)
        return (
            [
                {'key':self.tags_name[i], 'val':' '.join(j)} 
                for i,j in result if i in self.complex_tags
            ],
            [
                {'key':self.tags_name[i], 'val':' '.join(j)} 
                for i,j in result if i not in self.complex_tags and i!='S'
            ]
        )