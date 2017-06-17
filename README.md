# rapidserv
A micro web framework.

Rapidserv is a micro web framework that is built on top of a powerful asynchronous networking library. It shares with flask
some similarities in the design of the applications that are built on top of Rapidserv. Rapidserv is non blocking network I/O
consequently it can scale a lot of connections and it is ideal for some applications. 
Rapidserv uses jinja2 although it doesn't enforce the usage.

A basic rapidserv web application.

~~~python
from untwisted.plugins.rapidserv import RapidServ, core

app = RapidServ(__file__)

@app.request('GET /')
def send_base(con, request):
    con.add_data('<html> <body> <p> Rapidserv </p> </body> </html>')
    con.done()

if __name__ == '__main__':
    app.bind('0.0.0.0', 80, 50)
    core.gear.mainloop()
~~~


