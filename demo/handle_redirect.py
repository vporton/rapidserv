from rapidlib.requests import get, HttpResponseHandle
from untwisted.network import xmap, core
import sys

def on_done(con, response):
    print response.headers
    print response.code
    print response.version
    print response.reason 
    print response.fd.read()

def create_connection(addr):
    con = get(addr, '/', ssl=True)
    xmap(con, '200', on_done)
    return con

if __name__ == '__main__':
    redirect = lambda con, response: \
    create_connection(response.headers['location'])

    con = create_connection('https://www.bol.com.br')
    xmap(con, '302', redirect)
    xmap(con, '301', redirect)

    core.gear.mainloop()








