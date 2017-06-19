from rapidlib.requests import get, HttpResponseHandle
from untwisted.network import xmap, core
from untwisted import iossl

def on_done(con, response):
    print response.headers
    print response.code
    print response.version
    print response.reason 
    print response.fd.read()

if __name__ == '__main__':
    con = get('docs.python.org', 443, '/3/', ssl=True)

    xmap(con, HttpResponseHandle.HTTP_RESPONSE, on_done)
    core.gear.mainloop()


