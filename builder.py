# builder.py
# this generates the main page list of all images

import os
import taghandler

print("builder running")

htmldir = os.getcwd() + "/project_display/html/"

filelist = '/tmp/list.txt'
tagcache = '/tmp/tagcache.txt'

content1 = htmldir + "content1.html"
content2 = htmldir + "content2.html"

print('builder working from: ' + os.getcwd());

# this needs to only generate the /tmp/list.txt
def buildPage():

    f = open(filelist , 'w')
    index = 1
    for root, dirs, files in os.walk(".", topdown = True):
        for name in files:
            filename = os.path.join(root, name)
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif'):
                f.write(filename + '\n')

    f.close()

    print("builder finished")

# this needs to make the actual page
def buildPageFromCache():
    print('build page from Cache')
    tagcachefile = open(tagcache , 'r')
    content = open(content2, 'w')

    index = 1
    for line in tagcachefile:
        print('building page from Cache: ' + line)
        imgfile = line.split(',')[0]
        content.write('<div id="' + str(index) + '" > \n')
        content.write('<img src="' + imgfile + '" alt="image" style="width:100%; height:auto;"></body> <br>\n' )
        content.write( imgfile + '<br>\n')

        content.write('---------------------------------------------<br> \n')
        content.write(""" add tag 
        <form action="/command:add_tag:item:{itemno}" method="get" target="dummyframe" >
        <input list="tags" name="tag">
        <datalist id="tags">

        <!-- this business needs to come from the cache file. before starting read through all the tags to find the n most popular -->

        <option value="tag1">
        <option value="tag2">
        <option value="tag3">
        </datalist>
        <input type="submit">
        </form> <br>
        """.format(itemno=index))
        #content.write(' <button onclick="comnd(2,ONE,1)">copy to home</button> <br> ')
        content.write('---------------------------------------------<br> \n')
        content.write('</div> \n\n')
        index += 1


    content.write('loaded ' + str(index) + 'images \n\n')
    content.write('<iframe width="0" height="0" border="0" name="dummyframe" id="dummyframe"></iframe>')

    tagcachefile.close()
    content.close()

    os.remove(htmldir + "content.html")
    os.symlink(htmldir + "content2.html" , htmldir + "content.html")
    print("builder finished")


