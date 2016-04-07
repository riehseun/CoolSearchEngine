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

import operator
import crawler
import shelve
from crawler import *

extention_list = ['.arpa', '.com', '.edu', '.firm', '.gov', '.asia', '.biz', '.cat', '.info', '.museum', '.net', '.org', '.mil', '.name', '.im', '.jpn', '.mob', '.tel', '.co.ac', '.co.ad', '.co.ae', '.co.af', '.co.ag', '.co.ai', '.co.al', '.co.am', '.co.an', '.co.ao', '.co.aq', '.co.ar', '.co.as', '.co.at', '.co.au', '.co.aw', '.co.az', '.co.ba', '.co.bb', '.co.bd', '.co.be', '.co.bf', '.co.bg', '.co.bh', '.co.bi', '.co.bj', '.co.bm', '.co.bn', '.co.bo', '.co.br', '.co.bs', '.co.bt', '.co.bv', '.co.bw', '.co.by', '.co.bz', '.co.ca', '.co.cc', '.co.cf', '.co.cg', '.co.ch', '.co.ci', '.co.ck', '.co.cl', '.co.cm', '.co.cn', '.co.co', '.co.cr', '.co.cs', '.co.cu', '.co.cv', '.co.cx', '.co.cy', '.co.cz', '.co.de', '.co.dj', '.co.dk', '.co.dm', '.co.do', '.co.dz', '.co.ec', '.co.ee', '.co.eg', '.co.eh', '.co.er', '.co.es', '.co.et', '.co.eu', '.co.fi', '.co.fj', '.co.fk', '.co.fm', '.co.fo', '.co.fr', '.co.fx', '.co.ga', '.co.gb', '.co.gd', '.co.ge', '.co.gf', '.co.gg', '.co.gh', '.co.gi', '.co.gl', '.co.gm', '.co.gn', '.co.gp', '.co.gq', '.co.gr', '.co.gs', '.co.gt', '.co.gu', '.co.gw', '.co.gy', '.co.hk', '.co.hm', '.co.hn', '.co.hr', '.co.ht', '.co.hu', '.co.id', '.co.ie', '.co.il', '.co.in', '.co.io', '.co.iq', '.co.ir', '.co.is', '.co.it', '.co.je', '.co.jm', '.co.jo', '.co.jp', '.co.ke', '.co.kg', '.co.kh', '.co.ki', '.co.km', '.co.kn', '.co.kp', '.co.kr', '.co.kw', '.co.ky', '.co.kz', '.co.la', '.co.lb', '.co.lc', '.co.li', '.co.lk', '.co.lr', '.co.ls', '.co.lt', '.co.lu', '.co.lv', '.co.ly', '.co.ma', '.co.mc', '.co.md', '.co.me', '.co.mg', '.co.mh', '.co.mk', '.co.ml', '.co.mm', '.co.mn', '.co.mo', '.co.mp', '.co.mq', '.co.mr', '.co.ms', '.co.mt', '.co.mu', '.co.mv', '.co.mw', '.co.mx', '.co.my', '.co.mz', '.co.na', '.co.nc', '.co.ne', '.co.nf', '.co.ng', '.co.ni', '.co.nl', '.co.no', '.co.np', '.co.nr', '.co.nt', '.co.nu', '.co.nz', '.co.om', '.co.pa', '.co.pe', '.co.pf', '.co.pg', '.co.ph', '.co.pk', '.co.pl', '.co.pm', '.co.pn', '.co.pr', '.co.pt', '.co.pw', '.co.py', '.co.qa', '.co.qc', '.co.re', '.co.ro', '.co.ru', '.co.rw', '.co.sa', '.co.sb', '.co.sc', '.co.sd', '.co.se', '.co.sg', '.co.sh', '.co.si', '.co.sj', '.co.sk', '.co.sl', '.co.sm', '.co.sn', '.co.so', '.co.sr', '.co.st', '.co.su', '.co.sv', '.co.sx', '.co.sy', '.co.sz', '.co.tc', '.co.td', '.co.tf', '.co.tg', '.co.th', '.co.tj', '.co.tk', '.co.tl', '.co.tm', '.co.tn', '.co.to', '.co.tp', '.co.tr', '.co.tt', '.co.tv', '.co.tw', '.co.tz', '.co.ua', '.co.ug', '.co.uk', '.co.um', '.co.us', '.co.uy', '.co.uz', '.co.va', '.co.vc', '.co.ve', '.co.vg', '.co.vi', '.co.vn', '.co.vu', '.co.wf', '.co.ws', '.co.ye', '.co.yt', '.co.yu', '.co.za', '.co.zm', '.co.zr', '.co.zw', '.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.an', '.ao', '.aq', '.ar', '.as', '.at', '.au', '.aw', '.az', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', '.bm', '.bn', '.bo', '.br', '.bs', '.bt', '.bv', '.bw', '.by', '.bz', '.ca', '.cc', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cs', '.cu', '.cv', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm', '.do', '.dz', '.ec', '.ee', '.eg', '.eh', '.er', '.es', '.et', '.eu', '.fi', '.fj', '.fk', '.fm', '.fo', '.fr', '.fx', '.ga', '.gb', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.hu', '.id', '.ie', '.il', '.in', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.me', '.mg', '.mh', '.mk', '.ml', '.mm', '.mn', '.mo', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.mv', '.mw', '.mx', '.my', '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni', '.nl', '.no', '.np', '.nr', '.nt', '.nu', '.nz', '.om', '.pa', '.pe', '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.pt', '.pw', '.py', '.qa', '.qc', '.re', '.ro', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.st', '.su', '.sv', '.sx', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.tt', '.tv', '.tw', '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.wf', '.ws', '.ye', '.yt', '.yu', '.za', '.zm', '.zr', '.zw']

