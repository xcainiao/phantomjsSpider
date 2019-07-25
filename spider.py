import os
import re
import sys
import json
import socket
import random
import urllib2
import optparse
# import urltools
import subprocess
from tld import get_tld, exceptions
from threading import Timer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
jspath = os.path.join(BASE_DIR, "js/post.txt")

"""
getpath  = os.path.join(BASE_DIR, "temp/get_result.txt")
postpath = os.path.join(BASE_DIR, "temp/post_result.txt")
subpath = os.path.join(BASE_DIR, "temp/sub_result.txt")
sub1path = os.path.join(BASE_DIR, "temp/sub2_result.txt")
"""

headers = {"cookie": "PHPSESSID=hgrpge7m21gvb8f9k108hlg1kp; _ga=GA1.2.1987976722.1531469534; _gid=GA1.2.1965506052.1531705837; _gat=1", "accept": "*/*","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.9","content-length": "103","content-type": "application/x-www-form-urlencoded; charset=UTF-8","origin": "https://tools.keycdn.com","referer": "https://tools.keycdn.com/ping", "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.62 Chrome/67.0.3396.62 Safari/537.36", "x-requested-with": "XMLHttpRequest"}

headers2 = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.9","cookie": "PHPSESSID=hgrpge7m21gvb8f9k108hlg1kp; _ga=GA1.2.1987976722.1531469534; _gid=GA1.2.1965506052.1531705837; _gat=1","upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.62 Chrome/67.0.3396.62 Safari/537.36"}

def loginfo(type_l, url):
    if 1:
        if type_l==1:
            print "get new data---------------------------" + url
        elif type_l==2:
            print "post new data--------------------------" + url
        elif type_l==3:
            print "domain new data------------------------" + url
        else:
            print "new sub domain new data------------------------" + url

def runPhantomjs(url):
    process = subprocess.Popen(['phantomjs', 
        'js/script2.js',
        url], stdout=subprocess.PIPE)
    timer = Timer(20, process.kill)
    try:
        timer.start()
        out, err = process.communicate()
    finally:
        timer.cancel()
    return out

def filterurl(url):
    if url[-1] == '?' or url[-1] == '#':
        url = url[:-1]
    url = url.split('#')[0]
    urllist = url.split('?')
    if len(urllist) > 1:
        print url
        print "xxxxxxxxxxxxxxxxxxxxxxxxxx"
        print urllist[1] 
        parameter = ""
        #parameter = urltools.normalize_query(urllist[1])
        parameter = re.sub("&t=\d+(\.)*\d+", '&t=', parameter)
        parameter = re.sub("lang=[^&]*", 'lang=', parameter)
        url = urllist[0] + '?' + parameter  
    return url

def parsehost(url):
    tmp = urllib2.urlparse.urlparse(url).hostname
    if tmp:
        return tmp
    else:
        print "invild url"
        sys.exit(-1)

def countpath(url, number):
    path = urllib2.urlparse.urlparse(url).path
    path = path.rpartition('/')[0]
    if path not in pathdict.keys():
        pathdict[path] = 1
    elif pathdict[path]>number+1:
        return pathdict[path]
    else:
        pathdict[path] = pathdict[path] + 1
    return pathdict[path]

def iplookup(domain):
    try:
        value = socket.gethostbyname(domain)
    except:
        return
    return value


def saveget(urllist, domain, topdomain, number, fdomain, specialip):
    
    getpath, postpath, subpath, sub1path = filename(domain)
    tmpget = []
    subdomaininfo = {}
    for url in urllist:
        if (not url) or (not url.startswith('http')):
            continue
        try:
            maindomain = get_tld(url)
            subdomain = parsehost(url)
            if fdomain == '1':
                tmpdomain = maindomain
            else:
                tmpdomain = subdomain
        except:
            continue

        if domain == tmpdomain:
            if not number or countpath(url, number)<=number:
		# url = filterurl(url)
		fresult = open(getpath, 'a+')
		tmpurls = fresult.read()
		if url not in tmpurls:
		    tmpget.append(url)
		    loginfo(1, url)
		    reslist.append(url)
		    fresult.write(url + '\n')
		fresult.close()
        else:
            fsubdomain = open(subpath, 'a+')
            domains = fsubdomain.read()
            if tmpdomain not in domains:
                loginfo(3, tmpdomain)
                fsubdomain.write(tmpdomain + '\n')
            fsubdomain.close()

