# tagcacher.py
# this immediately forks and starts cacheing tags
# this will take some time

from multiprocessing import Process
import taghandler
import builder
import os
import time

#os.chdir('..')

def cachetags():
    print('cachetages here at ' + os.getcwd() )
    tagcachefile = '/tmp/tagcache'

    count=0
    #filelist = open('/tmp/list.txt','r')
    #cachefile = open('/tmp/tagcache.txt','w')
    print('cachetag building ' )
    #for line in filelist:
    #    line=line.strip()
    #    #print('cachetages: line: '+line)
    #    tags = taghandler.exifGetComment(line)
    #    #print('tags for it: '+ tags )
    #    #print(line + ',' +  tags)
    #    cachefile.write(line + ',' +  tags+'\n')
    #filelist.close()
    #cachefile.close()
    builder.buildPageFromCache()

print('forking tagcacher!')
p = Process(target=cachetags)
p.start()

