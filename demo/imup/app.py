"""

"""

from rapidserv import RapidServ, make, RequestHandle
import shelve

DB_FILENAME = 'DB'
DB          = shelve.open(make(__file__, DB_FILENAME))
RequestHandle.MAX_SIZE = 1024 * 1024 * 3
app    = RapidServ(__file__)

@app.overflow
def response(con, request):
    con.set_response('HTTP/1.1 400 Bad request')
    HTML = '<html> <body> <h1> Bad request </h1> </body> </html>'
    con.add_data(HTML)
    con.done()

@app.route('GET /')
def index(con):
    con.render('view.jinja', posts = DB.iterkeys())
    con.done()

@app.route('GET /load_index')
def load_index(con, index):
    con.add_data(DB[index[0]], mimetype='image/jpeg')
    con.done()

@app.route('POST /add_image')
def add_image(con, file):
    DB[file.filename] = file.file.read()
    index(con)

if __name__ == '__main__':
    app.run()







