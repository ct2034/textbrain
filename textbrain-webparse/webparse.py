import bs4
import urllib2
import nltk

def from_url(url, parser):
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

def from_url_lxml(url):
    return from_url(url, "lxml")

def from_url_html5lib(url):
    return from_url(url, "html5lib")

if __name__ == "__main__":
    print ">>>>"
    print from_url_lxml("http://www.khs.com/produkte.html")
    print "<<<<"