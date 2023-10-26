import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import sys
from urllib.robotparser import RobotFileParser

rTxt = RobotFileParser()
global currentRobotBaseUrl
currentRobotBaseUrl = ""
TOKENLIST = [] #global token list
WORDFREQ = {} #global words frequencies
NUM_WORDS = 0 #total number of words
UNIQUE_URLS = 0 #number of unique URLs


def scraper(url, resp):
    links = extract_next_links(url, resp)
    # getting stop words
    stops = set(stopwords.words('english'))
    soup = BeautifulSoup(resp.raw_response.content, "lxml")
    # line 30 is needed for tokenizer from nltk, just run it once the
    nltk.download('punkt')
    # Tokenizing the website
    dummy_text = soup.get_text()

    # tokenizing the website, filtering stop words and non alphanumerics
    text_tokens = nltk.tokenize.word_tokenize(dummy_text.lower())
    filtered_words = [word for word in text_tokens if word not in stops]
    cleaned_list = [word for word in filtered_words if word.isalnum()]

    #recording the number of word frequencies
    for word in cleaned_list:
        if word in WORDFREQ:
            WORDFREQ[word] += 1
        else:
            WORDFREQ[word] = 1
    # to check the frequencies of words
    #print(WORDFREQ)

    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.

    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    next_links = []
    if(resp.status == 200):

        soup = BeautifulSoup(resp.raw_response.content, "lxml")
        links = soup.find_all('a')
        #Getting out links
        for link in links:
            dummy_link = link.get('href')
            #checking for fragments of pages
            if "#" in dummy_link:
                print("# found")

            #this function slowing us down bruh
            next_links.append(dummy_link)

    else:
        print(resp.error)
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!

    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    return next_links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    try:
        parsed = urlparse(url)
        #need to check for valid domains
        valid_domains = [".ics.uci.edu", "cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu"]
        if parsed.scheme not in set(["http", "https"]):
            return False
        # making sure that the url has a network location or a hostname before continuing
        if parsed.netloc == None or parsed.hostname == None:
            return False

        # #Ensure url is within specific domains
        inDomain = False
        for domain in valid_domains:
            if domain in parsed.hostname:
                inDomain = True
        if not inDomain:
            #If not in domain, return false
            return False
        # Check Robots.txt for politeness
        # Got it from here: https://docs.python.org/3/library/urllib.robotparser.html
        global currentRobotBaseUrl
        if parsed.netloc != currentRobotBaseUrl:
            rTxt.set_url(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
            rTxt.read()
        currentRobotBaseUrl = parsed.netloc
        if not (rTxt.can_fetch("*", url)):
            print("Robots.txt, url disallowed")
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
    
