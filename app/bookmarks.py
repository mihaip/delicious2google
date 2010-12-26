import xml.dom.minidom

class Bookmark(object):
    def __init__(self, href, description, hash, tags, time, extended, count, shared):
        self.href = href
        self.description = description
        self.hash = hash
        if tags.strip():
            self.tags = tags.strip().split(' ')
        else:
            self.tags = []
        self.time = time
        self.extended = extended
        self.is_private = shared == 'no'
        
def parse_bookmarks_xml(xml_string):
    dom = xml.dom.minidom.parseString(xml_string)
    bookmarks = []
    for bookmark_xml in dom.getElementsByTagName('post'):
        def get_attribute(name):
            if bookmark_xml.attributes.has_key(name):
                return bookmark_xml.attributes[name].value
            return None
        
        bookmark = Bookmark(
            href=get_attribute('href'),
            description=get_attribute('description'),
            hash=get_attribute('hash'),
            tags=get_attribute('tag'),
            time=get_attribute('time'),
            extended=get_attribute('extended'),
            count=get_attribute('count'),
            shared=get_attribute('shared'))
        bookmarks.append(bookmark)
    return bookmarks        
