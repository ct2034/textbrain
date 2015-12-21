from timeout import timeout
import os
import bs4
import urllib2
# import nltk
import thread
import flask
import time
import json
import yaml
app = flask.Flask(__name__)


class webparse:
    def __init__(self):
        self.queue = []
        self.settings = self.load_config("settings.yaml")

    def load_config(self, filen):
        stream = open(filen, 'r')
        docs = yaml.load_all(stream)
        return docs.next()

    def start_server(self):
        port = os.getenv("PORT", 8080)
        ip = os.getenv("IP", '0.0.0.0')

        thread.start_new_thread(app.run, (ip, port))
        print "REST API started"

    def add_url(self, url):
        if url not in self.queue:
            self.queue.append(url)

    def check_pw(self, pw_):
        return (pw_ == self.settings['passphrase'])

    def work_on_queue(self):
        if self.queue.__len__() != 0:
            start = time.time()
            url = self.queue.pop(0)
            text = self.from_url(url, "lxml")
            end = time.time()
            print "Parsing of " + url + " took " + str(end - start) + "s"
            print " Text length: " + str(text.__len__())

    @timeout(5)
    def from_url(self, url, parser):
        # Source: http://stackoverflow.com/a/24618186
        # on parsers:
        # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
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
            return ""
        # remove all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        # get text
        text = soup.get_text(" ")
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (
            phrase.strip() for
            line in
            lines for
            phrase in
            line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text


@app.route('/api/queue_urls', methods=['POST'])
def api_queue_urls():
    try:
        rq_json = json.loads(flask.request.data)
    except Exception, e:
        return("error parsing json\nException: " + str(e), 404)
    pw = rq_json["pw"]
    print "api call with >" + pw + "<"
    if not wp.check_pw(pw):
        print "wrong pw"
        return ("wrong pw", 401)
    else:
        print "pw ok"
        urls = rq_json["urls"]
        for url in urls:
            wp.add_url(url)
        return ("ok", 200)


@app.route('/test', methods=['POST'])
def test():
    print str(flask.request.data)
    return ("ok", 200)

if __name__ == "__main__":
    wp = webparse()
    wp.start_server()
    # print wp.from_url("http://www.google.com", "lxml")

    while (True):
        time.sleep(.1)
        wp.work_on_queue()
