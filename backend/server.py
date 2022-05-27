import eventlet
import socketio
from nltk import CFG, ChartParser

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

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
    
    def pipeline(self, init_text, annotator):
        ### translate to Viet
        text = ''

        ### POS tag
        annotation = annotator.annotate(text)['sentences'][0]
        
        init_pos_tags = [i['posTag'] for i in annotation]
        pos_tags = [self.preprocess_tag(i) for i in init_pos_tags]
        # print(pos_tags)       
        tree_str = [str(i) for i in self.cp.parse(pos_tags)][0]
        tree = eval(','.join(tree_str.split()),  dict([(i,i) for i in ['S', 'CN', 'VN', 'DDN', 'DN', 'TN', 'N', 'V', 'A', 'P', 'L', 'OTH'] ])   )
        init_tags = [i for i in zip(init_pos_tags,text.split())]

        tree_str = [str(i) for i in self.cp.parse(pos_tags)][0]
        tree = eval(','.join(tree_str.split()),  dict([(i,i) for i in ['S', 'CN', 'VN', 'DDN', 'DN', 'TN', 'N', 'V', 'A', 'P', 'L', 'OTH'] ])   )
        init_tags = [i for i in zip(init_pos_tags,init_text.split())]

        return self.preorder_postprocess(tree, {'init_tags':init_tags})

@sio.on('parse')
def parse(sid, data):
    # if sid not in servers.keys():
    #     servers[sid] = Server(sid)
    # status = servers[sid].serve(data)
    # if status==TEARDOWN:
    #     servers.pop(sid)
    print(f"---------- Data recieved {data}")
    sio.emit('parse', {'data':[
        {'key': 'chu ngu', 'val': 'anh'},
        {'key': 'vi ngu', 'val': 'iu em'},
    ]})
    
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 1410)), app)