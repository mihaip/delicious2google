from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class FaviconHandler(webapp.RequestHandler):
    def get(self):
      self.redirect('http://persistent.info/favicon.ico')

def main():
    application = webapp.WSGIApplication([
            ('/favicon.ico', FaviconHandler),
        ],
        debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
