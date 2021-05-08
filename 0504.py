from bs4 import BeautifulSoup
import requests
from collections import deque
import json
from urllib.parse import *

prof = 'shivaram'
https = True
max_degree = 0
max_get_size = 262144 # if item is larger than 256KB, we do not get it
avoid_ext = '.mov .mp3 .mp4 .mpg .doc .xls .ppt .docx .xlsx .pptx .pdf .ps .tgz .zip .jpg'.split(' ')

class WebsiteContent:
    def __init__(self, deg):
        self.page = dict()
        self.degree = deg

# Let WebsiteContent serializable
class MyEncoder(json.JSONEncoder): # https://stackoverflow.com/questions/23088565/
    def default(self, o): # https://stackoverflow.com/questions/3768895/
        if (isinstance(o, WebsiteContent)):
            return o.__dict__
        return super().default(o)
    pass

def parse_link(site, link):
    if (not urlparse(link).scheme):
        a = urljoin(site, link)
    else:
        a = link
    return a

def get_links(url):
    """
    pass in an url without protocol (http/https). 
    retrieve the page and get all the links in that page. 
    delete links that are not in http/https and remove protocols from the remaining links. 
    return links list
    """
    # first, don't want anything not html
    if ([ext for ext in avoid_ext if(ext in url)]): # https://www.geeksforgeeks.org/python-test-if-string-contains-element-from-list/
        return list()
    while (True) :
        header = requests.head(url=url, timeout=0.5)
        if (header.status_code != 301):
            break
        url = header.headers['Location']
    if ('html' not in header.headers['Content-Type']):
        return list()
    if ('Content-Length' in header.headers.keys() and int(header.headers['Content-Length']) > max_get_size):
        return list()
    
    res = requests.get(url=url, timeout=0.5)
    ret = list()
    for link in BeautifulSoup(res.content, 'lxml').find_all('a'):
        href = link.get('href')
        if (not href or 'mailto' in href):
            continue
        
        # parse the link
        a = parse_link(url, href)
        
        # now it is a valid link. clean up the link
        # # remove end slash
        # if(href.endswith('/')):
        #     href = href[:-1]
        ret.append(a)
    return ret

def main():
    global max_degree
    root = 'http' + ('s' if https else '') + '://pages.cs.wisc.edu/~' + prof + '/'
    site = dict()
    todo = deque()
    site['pages.cs.wisc.edu'] = WebsiteContent(0)
    site['www.cs.wisc.edu'] = WebsiteContent(0)
    todo.append(root)
    
    break_now = False # We can change it to true during debugging so that we will stop at certain point
    while (bool(todo) and (break_now is False) ):
        page = todo.pop()
        sitename = None # netloc
        pagename = None # path
        degree = -1
        
        # get the sitename and pagename
        ps = urlparse(page)
        sitename = ps.netloc
        pagename = ps.path if (len(ps.path)) else '/'
        del ps
        
        # get the degree
        try:
            degree = site[sitename].degree
        except KeyError:
            print('Error getting the degree of \'' + sitename + '\'! Abort.')
            exit(1)
        
        # get links in this page
        try:
            links = get_links(page)
        except requests.exceptions.Timeout:
            # timeout, so empty "links"
            links = list()
        except Exception as e:
            print(str(e) + '; \t' +  str(e.__cause__) + '. Making empty list')
            links = list()

        # make the page's link list
        site[sitename].page[pagename] = links

        # store links and add them to "todo" if we haven't visited them
        for link in links: # link has no protocol (http[s]) and will not end with '/'
            # put them into page's link list in "site"
            # site[sitename].page[pagename].append(link)
            
            # NOTE: This time only get webpages in ~remzi
            if (prof not in link):
                continue

            # do not want files that are not webpages
            if ([ext for ext in avoid_ext if(ext in link)]): 
                continue
            
            # see if we've visited this site. If not, add a new entry in "site" and setup the degree if it fits our "max_degree" rule
            link_sitename = None
            link_pagename = None
            ps = urlparse(link)
            link_sitename = ps.netloc
            link_pagename = ps.path if (len(ps.path)) else '/'
            del ps

            if (link_sitename in site):
                # check if we have not visited the site. Add link to queue only if we haven't.
                if(link_pagename not in site[link_sitename].page ):
                    todo.append(link)
            else:
                # never visited this site. create WebsiteContent only if the degree fits. else just ignore this link
                if (degree >= 0 and degree < max_degree):
                    site[link_sitename] = WebsiteContent(degree + 1)
                    todo.append(link)
    
    # finally, save all the hard work we've (the computers have) done
    outfile = open(file=root.replace(':', '_').replace('/', '_').replace('~', '_') + '.json', mode='w')
    outfile.write(json.dumps(site, cls=MyEncoder))
    

if (__name__ == '__main__'):
    main()
