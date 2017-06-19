from rapidlib.requests import get, HttpResponseHandle
from untwisted.network import xmap, core

def on_done(con, response):
    print response.headers
    print response.code
    print response.version
    print response.reason 
    print response.fd.read()

if __name__ == '__main__':
    xmap(get('codepad.org', 80, '/'), 
    HttpResponseHandle.HTTP_RESPONSE, on_done)


    core.gear.mainloop()









