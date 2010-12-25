Introduction
============

delicious2google is a simple Python Google App Engine-based tool to export [Delicious](http://www.delicious.com/) bookmarks to [Google Bookmarks](http://www.google.com/bookmarks). It uses the V2 Delicious API (with OAuth) for accounts that have been merged with Delicious accounts, or the V1 API (Basic Auth over HTTPS) for accounts that have not been merged.

There is a running instance at [http://delicious-export.appspot.com/](http://delicious-export.appspot.com/).

### Code Organization

The App Engine app lives in the `app` directory.

### OAuth Keys

The OAuth application keys should live in a `oauthkeys.py` file inside of `app`. The file should define three variables, `CONSUMER_KEY`, `CONSUMER_SECRET` and `APPLICATION_ID`. If you'd like to run your own instance of the application, you can get your own values from the [Yahoo! APIs Dashboard](https://developer.apps.yahoo.com/dashboard/createKey.html).
