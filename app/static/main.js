function xmlEscape(str) {
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
}
 
function jsonCallback(bookmarks) {	  
  var dataNode = document.getElementById('data');
  
  var bookmarksXml = [];
  
  for (var i = 0, bookmark; bookmark = bookmarks[i]; i++) {
    bookmarksXml.push(
      '<bookmark>',
        '<url>', xmlEscape(bookmark.u || ''), '</url>',
        '<title>', xmlEscape(bookmark.d || ''), '</title>',
        '<annotation>', xmlEscape(bookmark.e || ''), '</annotation>');
    
    if (bookmark.t) {
      var xmlTags = [];
      for (var j = 0; j < bookmark.t.length; j++) {
        var tag = bookmark.t[j];
        if (tag.length > 1 && tag.charAt(tag.length - 1) == ',') {
          tag = tag.substring(0, tag.length - 1);
        }
        xmlTags.push(xmlEscape(tag));
      }
      bookmarksXml.push('<labels><label>', 
                        xmlTags.join(','), 
                        '</label></labels>');
    }
    
    bookmarksXml.push('</bookmark>');
  }
  
  // Split XML processing instruction across name and value in an ugly
  // hack to do something with the equals sign in the POST data.
  dataNode.name = '<?xml version';
  dataNode.value = [
    '"1.0" encoding="utf-8"?>',
    '<bookmarks>',
      bookmarksXml.join(''),
    '</bookmarks>'].join('');
    
  var formNode = document.getElementById('upload-form');
  formNode.action += '&zx=' + Math.round(65535 * Math.random());
  formNode.submit();
}
