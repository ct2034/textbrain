import os 
import bs4
import urllib2
import nltk
import thread
import flask
import time
app = flask.Flask(__name__)

class webparse:
    def __init__(self, pw):
        # variables
        self.pw = pw
        self.queue = []
        
    def start_server(self):
        port = os.getenv("PORT", 8080)
        ip = os.getenv("IP", '0.0.0.0')
        
        thread.start_new_thread( app.run, (ip, port) )
        print "started"
        #t1.join()
        
        
    def from_url(self, url, parser):
        # Source: http://stackoverflow.com/a/24618186
        
        html = urllib2.urlopen(url).read()
        soup = bs4.BeautifulSoup(html, parser)
        
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

pw = raw_input("Choose a passphrase ...")
wp = webparse(pw)

@app.route('/')
def hello_world():
    global wp
    return wp.from_url("http://www.zeit.de/politik/ausland/2015-12/parlamentswahlen-spanien-podemos-mariano-rajoy", "lxml")
    
if __name__ == "__main__":
    global wp
    # wp = webparse(pw)
    wp.start_server()
    # for parser: http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
    # print wp.from_url("http://www.google.com", "lxml")
    
    while (True):
        time.sleep(1)