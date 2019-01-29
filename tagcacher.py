# tagcacher.py
# this immediately forks and starts cacheing tags
# this will take some time

# gunicorn has a thread timeout 
# so we make a new thread that can take as long as it wants
from multiprocessing import Process 

# other files
import taghandler
import builder

import os
import shutil

#os.chdir('..')

def buildTagCache():
    print('cachetages here at ' + os.getcwd() )
    tagcachefile = '/tmp/tagcache'

    tagcachedir = '/tmp/tagcachedir/'

    if os.path.isdir(tagcachedir):
        shutil.rmtree(tagcachedir)
    os.mkdir(tagcachedir)

    count=0
    filelist = open('/tmp/list.txt','r')
    cachefile = open('/tmp/tagcache.txt','w')
    print('cachetag building ' )
    for line in filelist:
    # /tmp/flatfile tag list cache the page is built from
        line = line.strip()
        tags = taghandler.exifGetComment(line)
        print(line + ',' +  tags)
        cachefile.write(line + ',' +  tags+'\n')
    # this will make it easy to generate the page of specific tags
    # /tmp/tagdir/tag
    #   filename
    #   filename
    #   filename
        for tag in tags.split(','):
            print('tagcachedir writing '+tag)
            with open(tagcachedir+tag , 'a') as tagtoken:
                tagtoken.write(line + '\n')

    filelist.close()
    cachefile.close()
    builder.buildPageFromCache()

print('forking tagcacher!')
p = Process(target=buildTagCache)
p.start()

