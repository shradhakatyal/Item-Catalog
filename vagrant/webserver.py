from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                rows = session.query(Restaurant.name).all()
                output += "<html><body>"
                for row in rows:
                    output += '<div>' + str(row.name) + '</div>'
                    output += '<a href="#">edit</a>'
                    output += '&emsp;'
                    output += '<a href="#">delete</a>'
                
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            
            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += " <h1>Make a new restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                    action='/restaurants'><input name='restaurant-name' type='text' >
                    <input type='submit' value='Create' ></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
        except IOError:
            self.send_error(404, "File not Found %s" % self.path)
    
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                restaurantname = fields.get('restaurant-name')

            restaurantnew = Restaurant(name=restaurantname[0])
            session.add(restaurantnew)
            session.commit()
            self.do_GET()

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print ("Web server running on %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C entered, stopping web server...')
        server.socket.close()


if __name__ == '__main__':
    main()