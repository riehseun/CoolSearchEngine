from bottle import route, run, request, static_file, post
import PageRank
import crawler
from crawler import *

def links(query):
    text=[]
    f=open('./results.txt','w')#wipes out results from previous query in order to prevent those results from adding to a new user query    
    f.write('<p style="font-family:FreeSans;font-size:120%;color:black">')
    f.close()#inserts a line of code that displays the text result in the format named FreeSans at 1.2 times the original size before closing the file.
    PageRank.search(query)#calls the query function in PageRank.py that computes and stores the results in "results.txt"
    f = open("./results.txt")
    f2=open('./numbers.txt')#contains the total number of results for the user's inputted query
    for line in f:#reads text file and copies contents onto a tuple (named 'text'), with each element of the tuple representing one line in the textfile.
	word = line.strip()
	text.append(word)
    f.close()
    for line in f2:#reads the number of results determined and saves it onto a vvariable named 'word2'.
	word2 = line.strip()
    f.close() 
    html = '<p style="font-family:FreeSans;font-size:120%;color:black">'+"Your query '"+query+"' returned the following "+word2+" result(s):<br/>"
    if(query.find(' ')==1):
	html=html+"NOTE: Since you typed MORE THAN ONE keyword, the following results may not be acurate.<br/>"
    html=html+"<br/>"
    html=html+"<br/>".join(text)    
    return html#displays results to the user

@route("/search")#displays the home page, which contains the welcome message and a blank where they can fill their desired query
def home():
    f = open("head.html")
    html = "".join(f.readlines())
    return html

@post("/query")#causes the computer to open up another page before calling the "links" function above that display the result(s) of the user's query
def query():
    query=request.forms.get("name")    
    return links(query)

@route("/static/<filename>")
def static(filename):
    return static_file(filename, root="./")





run(host="localhost", port=8080, debug=True)