def page_rank(links, num_iterations=20, initial_pr=1.0):
    from collections import defaultdict
    import numpy as np

    page_rank = defaultdict(lambda: float(initial_pr))
    
    num_outgoing_links = defaultdict(float)
    incoming_link_sets = defaultdict(set)
    incoming_links = defaultdict(lambda: np.array([]))
    damping_factor = 0.85

    # collect the number of outbound links and the set of all incoming documents
    # for every document
    for (from_id,to_id) in links:
        num_outgoing_links[int(from_id)] += 1.0
        incoming_link_sets[to_id].add(int(from_id))
    
    # convert each set of incoming links into a numpy array
    for doc_id in incoming_link_sets:
        incoming_links[doc_id] = np.array([from_doc_id for from_doc_id in incoming_link_sets[doc_id]])
    
    num_documents = float(len(num_outgoing_links))
    if (num_documents == 0):
	num_documents = 1
    lead = (1.0 - damping_factor) / num_documents
    partial_PR = np.vectorize(lambda doc_id: page_rank[doc_id] / num_outgoing_links[doc_id])

    for _ in xrange(num_iterations):
        for doc_id in num_outgoing_links:
            tail = 0.0
            if len(incoming_links[doc_id]):
                tail = damping_factor * partial_PR(incoming_links[doc_id]).sum() 
		
            page_rank[doc_id] = lead + tail
            if page_rank[doc_id] >= 1:
               page_rank[doc_id] = 1 
    
    return page_rank

def hits(keyword):
    '''string->dictionary
    function that takes in a keyword, go through each URL in docdb, compute
    the number of hits and corresponding doc_id into a dictionary'''
    worddb = shelve.open('worddb')
    docdb = shelve.open('docdb')
    db = shelve.open('db')
	
    dic = {}
   
    try:  
        word_id =  worddb[keyword]
	i = 0
	
	while i < len(docdb):
	    hit = 0
	    a = []
	    try:
	        if db['doc_id:%s:isvalid' % i] == True:
                    
	    	    for x in db['doc_id:%s:words' % i]: #fill a with the first elements of tuples, which are the word_id's   
                        a.append(x[0])
                     
		    num_word = len(db['doc_id:%s:words' % i])
		    for j in a:
		        if word_id == a: #if keyword matches the word
			    hit += 1
                      
		    result = hit / num_word

		    if result==0:
		        point = 0
		    elif result > 0 and result < 0.02:
		        point = 0.2
		    elif result >= 0.02 and result < 0.04:
		        point = 0.6
		    elif result >= 0.04 and result < 0.06:
		        point = 1
		    elif result >= 0.06 and result < 0.08:
		        point = 0.6
		    elif result >= 0.08 and result < 0.10:
		        point = 0.2
		    else:
		        point = 0.01
	   
		    dic.update({i:point})

	    except Exception as e:
		pass
          
	    i+=1
	    
	worddb.close()
	docdb.close()
	db.close()
      
	return dic
        
    except Exception as e: 
	return dic

