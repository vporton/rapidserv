"""
"""

from rapidserv import RapidServ, make, CLOSE, WebSocket
from chat import chatserver

app = RapidServ(__file__)

@app.request('GET /')
def send_base(con, request):
    con.render('base.jinja', )
    con.done()

@app.request('GET /chat')
def chat(con, request):
    con.handshake(request)
    chatserver.add_user(con)

if __name__ == '__main__':

    app.run()
    



