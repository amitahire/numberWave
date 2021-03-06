#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import os,sys
import getopt
import webbrowser
from utils import Utils
from update.all_subject import print_all_subject

engin = ""
keyword = ""
use_subject = u""
search_keyword = False
search_video = False

def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-c, --course: the course for search on the web'
    print '-q, --query: the query keyword for search on the web'
    print '-e, --engin: what search for search include: google baidu bing yahoo'
    print '-u, --use: seach in what subject'
    print '-v, --video: search video'
    print "\nsubject include:"
    print_all_subject()
    print '\nex: ' + argv0 + ' -c "cs199" -u eecs'
    print '\nthe suported engin:\n' + get_all_engins()

def get_all_engins():
    utils = Utils()
    return '  '.join(utils.search_engin_dict.keys())

def openBrowser(url):
    if url == "":
        print "not found url"
    else:
        print "open " + url
        webbrowser.open(url)

def search(keyword, engin, search_keyword = False):
    url = ''
    if search_keyword == False:
        utils = Utils()
        record = utils.getRecord(keyword, use_subject)
        url = record.get_url().strip()
        keyword = record.get_title().strip()

    if search_video:
        engin_list = ['youtube', 'coursera', 'edx', 'googlevideo', 'chaoxing', 'youku', 'tudou', 'videolectures']
        for e in engin_list:
            openWeb(e, keyword, url)
    else:
        openWeb(engin, keyword, url)

def openWeb(engin, keyword, url):
    if engin.lower() == 'edx':
        keyword = keyword.replace(' ', '+')
    utils = Utils()
    if engin != '':
        url = utils.getEnginUrl(engin) + keyword
    if engin == "arxiv":
        url = url.replace("$", keyword)
    if engin == "doaj":
        url = url.replace('$', keyword)

    if url != '':
        openBrowser(url)

def main(argv):
    global keyword, engin, use_subject, search_keyword, search_video
    try:
        opts, args = getopt.getopt(argv[1:], 'hc:e:u:q:v', ["help","course","engin","use", 'query', 'video'])
        if len(args) == 1:
            keyword = args[0]
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
        elif o in ('-c', '--course'):
            keyword = a
        elif o in ('-q', '--query'):
            keyword = a
            search_keyword = True
        elif o in ('-e', '--engin'):
            engin = a
        elif o in ('-u', '--use'):
            use_subject = str(a)
        elif o in ('-v', '--video'):
            search_video = True
           
    if keyword != "":
        search(keyword, engin, search_keyword) 
             

if __name__ == '__main__':
    main(sys.argv)