def relative_font_size(keyword):
    '''string->dictionary
    function that takes in a keyword, go through each URL in docdb, compute
    the font sizes of the keyword (for now, we can compute the average font size) and corresponding doc_id into a dictionary'''
    worddb = shelve.open('worddb')
    docdb = shelve.open('docdb')
    db = shelve.open('db')

    dic = {}
    
    try:
        word_id =  worddb[keyword]

        i = 0
        while i < len(docdb):
	    hit = 0
	    font_size_counter = 0
            try:
	        if db['doc_id:%s:isvalid' % i] == True:	
	            try:
	    	        for x in db['doc_id:%s:words' % i]:   
		            if x[0] == word_id:
			        font_size_counter = font_size_counter + x[1]
			        hit += 1	
		        if hit == 0:
	                    result = 0
		        else:
		            result = font_size_counter / hit

		        if result >= 5:
	                    point = 0.2
		        elif result >1:
		            point = 1
		        else:
		            point = 0
	 		
		        dic.update({i:point})
                    except Exception as e:
		        pass
	    except Exception as e:
		pass
            i += 1

        worddb.close()
        docdb.close()
        db.close()

        return dic

    except Exception as e: 
	return dic

def hits_in_title(keyword):
    '''string->dictionary
    function that takes in a keyword, go through each URL in docdb, compute
    the number of hits in the titles of URLs and corresponding doc_id into a dictionary'''
    worddb = shelve.open('worddb')
    docdb = shelve.open('docdb')
    db = shelve.open('db')

    dic = {}
    
    try:
        i = 0
        while i < len(docdb):
	    hit = 0
            a = []
            try:
	        if db['doc_id:%s:isvalid' % i] == True: 
                    try:
		        if keyword in db['doc_id:%s:title' % i].split():
		            hit += 1	
		        result = hit 

		        if result == 0:
		            point = 0
		        else:
		            point = 1

		        dic.update({i:point})

	            except Exception as e:
		        pass	   
	    except Exception as e:
 	        pass	
	    i += 1	
  
        worddb.close()
        docdb.close()
        db.close()	

        return dic

    except Exception as e:
	print "No Match Found In The Title" 
	return dic

def hits_in_outgoing_titles(keyword):
    '''string->dictionary
    function that takes in a keyword, go through each URL in docdb, compute
    the number of hits in the titles of incoming URLs and corresponding doc_id into a dictionary''' 
    worddb = shelve.open('worddb')
    docdb = shelve.open('docdb')
    db = shelve.open('db')

    dic = {}
   
    try:
        i = 0
        while i < len(docdb):
	    hit = 0
            a = []
            try:
	        if db['doc_id:%s:isvalid' % i] == True: 
                    try:
		        for x in db['doc_id:%s:links' % i]: #append all the doc_id's for outgoing links into a
                            a.append(x[1]) 

		        for j in a:
	                    if db['doc_id:%s:isvalid' % j] == True: #if outgoing link is valid    
	    	                if keyword in db['doc_id:%s:title' % j].split(): #if keyword is in the title of outgoing link             
			            hit += 1	
		        result = hit 

		        if result == 0:
		            point = 0
		        else:
		            point = 1

		        dic.update({i:point})

	            except Exception as e:
		        pass
            except Exception as e:
	        pass

	    i += 1	
        
        worddb.close()
        docdb.close()
        db.close()	
        
        return dic

    except Exception as e:
	print "No Match Found In The Outgoing Titles" 
     
	return dic

def hits_in_incoming_titles(keyword):
    '''string->dictionary
    function that takes in a keyword, go through each URL in docdb, compute
    the number of hits in the titles of incoming URLs and corresponding doc_id into a dictionary''' 
    worddb = shelve.open('worddb')
    docdb = shelve.open('docdb')
    db = shelve.open('db')

    dic = {}
   
    try:
        y = []
        i = 0
        while i < len(docdb):
	    hit = 0
            a = []
            try:
	        if db['doc_id:%s:isvalid' % i] == True: 
                    try:
		        for x in db['doc_id:%s:links' % i]: #append all the doc_id's for incoming links into a
			    a.append(x[0])

		        for j in a:
	                    if db['doc_id:%s:isvalid' % j] == True: #if incoming link is valid    
	    	                if keyword in db['doc_id:%s:title' % j].split(): #if keyword is in the title of incoming link             
			            hit += 1	
		        result = hit 

		        if result == 0:
		            point = 0
		        else:
		            point = 1

		        dic.update({i:point})

	            except Exception as e:
		        pass
            except Exception as e:
                pass
	    i += 1	
  
        worddb.close()
        docdb.close()
        db.close()	
       
        return dic

    except Exception as e:
	print "No Match Found In The Incoming Titles" 
	return dic

