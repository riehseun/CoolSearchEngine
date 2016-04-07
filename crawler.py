
# Copyright (C) 2011 by Peter Goodman
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import urllib2
import urlparse
from BeautifulSoup import *
from collections import defaultdict
import re
import shelve

def attr(elem, attr):
    """An html attribute from an html element. E.g. <a href="">, then
    attr(elem, "href") will get the href or an empty string."""
    try:
        return elem[attr]
    except:
        return ""

WORD_SEPARATORS = re.compile(r'\s|\n|\r|\t|[^a-zA-Z0-9\-_]')

class crawler(object):
    """Represents 'Googlebot'. Populates a database by crawling and indexing
    a subset of the Internet.

    This crawler keeps track of font sizes and makes it simpler to manage word
    ids and document ids."""

    def __init__(self, db_conn, url_file):
        """Initialize the crawler with a connection to the database to populate
        and with the file containing the list of seed URLs to begin indexing."""
        self._url_queue = [ ]
        self._doc_id_cache = { }
        self._word_id_cache = { }
        
        # functions to call when entering and exiting specific tags
        self._enter = defaultdict(lambda *a, **ka: self._visit_ignore)
        self._exit = defaultdict(lambda *a, **ka: self._visit_ignore)

        # add a link to our graph, and indexing info to the related page
        self._enter['a'] = self._visit_a

        # record the currently indexed document's title an increase
        # the font size
        def visit_title(*args, **kargs):
            self._visit_title(*args, **kargs)
            self._increase_font_factor(7)(*args, **kargs)

	# catches meta tags and visits
	def visit_meta(*args, **kargs):
	    self._visit_meta(*args, **kargs)
	    self._increase_font_factor(5)(*args, **kargs)

        # increase the font size when we enter these tags
        self._enter['b'] = self._increase_font_factor(2)
        self._enter['strong'] = self._increase_font_factor(2)
        self._enter['i'] = self._increase_font_factor(1)
        self._enter['em'] = self._increase_font_factor(1)
        self._enter['h1'] = self._increase_font_factor(7)
        self._enter['h2'] = self._increase_font_factor(6)
        self._enter['h3'] = self._increase_font_factor(5)
        self._enter['h4'] = self._increase_font_factor(4)
        self._enter['h5'] = self._increase_font_factor(3)
        self._enter['title'] = visit_title
	self._enter['meta'] = visit_meta

        # decrease the font size when we exit these tags
        self._exit['b'] = self._increase_font_factor(-2)
        self._exit['strong'] = self._increase_font_factor(-2)
        self._exit['i'] = self._increase_font_factor(-1)
        self._exit['em'] = self._increase_font_factor(-1)
        self._exit['h1'] = self._increase_font_factor(-7)
        self._exit['h2'] = self._increase_font_factor(-6)
        self._exit['h3'] = self._increase_font_factor(-5)
        self._exit['h4'] = self._increase_font_factor(-4)
        self._exit['h5'] = self._increase_font_factor(-3)
        self._exit['title'] = self._increase_font_factor(-7)
	self._exit['meta'] = self._increase_font_factor(-5)

        # never go in and parse these tags
        self._ignored_tags = set([
            'script', 'link', 'embed', 'iframe', 'frame', 
            'noscript', 'object', 'svg', 'canvas', 'applet', 'frameset', 
            'textarea', 'style', 'area', 'map', 'base', 'basefont', 'param',
        ])

        # set of words to ignore
        self._ignored_words = set([
            '', 'the', 'of', 'at', 'on', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
        ])

        # keep track of some info about the page we are currently parsing
        self._curr_depth = 0
        self._curr_url = ""
        self._curr_doc_id = 0
        self._font_size = 0
        self._curr_words = None
        self._next_doc_id = 0
        self._next_word_id = 0

        # get all urls into the queue
        try:
            with open(url_file, 'r') as f:
                for line in f:
                    self._url_queue.append((self._fix_url(line.strip(), ""), 0))
        except IOError:
            pass
    
    def word_id(self, word):
        """Get the word id of some specific word."""
        if word in self._word_id_cache:
            return self._word_id_cache[word]
        
        # Done: 1) add the word to the lexicon, if that fails, then the
        #          word is in the lexicon
        #       2) query the lexicon for the id assigned to this word, 
        #          store it in the word id cache, and return the id.

        worddb=shelve.open('worddb')
        if worddb.has_key(str(word)):
            word_id = worddb[str(word)]
        else:
            worddb[str(word)] = self._next_word_id
            word_id = self._next_word_id
            self._next_word_id += 1
        self._word_id_cache[word] = word_id
        worddb.close()
        return word_id
    
    def document_id(self, url):
        """Get the document id for some url."""
        if str(url) in self._doc_id_cache:
            return self._doc_id_cache[str(url)]
        
        # Done: just like word id cache, but for documents. if the document
        #       doesn't exist in the db then only insert the url and leave
        #       the rest to their defaults.
        docdb=shelve.open('docdb')
        db=shelve.open('db')
        if docdb.has_key(str(url)):
            doc_id = docdb[str(url)]
        else:
            docdb[str(url)] = self._next_doc_id
            doc_id = self._next_doc_id
            self._next_doc_id += 1
        
       # storing validity to the database
        self._doc_id_cache[url] = doc_id
        db['doc_id:%s:isvalid' % doc_id] = True
        docdb.close()
        db.close()
        return doc_id
    
    def _fix_url(self, curr_url, rel):
        """Given a url and either something relative to that url or another url,
        get a properly parsed url."""

        rel_l = rel.lower()
        if rel_l.startswith("http://") or rel_l.startswith("https://"):
            curr_url, rel = rel, ""
            
        # compute the new url based on import 
        curr_url = urlparse.urldefrag(curr_url)[0]
        parsed_url = urlparse.urlparse(curr_url)
        return urlparse.urljoin(parsed_url.geturl(), rel)

    def add_link(self, from_doc_id, to_doc_id):
        # adding links to the database.
        db = shelve.open('db')
        if db.has_key('doc_id:%s:links' % from_doc_id):
            db['doc_id:%s:links' % from_doc_id].append((from_doc_id, to_doc_id))
        else:
            db['doc_id:%s:links' % from_doc_id] = [(from_doc_id, to_doc_id)]
        db.close()

    def _visit_title(self, elem):
        """Called when visiting the <title> tag."""
        title_text = self._text_of(elem).strip()
        print "document title="+ str(title_text)
        # stores the title of the page into the database
        db = shelve.open('db')
        db['doc_id:%s:title' % self._curr_doc_id] = title_text
        db.close()

    def _shape_meta(self, elem):
	# shapes and extracts the description tag and the keywords tag
	elemstr = str(elem)
	if ("description" in elem) or ("keywords" in elem):
		if elem.find('" name="desctiption') > 0:
			return elem[elemstr.find("content=")+9:elem.find('"')]
		elif elem.find('" />') > 0:
			return elem[elemstr.find("content=")+9:elem.find('" />')]
		elif elem.find('"/>') > 0:
			return elem[elemstr.find("contetn=")+9:elem.find('"/>')]

    def _visit_meta(self, elem):
	# stores the description tag and the keywords tag into the database
	db = shelve.open('db')
	elemstr = str(elem)
	if "description" in elemstr:
		db['doc_id:%s:desc' % self._curr_doc_id] = self._shape_meta(elemstr)
	elif "keywords" in elemstr:
		db['doc_id:%s:keywords' % self._curr_doc_id] = self._shape_meta(elemstr)

    def add_alt(self, doc_id, alt, text):
	# adds alt tag and text tag into the database
        db = shelve.open('db')
        if db.has_key('doc_id:%s:alt' % doc_id):
            db['doc_id:%s:alt' % doc_id].append((alt, text))
        else:
            db['doc_id:%s:alt' % doc_id] = [(alt, text)]
        db.close()

    def _visit_a(self, elem):
        """Called when visiting <a> tags."""
        
        dest_url = self._fix_url(self._curr_url, attr(elem,"href"))
        self._url_queue.append((dest_url, self._curr_depth))
        self.add_link(self._curr_doc_id, self.document_id(dest_url))

        # adds alt tag (alt, text)
	if (len(attr(elem, "alt")) > 0) or (len(attr(elem, "alt")) > 0):
	        self.add_alt(self._curr_doc_id, attr(elem, "alt"), attr(elem, "text"))

        
    def _getword(self, word_id):
	# takes word id as an argument and returns the corresponding word (string)
	worddb = shelve.open('worddb')
	a = worddb.items() #converting dictionary into a list of tupples
	for i in a:
		if i[1] == word_id:
			return str(i[0])
    
    def _add_words_to_document(self):
        # DONE: knowing self._curr_doc_id and the list of all words and their
        #       font sizes (in self._curr_words), add all the words into the
        #       database for this document
	# Also, if the description tag was not there, adds first 10 words into the description database
	# so that the result can show 'some description' of the page

        print "    num words="+ str(len(self._curr_words))
        db = shelve.open('db')
        db['doc_id:%s:words' % self._curr_doc_id] = self._curr_words
	if not db.has_key('doc_id:%s:desc' % self._curr_doc_id):
		temp = ''
		i = 0
		while i < len(self._curr_words):
			temp = temp + self._getword(self._curr_words[i][0])+ ' '
			i+=1
			if i > 9:
				break
		db['doc_id:%s:desc' % self._curr_doc_id] = temp
        db.close()

    def _increase_font_factor(self, factor):
        """Increade/decrease the current font size."""
        def increase_it(elem):
            self._font_size += factor
        return increase_it
    
    def _visit_ignore(self, elem):
        """Ignore visiting this type of tag"""
        pass

    def _add_text(self, elem):
        """Add some text to the document. This records word ids and word font sizes
        into the self._curr_words list for later processing."""

        words = WORD_SEPARATORS.split(elem.string.lower())
        for word in words:
            word = word.strip()
            if word in self._ignored_words:
                continue
            self._curr_words.append((self.word_id(word), self._font_size))
        
    def _text_of(self, elem):
        """Get the text inside some element without any tags."""
        if isinstance(elem, Tag):
            text = [ ]
            for sub_elem in elem:
                text.append(self._text_of(sub_elem))
            
            return " ".join(text)
        else:
            return elem.string

    def _index_document(self, soup):
        """Traverse the document in depth-first order and call functions when entering
        and leaving tags. When we come accross some text, add it into the index. This
        handles ignoring tags that we have no business looking at."""
        class DummyTag(object):
            next = False
            name = ''
        
        class NextTag(object):
            def __init__(self, obj):
                self.next = obj
        
        tag = soup.html
        stack = [DummyTag(), soup.html]
        while tag and tag.next:
            tag = tag.next

            # html tag
            if isinstance(tag, Tag):

                if tag.parent != stack[-1]:
                    self._exit[stack[-1].name.lower()](stack[-1])
                    stack.pop()

                tag_name = tag.name.lower()

                # ignore this tag and everything in it
                if tag_name in self._ignored_tags:
                    if tag.nextSibling:
                        tag = NextTag(tag.nextSibling)
                    else:
                        self._exit[stack[-1].name.lower()](stack[-1])
                        stack.pop()
                        tag = NextTag(tag.parent.nextSibling)
                    
                    continue
                
                # enter the tag
                self._enter[tag_name](tag)
                stack.append(tag)

            # text (text, cdata, comments, etc.)
            else:
                self._add_text(tag)

    def crawl(self, depth=2, timeout=3):
        """Crawl the web!"""
        seen = set()

        while len(self._url_queue):

            url, depth_ = self._url_queue.pop()

            # skip this url; it's too deep
            if depth_ > depth:
                continue

            doc_id = self.document_id(url)

            # we've already seen this document
            if doc_id in seen:
                continue

            seen.add(doc_id) # mark this document as haven't been visited
            
            socket = None
            try:
                socket = urllib2.urlopen(url, timeout=timeout)
                soup = BeautifulSoup(socket.read())
                self._curr_depth = depth_ + 1
                self._curr_url = url
                self._curr_doc_id = doc_id
                self._font_size = 0
                self._curr_words = [ ]
                self._index_document(soup)
                self._add_words_to_document()
                print "    url="+str(self._curr_url)

            except Exception as e:
                print e
                db=shelve.open('db')
                db['doc_id:%s:isvalid' % doc_id] = False
                db.close()
                pass
            finally:
                if socket:
                    socket.close()

if __name__ == "__main__":
    bot = crawler(None, "urllist.txt")
    bot.crawl(depth=1)