def savepost(domain, topdomain, fdomain, specialip):

    getpath, postpath, subpath, sub1path = filename(domain)
    tmppost = []
    subdomaininfo = {}
    ftmp = open(jspath, 'r')
    for line in ftmp.readlines():
        line = line.strip('\n')
        postdic = json.loads(line)
        poststr = str(postdic['url'])
        try:
            maindomain = get_tld(poststr)
            subdomain = parsehost(poststr)
            if fdomain == '1':
                tmpdomain = maindomain
            else:
                tmpdomain = subdomain
        except Exception,e:
            print e
            continue
        
        '''
        del postdic['headers']
        poststr = json.dumps(postdic).replace(' ','').replace('{','').replace('}','')
        '''
        if domain == tmpdomain:
            fresult = open(postpath, 'a+')
            tmpres = fresult.read()
            if poststr not in tmpres:
                tmppost.append(line)
                loginfo(2, line)
                fresult.write(line + '\n')
        else:
            fsubdomain = open(subpath, 'a+')
            domains = fsubdomain.read()
            if tmpdomain not in domains:
                loginfo(3, tmpdomain)
                fsubdomain.write(tmpdomain + '\n')
            fsubdomain.close()

def spider(starturl, domain, topdomain, number, fdomain, specialip):
    urlstring = runPhantomjs(starturl)
    urllist = urlstring.split('\n')
    saveget(urllist, domain, topdomain, number, fdomain, specialip)
    savepost(domain, topdomain, fdomain, specialip)

def clearfile(domain, topdomain):
    if(not os.path.exists(jspath)):
        print "./js/post.txt file not exit"
        sys.exit (1)

    getpath, postpath, subpath, sub1path = filename(domain)

    open(getpath, 'w').close()
    open(postpath, 'w').close()
    open(subpath, 'w').close()
    open(sub1path, 'w').close()

def filename(topdomain):

    getname = "temp/" + topdomain + "_get.txt" 
    postname = "temp/" + topdomain + "_post.txt" 
    subname = "temp/" + topdomain + "_sub.txt" 
    sub1name = "temp/" + topdomain + "_sub1.txt" 
    getpath  = os.path.join(BASE_DIR, getname)
    postpath = os.path.join(BASE_DIR, postname)
    subpath = os.path.join(BASE_DIR, subname)
    sub1path = os.path.join(BASE_DIR, sub1name)

    return getpath, postpath, subpath, sub1path

def arguments():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url',
                    action="store", dest="url",
                    help="dest url", default='')
    parser.add_option('-n', '--number',
                    action="store", dest="number",
                    help="path url number default 0", default='0')
    parser.add_option('-d', '--domain',
                    action="store", dest="domain",
                    help="all subdomain(1/0)", default="0")
    parser.add_option('-s', '--special',
                    action="store", dest="special",
                    help="use super ip get domain", default="0")
    options, args = parser.parse_args()
    if not options.url:
        print 'python spider.py -h'
        sys.exit(-1)
    return options.url, int(options.number), options.domain, int(options.special)

reslist = []
pathdict = {}
def main():
    starturl, number, fdomain, specialip = arguments()
    try:
        topdomain = get_tld(starturl)
        subdomain = parsehost(starturl)
        if fdomain=="1":
            domain = topdomain
        elif fdomain=="0":
            domain = subdomain
        else:
            print "invalid domain"
            sys.exit(1)
        if not domain:
            print "invalid url"
            sys.exit(1)
        clearfile(domain, topdomain)
        reslist.append(starturl)
    except:
        print "invalid url"
        sys.exit(1)
    try:
        while len(reslist):
            spider(reslist.pop(random.randint(0, len(reslist)-1)), domain, topdomain, number, fdomain, specialip)
    except KeyboardInterrupt, e:
        print "********************************"
        print "********************************"
        print "program over"
        print "********************************"
        print "********************************"
        sys.exit(1)
main()
