import eventlet
import socketio

from Parser import Parser

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.on('parse')
def parse(sid, data):
    # if sid not in servers.keys():
    #     servers[sid] = Server(sid)
    # status = servers[sid].serve(data)
    # if status==TEARDOWN:
    #     servers.pop(sid)
    print(f"---------- Data recieved {data}")
    parser = Parser()
    sio.emit('parse', {'data':parser(data)})
    
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 1410)), app)