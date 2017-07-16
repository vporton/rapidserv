from rapidserv import CLOSE, WebSocket

class ChatServer(object):
    def __init__(self):
        self.pool = []

    def add_user(self, con):
        con.add_map(CLOSE, self.del_user)
        con.add_map(WebSocket.LOAD, self.echo_msg)
        self.pool.append(con)

    def echo_msg(self, con, data):
        for ind in self.pool: ind.wsdump(data)

    def del_user(self, con, reason):
        self.pool.remove(con)
        print 'Client closed!', reason

chatserver = ChatServer()



