#Unittest Suite

import unittest
import PageRank
import crawler
from crawler import *

class crawler_test(unittest.TestCase):
         
    def setUp(self):
        pass

    #result.txt test
    def testmethod_1(self):
	f=open("./results.txt","r")
	self.assertNotEqual(f,IOError,"Oops! File containing query results doesn't exist.")
	f.close()

    #urllist.txt test
    def testmethod_2(self):
	f=open("./urllist.txt","r")
	if (f!=IOError):
	    word = f.readline()
	    self.assertNotEqual(len(word),0,"Oops! Nothing is in the URL Links file!!!!!.")
            check=word[:7]
            self.assertEqual(check,"http://","Oops! this is NOT a URL Link!!!!!") 
	else:
	    self.assertNotEqual(IOError,IOError, "Oops! File containing URL Links doesn't exist.")
	f.close()

    #worddb test
    def testmethod_3(self):
	f=open("./worddb")
	self.assertNotEqual(f,IOError,"Oops! File doesn't exist.")
	f.close()

    #db test
    def testmethod_4(self):
	f=open("./db")
	self.assertNotEqual(f,IOError,"Oops! File doesn't exist.")
	f.close()

    #docdb test
    def testmethod_5(self):
	f=open("./db")
	self.assertNotEqual(f,IOError,"Oops! File doesn't exist.")
	f.close()
     
class search_test(unittest.TestCase):

    def setUp(self):
        pass

    #Following three tests to see whether the search function returns a list of tuple(s)
    #In all cases, it has to return a list of some elements to let the front end to
    #know how to handle each case  

    #search_test 1
    def testmethod_1(self):
        result = PageRank.search("youtube")
        self.assertNotEqual(len(result),0,"fail")

    #search_test 2
    def testmethod_2(self):
        result = PageRank.search("zhu")
        self.assertNotEqual(len(result),0,"fail")

    #search_test 3
    def testmethod_3(self):
        result = PageRank.search("shit")
        self.assertNotEqual(len(result),0,"fail")
    
    #Following three tests to see whether the corner cases are handled correctly in the
    #search function

    #search_test "bad iput"
    def testmethod_4(self):
        result = PageRank.search(".,.,.,.")
        self.assertEqual(len(result), 1, "fail")

    #search_test "blank search box"
    def testmethod_5(self):
        result = PageRank.search("") 
        self.assertEqual(len(result), 1, "fail") 

    #search_test "keywords that is not like to give result"
    def testmethod_6(self):
        result = PageRank.search("ruosyguweryiotgryu")
        self.assertEqual(len(result), 1, "fail")
        
class PageRank_test(unittest.TestCase):

    def setUp(self):
        pass

    #hits test 1  
    def testmethod_1(self):
        dic = PageRank.hits("zhu")
        result = PageRank.search("zhu")
        if result == [-1]:
            self.assertNotEqual(len(dic), 1, "fail")
        else:
            self.assertNotEqual(len(dic), 0, "fail")

    #hits test 2 
    def testmethod_2(self):
        dic = PageRank.hits("zhu")
        result = PageRank.search("zhu")
        if result == [-1]:
            self.assertNotEqual(len(dic), 1, "fail")
        else:
            self.assertNotEqual(len(dic), 0, "fail")

    #relative_font_size test 1
    def testmethod_3(self):
        dic = PageRank.relative_font_size("youtube")
        result = PageRank.search("youtube")
        if result == [-1]:
            self.assertNotEqual(len(dic), 1, "fail")
        else:
            self.assertNotEqual(len(dic), 0, "fail")
 
    #relative_font_size test 2
    def testmethod_4(self):
        dic = PageRank.relative_font_size("youtube")
        result = PageRank.search("youtube")
        if result == [-1]:
            self.assertNotEqual(len(dic), 1, "fail")
        else:
            self.assertNotEqual(len(dic), 0, "fail")

    #trim_url test 1
    def testmethod_5(self):
        result = PageRank.trim_url("http://en.wikipedia.org/wiki/Hotmail") 
        self.assertEqual(result, "wikipedia.org")

def crawler_suite():
    return unittest.TestLoader().loadTestsFromTestCase(crawler_test)

def search_suite():
    return unittest.TestLoader().loadTestsFromTestCase(search_test)

def PageRank_suite():
    return unittest.TestLoader().loadTestsFromTestCase(PageRank_test)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(crawler_suite())
    runner.run(search_suite())
    runner.run(PageRank_suite())
    
