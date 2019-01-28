# tagpage.py
# this generates the inner content when requested for a specific tag

import os
import linecache # for reading /tmp/list.txt
import taghandler

def getImgFromIndex(index):
    print('get path to image given img number ' + index)
    theline = linecache.getline('/tmp/list.txt',int(index)).strip()
    print(theline)
    return theline

def tagImageFromURI(uri):
    # process uri for args for tagimage
    print("tagImageFromURI with " + uri)
    print(uri.split(':'))
    imgnum = uri.split(':')[3].split('?')[0]
    tag = uri.split('tag=')[1] 
    if tag == "":
        print('tag empty')
        return
    print('adding tag ' + tag + " to image " + imgnum)
    taghandler.addtag(getImgFromIndex(imgnum),tag)

def maketagpage(uri):
    print("maketagpage with" + uri)
    return """<br>
            maketagpage called with <br>
            uri {u}<br>
            i see {getcwd}<br>
            """.format(u=uri,getcwd=os.getcwd())

