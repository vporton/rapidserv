from rapidlib.requests import post, HttpResponseHandle
from untwisted.network import xmap, core
import json

def on_done(con, response):
    print response.fd.read()

def create():
    payload = {
    "description": "the description for this gist",
    "public": "true", "files": {
    "file1.txt": {"content": "String file contents"}}}

    con = post('api.github.com', 443, 
    '/gists', payload=json.dumps(payload), 
    headers={'content-type': 'application/json'}, ssl=True)

    xmap(con, HttpResponseHandle.HTTP_RESPONSE, on_done)

if __name__ == '__main__':
    create()
    core.gear.mainloop()








