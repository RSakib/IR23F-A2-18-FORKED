import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys
from urllib.request import urlopen



def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.

    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.

    if(resp.status == 200):

        soup = BeautifulSoup(resp.raw_response.content, "html.parser")
        links = soup.find_all('a')
        dummycounter = 0
        counter = 50
        next_links = []
        for link in links:
            dummy_link = link.get('href')
            dummycounter += 1

            #checking for fragments of pages
            if "#" in dummy_link:
                print("# found")

            #print(dummy_link)
            next_links.append(dummy_link)
            if dummycounter == counter:
                break




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
        print(parsed.scheme + "://" + parsed.netloc + "/robots.txt")


        if parsed.scheme not in set(["http", "https"]):
            return False
        # making sure that the url has a network location or a hostname before continuing
        if parsed.netloc == None or parsed.hostname == None:
            return False
        # making sure that the hostname is within the domains we are limited to
        # Doesnt really work yet - Kevin
        # for domain in valid_domains:
        #     if domain not in parsed.hostname:
        #         return False

        check_robot(parsed.scheme + "://" + parsed.netloc + "/robots.txt")

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

def check_robot(robotTxtURL):
    # I used this to see how to open and read contents from a URL
    # https://stackoverflow.com/questions/15138614/how-can-i-read-the-contents-of-an-url-with-python
    robotTxt = urlopen(robotTxtURL)
    f = urlopen(robotTxtURL)
    myfile = f.readline()
    while len(myfile) != 0:
        print(myfile)
        myfile = f.readline()
    
    

if __name__ == "__main__":
    print()
    is_valid(sys.argv[1])