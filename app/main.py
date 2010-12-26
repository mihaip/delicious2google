import base64
import cgi
import logging

from django.utils import simplejson as json
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import oauthlib.oauth
import yahoo.application
import yahoo.oauth

from bookmarks import parse_bookmarks_xml
import oauthkeys

class BaseHandler(webapp.RequestHandler):
    def _handle_error(self, url_fetch_result):
        def debug(str):
            self.response.out.write(str + '\n')
            logging.debug(str)
      
        self.response.set_status(500)
        self.response.headers["Content-Type"] = "text/html"
      
        debug('<h1>Received an error from the Delicious API</h1>')
        debug('<b>Status code:</b> %d<br>' %
            url_fetch_result.status_code)
        debug('<b>Headers:</b><ul>')
        for header, value in url_fetch_result.headers.items():
            debug('<li><b>%s:</b> %s</li>' %
                (cgi.escape(header), cgi.escape(value)))
        debug('</ul>')
        debug('<b>Body:</b> <pre>%s</pre>' %
            cgi.escape(url_fetch_result.content))

    def _output_export_form(self, bookmarks):
        self.response.headers['Content-Type'] = 'text/html'
        
        out = self.response.out
        
        out.write('<script type="text/javascript" src="/main.js"></script>')
        out.write('''
              <h1>Uploading...</h1>
              <form id="upload-form"
                  action="https://www.google.com/bookmarks/mark?op=upload"
                  method="POST"
                  accept-charset="utf-8">
                <input type="hidden" name="" id="data">
              </form>
              ''')
              
        out.write('<script type="text/javascript">jsonCallback(')
    
        # Mimic the "raw" JSON output produced by the Delicious PAI    
        bookmarks_json = []
        for bookmark in bookmarks:
            tags = list(bookmark.tags)
            if bookmark.is_private:
                tags.append('delicious-private')
            tags.append('delicious-export')        
            bookmark_json = {
              'u': bookmark.href,
              'd': bookmark.description,
              'e': bookmark.extended,
              't': tags
            }
            bookmarks_json.append(bookmark_json)
    
        out.write(json.dumps(bookmarks_json, indent=2, ensure_ascii=True))
        
        out.write(')</script>')    

class OAuthHandler(BaseHandler):
    def _create_oauthapp(self):
        return yahoo.application.OAuthApplication(
            oauthkeys.CONSUMER_KEY,
            oauthkeys.CONSUMER_SECRET,
            oauthkeys.APPLICATION_ID,
            'http://delicious-export.appspot.com/oauth-callback')

    def _handle_xml_export(self, oauthapp):
        url = 'http://api.del.icio.us/v2/posts/all'
        signing_request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(
            oauthapp.consumer,
            token=oauthapp.token,
            http_method='GET',
            http_url=url)
        signing_request.sign_request(
            oauthapp.signature_method_hmac_sha1, oauthapp.consumer, oauthapp.token)
        headers = signing_request.to_header('yahooapis.com')
    
        result = urlfetch.fetch(
            url=url,
            method=urlfetch.GET,
            deadline=60,
            headers=headers)
    
        if result.status_code != 200:
            self._handle_error(result)
            return
            
        bookmarks = parse_bookmarks_xml(result.content)
        self._output_export_form(bookmarks)

class BasicAuthUploadHandler(BaseHandler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        logging.debug('Exporting bookmarks using Basic Auth for %s' % username)
        
        encoded_credentials = base64.encodestring(
            '%s:%s' % (username, password))[:-1]
        
        # The v1 API seems to be more prone to taking longer to respond (or is
        # it that v1 users tend to have more bookmarks?), so to avoid hitting
        # the 10 second HTTP urlfetch timeout limit, we chunk the data that is
        # requested
        chunk_start = 0
        chunk_size = 500
        bookmarks = []

        while True:
          logging.debug('  Fetching chunk from %d' % chunk_start)
          result = urlfetch.fetch(
              url='https://api.del.icio.us/v1/posts/all?results=%d&start=%d' %
                  (chunk_size, chunk_start),
              method=urlfetch.GET,
              deadline=60,
              headers={'Authorization': 'Basic %s' % encoded_credentials})
          
          if result.status_code != 200:
              self._handle_error(result)
              return
          
          chunk_bookmarks = parse_bookmarks_xml(result.content)
          bookmarks.extend(chunk_bookmarks)

          logging.debug('  Got %d bookmarks in chunk' % len(chunk_bookmarks))
          
          if len(chunk_bookmarks) != chunk_size:
              break
          
          chunk_start += chunk_size

        self._output_export_form(bookmarks)

class DebugTokenHandler(OAuthHandler):
    def post(self):
        oauthapp = self._create_oauthapp()
        access_token = yahoo.oauth.AccessToken.from_string(
            self.request.get('access-token'))
        oauthapp.token = access_token
        self._handle_xml_export(oauthapp)

class FaviconHandler(webapp.RequestHandler):
    def get(self):
      self.redirect('http://persistent.info/favicon.ico')

def main():
    application = webapp.WSGIApplication([
            ('/debug-token', DebugTokenHandler),
            ('/basic-auth', BasicAuthUploadHandler),            
            ('/favicon.ico', FaviconHandler),
        ],
        debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
