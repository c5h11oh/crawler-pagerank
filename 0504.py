from bs4 import BeautifulSoup
import requests
from collections import deque
import json

max_degree = 0
avoid_ext = '.mov .mp3 .mp4 .mpg .doc .xls .ppt .docx .xlsx .pptx .pdf .ps'.split(' ')

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

def get_links(url):
    """
    pass in an url without protocol (http/https). 
    retrieve the page and get all the links in that page. 
    delete links that are not in http/https and remove protocols from the remaining links. 
    return links list
    """
    # first, don't want anything not html
    if ([ele for ele in avoid_ext if(ele in url)]): # https://www.geeksforgeeks.org/python-test-if-string-contains-element-from-list/
        return list()
    header = requests.head(url='http://'+url, timeout=0.5)
    if ('html' not in header.headers['Content-Type']):
        return list()
    
    res = requests.get(url='http://'+url, timeout=0.5)
    ret = list()
    for link in BeautifulSoup(res.content, 'lxml').find_all('a'):
        href = link.get('href')
        if (not href or 'mailto' in href):
            continue
        if ( (not href.startswith('http://')) and (not href.startswith('http://')) and (not href.startswith('./')) ):
            # may be a relative link. give it a try instead of 'continue'?
            href = './' + href
            # continue
        
        # now it is a valid link. clean up the link
        # remove end slash
        if(href.endswith('/')):
            href = href[:-1]
        # turn relative path to absolute path
        if (href.startswith('.')):
            ret.append(url + href[1:])
        # otherwise remove the protocol
        else:
            ret.append(href.split('://')[1])
    return ret

def main():
    global max_degree
    root = 'pages.cs.wisc.edu/~remzi'
    site = dict()
    todo = deque()
    site['pages.cs.wisc.edu'] = WebsiteContent(0)
    todo.append(root)
    
    while (bool(todo)):
        page = todo.pop()
        sitename = None
        pagename = None
        degree = -1
        
        # get the sitename and pagename
        i = page.find('/')
        if (i != -1): # needs to split to get the sitename
            sitename = page[:i]
            pagename = page[i:]
        else:
            sitename = page
            pagename = '/'
        del i
        
        # get the degree
        try:
            degree = site[sitename].degree
        except KeyError:
            print('Error getting the degree of \'' + sitename + '\'! Abort.')
            exit(1)
        
        # make the page's link list
        site[sitename].page[pagename] = list()

        # get links in this page
        try:
            links = get_links(page)
        except requests.exceptions.Timeout as timeout:
            # timeout, so empty "links"
            links = list()
        
        # store links and add them to "todo" if we haven't visited them
        for link in links: # link has no protocol (http[s]) and will not end with '/'
            # put them into page's link list in "site"
            site[sitename].page[pagename].append(link)
            
            # see if we've visited this site. If not, add a new entry in "site" and setup the degree if it fits our "max_degree" rule
            link_sitename = None
            link_pagename = None
            i = str(link).find('/')
            if (i != -1):
                link_sitename = link[:i]
                link_pagename = link[i:]
            else:
                link_sitename = link
                link_pagename = '/'
            
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
    outfile = open(file='out.txt', mode='w')
    outfile.write(json.dumps(site, cls=MyEncoder))
    

if (__name__ == '__main__'):
    main()