def description_tags(keyword):
    '''string->dictionary
    function that takes in a keyword, go through each URL in docdb, compute
    the number of hits in the description tags and corresponding doc_id into a dictionary'''
    worddb = shelve.open('worddb')
    docdb = shelve.open('docdb')
    db = shelve.open('db')

    dic = {}
    
    try:
        i = 0
        while i < len(docdb):
	    hit = 0
            try:
	        if db['doc_id:%s:isvalid' % i] == True: 
                    try:
			desc_words = db['doc_id:%s:desc' %i].split()
		        if keyword in desc_words:
		            hit += 1	
		        result = hit 

		        if result == 0:
		            point = 0
		        else:
		            point = 1

		        dic.update({i:point})

	            except Exception as e:
			# when there is no description tag and there is no text on the page
		        db['doc_id:%s:desc' % i] = 'No meta description or text on the page' 
			pass
            except Exception as e:
		pass	   
		
	    i += 1	
  
        worddb.close()
        docdb.close()
        db.close()	

        return dic

    except Exception as e:
	print "No Match Found In The Description Tags" 
	return dic

def hits_in_urls(keyword):
    '''string->dictionary
    function that takes in a keyword, go through each URL in docdb, compute
    the number of hits in the URLs and corresponding doc_id into a dictionary'''
    worddb = shelve.open('worddb')
    docdb = shelve.open('docdb')
    db = shelve.open('db')

    dic = {}
   
    try:
        new_db = docdb.items() 
        for x in new_db:
            hit = 0
            try: 
                if keyword in trim_url(x[0]): 
	            hit += 1

		    if hit == 0:
		        point = 0
		    else:
		        point = 1

		    dic.update({x[1]:point})
               	            
            except Exception as e:
                pass
	    	  
        worddb.close()
        docdb.close()
        db.close()	

        return dic

    except Exception as e:
	print "No Match Found In The URL" 
	return dic

def keywords(keyword):
    '''string->dictionary
    function that takes in a keyword, go through the keywords of the webpage, compute
    whether there is a hit and the corresponding doc_id into a dictionary'''
    worddb = shelve.open('worddb')
    docdb = shelve.open('docdb')
    db = shelve.open('db')

    dic = {}
    
    try:
        i = 0
        while i < len(docdb):
	    hit = 0
            try:
	        if db['doc_id:%s:isvalid' % i] == True: 
                    try:
		        if keyword in db['doc_id:%s:keywords' % i]:
		            hit += 1	
		        result = hit 

		        if result == 0:
		            point = 0
		        else:
		            point = 1

		        dic.update({i:point})

	            except Exception as e:
		        pass	   
            except Exception as e:
		pass	   
		
	    i += 1	
  
        worddb.close()
        docdb.close()
        db.close()	

        return dic

    except Exception as e:
	print "No Match Found In The Description Tags" 
	return dic

def trim_url(fullurl):
        '''string->string
        function that take in an URL and trim it and return'''
	# takes a full url and returns tier 1 url
	if fullurl.find('//')>0:
		newurl = fullurl[fullurl.find('//')+2:]
	else:
		newurl = fullurl
	if not newurl[-1] == '/':
		newurl = newurl + '/'
	newurl = newurl[:newurl.find('/')]
	
	if newurl[newurl.find('.'):] in extention_list:
		return newurl
	else:
		return trim_url(newurl[newurl.find('.')+1:])

