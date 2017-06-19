from untwisted.iostd import LOAD, CLOSE, CONNECT, CONNECT_ERR, \
Client, Stdin, Stdout, lose, create_client
from untwisted.iossl import SSL_CONNECT, create_client_ssl
from untwisted.splits import AccUntil, TmpFile
from untwisted.network import Spin, xmap, spawn, zmap, SSL
from untwisted.event import get_event
from urllib import urlencode
from rapidlib import rapidserv
from tempfile import TemporaryFile as tmpfile


class Response(object):
    def __init__(self, data):
        headers                              = data.split('\r\n')
        response                             = headers.pop(0)
        self.version, self.code, self.reason = response.split(' ', 2)
        self.headers                         = rapidserv.Headers(headers)
        self.fd                              = tmpfile('a+')

class HttpTransferHandle(rapidserv.HttpTransferHandle):
    def process_request(self, spin, response, data):
        """
        """

        response = Response(response)
        spawn(spin, HttpTransferHandle.HTTP_TRANSFER, response, data)

class HttpResponseHandle(rapidserv.HttpRequestHandle):
    HTTP_RESPONSE = rapidserv.HttpRequestHandle.HTTP_REQUEST

class HttpCode(object):
    def __init__(self, spin):
        xmap(spin, HttpResponseHandle.HTTP_RESPONSE, self.process)

    def process(self, spin, response):
        pass

def on_connect(spin, request):
    AccUntil(spin)
    HttpTransferHandle(spin)

    # It has to be mapped here otherwise HttpTransferHandle.HTTP_RESPONSE
    # will be spawned and response.fd cursor will be at the end of the file.
    xmap(spin, TmpFile.DONE, 
                        lambda spin, fd, data: fd.seek(0))

    HttpResponseHandle(spin)
    spin.dump(request)

def create_con_ssl(addr, port, data):
    con = create_client_ssl(addr, port)  
    xmap(con, SSL_CONNECT,  on_connect, data)
    return con

def create_con(addr, port, data):
    con = create_client(addr, port)
    xmap(con, CONNECT,  on_connect, data)
    return con

def get(addr, port, path, args={},  headers={}, version='HTTP/1.1', ssl=False, auth=()):
    default = {
    'user-agent':"Untwisted-requests/1.0.0", 
    'accept-charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'connection':'close',
    'host': addr}

    default.update(headers)
    args = '?%s' % urlencode(args) if args else ''

    if auth: default['authorization'] = build_auth(*auth)
    data  = 'GET %s%s %s\r\n' % (path, args, version)

    for key, value in default.iteritems():
        data = data + '%s: %s\r\n' % (key, value)
    data = data + '\r\n'

    return create_con_ssl(addr, port, data) if ssl else \
        create_con(addr, port, data)

def post(addr, port, path, payload='', version='HTTP/1.1', headers={}, ssl=False, auth=()):
    """
    """

    default = {
    'user-agent':"Untwisted-requests/1.0.0", 
    'accept-charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'connection':'close',
    'host': addr,
    'content-type': 'application/x-www-form-urlencoded',
    'content-length': len(payload)}

    default.update(headers)

    request  = 'POST %s %s\r\n' % (path, version)
    if auth: default['authorization'] = build_auth(*auth)

    for key, value in default.iteritems():
        request = request + '%s: %s\r\n' % (key, value)
    request = request + '\r\n' + payload

    return create_con_ssl(addr, port, request) if ssl else \
        create_con(addr, port, request)

def build_auth(username, password):
    from base64 import encodestring
    base = encodestring('%s:%s' % (username, password))
    base = base.replace('\n', '')
    return "Basic %s" % base




