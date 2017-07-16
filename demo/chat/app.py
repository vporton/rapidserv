"""
"""

from rapidserv import RapidServ, make, CLOSE, WebSocket
import sqlite3
import struct

app = RapidServ(__file__)

@app.request('GET /')
def send_base(con, request):
    con.render('base.jinja', )
    con.done()

class ChatServer(object):
    def __init__(self):
        self.pool = []

    def add_user(self, con):
        con.add_map(CLOSE, self.on_close)
        con.add_map(WebSocket.LOAD, self.echo_msg)
        self.pool.append(con)

    def echo_msg(self, con, data):
        for ind in self.pool:
            ind.wsdump(data)

    def on_close(self, con, err):
        self.pool.remove(con)
        print 'Client closed!'

chatserver = ChatServer()

@app.request('GET /chat')
def add_quote(con, request):
    con.handshake('SimpleChat', request.headers['sec-websocket-key'])
    WebSocket(con)
    chatserver.add_user(con)

if __name__ == '__main__':

    app.run()
    


