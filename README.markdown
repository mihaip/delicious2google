Introduction
============

delicious2google is a simple Python Google App Engine-based tool to export [Delicious](http://www.delicious.com/) bookmarks to [Google Bookmarks](http://www.google.com/bookmarks). It uses the V2 Delicious API (with OAuth) for accounts that have been merged with Delicious accounts, or the V1 API (Basic Auth over HTTPS) for accounts that have not been merged.

There is a running instance at [http://delicious-export.appspot.com/](http://delicious-export.appspot.com/).

### Code Organization and Design

The App Engine app lives in the `app` directory. There are a few endpoints (only the first two are exposed by `static/index.html`):

* `/basic-auth`: Uses the V1 HTTP Basic Auth API endpoint which fetches the bookmarks and export them given the user's credentials (implemented by `BasicAuthUploadHandler` in `main.py`)
* `/request-authorization`: Does the complete OAuth authorization flow and exports the fetched bookmarks (implemented by `RequestAuthorizationHandler` and `OAuthCallbackHandler` in `main.py`)
* `/debug-token.html`: Given an OAuth [access token](http://tools.ietf.org/html/rfc5849#section-2.3) that has already been fetched, fetches the bookmarks and exports them (implemented by `DebugTokenHandler` in `main.py`)
* `/json.html`: Uses the Delicious API JSON endpoint to request publicly-visible data (for any user) and uploads it (implemented by `static/json.html`). Useful for debugging user requests (assuming that the problem is with the first 100 bookmarks)

Exporting is done by generating a JSON dump that mimics the Delicious API JSON "raw" output (not necessary for the debug JSON endpoint, since we already have JSON data there) then pointing `jsonCallback` from `static/main.js` at it. That creates a form in which it fills in the bookmark XML data that the Google Bookmarks [bulk import endpoint](https://www.google.com/bookmarks/mark?op=upload) accepts.

### OAuth Keys

The OAuth application keys should live in a `oauthkeys.py` file inside of `app`. The file should define three variables, `CONSUMER_KEY`, `CONSUMER_SECRET` and `APPLICATION_ID`. If you'd like to run your own instance of the application, you can get your own values from the [Yahoo! APIs Dashboard](https://developer.apps.yahoo.com/dashboard/createKey.html).
