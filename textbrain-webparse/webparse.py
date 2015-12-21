import os 
import bs4
import urllib2
import nltk
import thread
import flask
import time
import json
app = flask.Flask(__name__)

class webparse:
    def __init__(self):
        pw = raw_input("Choose a passphrase ...")
        # variables
        self.pw = pw
        self.queue = []
        
    def start_server(self):
        port = os.getenv("PORT", 8080)
        ip = os.getenv("IP", '0.0.0.0')
        
        thread.start_new_thread( app.run, (ip, port) )
        print "started"
        #t1.join()
        
    def add_url(self, url):
        if url not in self.queue:
            self.queue.append(url)
            
    def check_pw(self, pw_):
        return (pw_ == self.pw)
        
    def work(self):
        if self.queue.__len__() == 0:
            print "Queue empty"
        else:
            start = time.time()
            url = self.queue.pop(0)
            text = self.from_url(url, "lxml")
            end = time.time()
            print "Parsing of " + url + " took " + str(end - start)
        
    def from_url(self, url, parser):
        # Source: http://stackoverflow.com/a/24618186
        
        try:
            html = urllib2.urlopen(url).read()
        except Exception, e:
            print "ERROR: " + str(e)
            print "failed to open: >" + url + "<"
            return ""
            
        try:
            soup = bs4.BeautifulSoup(html, parser)
        except Exception, e:
            print "ERROR: " + str(e)
         
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        
        # get text
        text = soup.get_text(" ")
        
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text

wp = webparse()

@app.route('/api/<pw>', methods=['POST'])
def api(pw):
    print "api call with >" + pw + "<"
    if not wp.check_pw(pw):
        print "wrong pw"
        return ("wrong pw", 401)
    else:
        print "pw ok"
        try:
            urls = json.loads(flask.request.data)
            for url in urls:
                wp.add_url(url)
        except Exception, e:
            return("Exception: " + e, 404) 
        return ("ok", 200)
    
if __name__ == "__main__":
    global wp
    # wp = webparse(pw)
    wp.start_server()
    # for parser: http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
    # print wp.from_url("http://www.google.com", "lxml")
    
    while (True):
        time.sleep(2)
        wp.work()