def search(keyword):
    '''string->list
    function that takes in a keyword and returns the URLs, its title, and its description tags
    in the order of relevance calculated from different metrics and the page rank'''
    #Initialize the error signal to False
    error = False
    
    worddb = shelve.open('worddb')
    docdb = shelve.open('docdb')
    db = shelve.open('db')
      
    #This is used to detect if the keyword is an empty string
    keyword = keyword.strip()
    if len(keyword) == 0:
        error= True
     
    metric_1 = hits(keyword)
    metric_2 = relative_font_size(keyword)
    metric_3 = hits_in_title(keyword)
    metric_4 = hits_in_outgoing_titles(keyword)
    metric_5 = hits_in_incoming_titles(keyword)    
    metric_6 = hits_in_urls(keyword)
    metric_7 = description_tags(keyword)
    metric_8 = keywords(keyword)

    #set weights for each above metric
    weight_1 = 2
    weight_2 = 1
    weight_3 = 1.5
    weight_4 = 0.5
    weight_5 = 0.5
    weight_6 = 2.5
    weight_7 = 1.5
    weight_8 = 0.5
   
    #This is the weight for the page rank.
    #The low number means we will only differentiate the URLs by the page rank
    #when their scores from other metrics are the same.
    weight_9 = 0.0000001
 
    dic = {}
    dick = {}
    score = []

    #Initialize the scores for each document to zero
    j = 0
    while j < len(docdb):
        score.append(0)
        j += 1

    #Compute the page rank of all documents
    k = 0
    a = []
    while k < len(docdb):   
        try:          
	    if db['doc_id:%s:isvalid' % k] == True: 
	        try:	
		    for x in db['doc_id:%s:links' % k]:
		        a.append(x)
	        except Exception as e:
		    pass  
        except Exception as e:
	    pass
  
	k += 1

    PageRank = page_rank(a,3,1)		
 
    #Compute the scores for each document using metrics and the page rank
    i = 0
    while i < len(docdb):
        try: score[i] += metric_1[i]*weight_1
        except Exception as e:
            pass
        try: score[i] += metric_2[i]*weight_2
        except Exception as e: 
            pass
        try: score[i] += metric_3[i]*weight_3
        except Exception as e: 
            pass
        try: score[i] += metric_4[i]*weight_4
        except Exception as e: 
            pass
        try: score[i] += metric_5[i]*weight_5
        except Exception as e: 
            pass
        try: score[i] += metric_6[i]*weight_6
        except Exception as e: 
            pass
        try: score[i] += metric_7[i]*weight_7
        except Exception as e: 
            pass
        try: score[i] += metric_8[i]*weight_8
        except Exception as e: 
            pass
        dick.update({i:score[i]}) #Needed later to detect keywords that are not like to give outputs
        try: score[i] += PageRank[i]*weight_9
        except Exception as e: 
            pass 
        dic.update({i:score[i]}) 
        i += 1
    
    #This is used to catch the keywords that are not likely to give outputs
    q = 0
    p = 0
  
    while p < len(dick):
        if dick[p] != 0:
            q = 1
        p +=1
    
    if q == 0:
        error = True
 
    dic = dic.items()
    
    #Sort the dictionary {doc_id: score} according to score
    dic_sorted = sorted(dic, key=operator.itemgetter(1), reverse=True)
        
    doc = docdb.items()

    #This is used for comparison purpose onlly
    doc_sorted = sorted(doc, key=operator.itemgetter(1), reverse=True)     

    main_url_cache =[]
    result = [] 
    for x in dic_sorted:
         for y in doc: 
             if x[0] == y[1]:
                 try: 

		     temp_url = trim_url(y[0])               
		     if temp_url in main_url_cache:
		     	 pass
		     else:
			 revised_desc = ''
			 if len(db['doc_id:%s:desc' % y[1]]) > 144:
				revised_desc = db['doc_id:%s:desc' % y[1]][:144] + ' .....'
			 else:
				revised_desc = db['doc_id:%s:desc' % y[1]]
	                 result.append( (y[0], db['doc_id:%s:title' % y[1]], revised_desc, x[1]) )
		         main_url_cache.append(temp_url)
                 except Exception as e: 
                    pass   
    
    #Actual Code, used only when using frontend as well! NOT TO BE USED FOR UNIT TESTING
    f = open('./results.txt','w')
    f2=open("./numbers.txt","w")
    f.write('<body bgcolor="#fdf5e6">\n')
    count=0
    if (error):
	f.write('<p style="font-family:FreeSans;font-size:120%;color:black">\n')
	f.write('Sorry, your search '+keyword+' did not match any document.\n')
	f.write('Suggestions\n1.Make sure the query is not empty\n2. Make sure all words are spelt correctly.\n3. Try different keywords\n4. Try more general keywords\n')
	count=0
    else:
        for i in range(len(result)):
	    link=result[i][0]
	    title=result[i][1]
	    description=result[i][2]
	    if result[i][3] > 0.0000001:
		    if link[0]=='u':
		        link=link[1:]
		    if title[0]=='u':
		        title=title[1:]
		    if description[0]=='u':
		        description=description[1:]	
		    if link[0]!='m':
		        count=count+1	    
		        f.write (str(count)+'. title=<a href="'+link+'">'+title+'</a>\n')	    
		        f.write ('    url='+link+'\n')
		        f.write ("description="+description+"\n")
		        f.write ("\n")
			if (count%10==0):
			    f.write ("\n\n")
    f.write("</body>\n")
    f.close()
    f2.write('<p style="font-family:FreeSans;font-size:120%;color:black">\n'+str(count))#stores the total number of results found in another text file.
    f2.close()
    count=0

    worddb.close()
    docdb.close()
    db.close()
    
    #This is used for unittest purpose only
    if error:
	result = [-1]
 
    return result
