# taghandler.py
# this handles tagging

# dependancies = exiftool
# python{2,3} cant do exif by itself

# TODO redo the functions using piexif instead of exiftool because exiftool using subprocess is very unstable and inconsistant and requires a lot of hacks to make work 50% of the time

import subprocess
import time

def sleep(n):
    #time.sleep(n)
    return

def exifGetComment(filename):
    print('get comment broke have some trash')
    return 'trashtags'
    #print('exifGetComment')
    try: # some images have no comment field. 
        exiflist = subprocess.check_output(["exiftool",filename], universal_newlines=True ).split("\n")
        for tag in exiflist:
            comments = ""
            if 'Comment' in tag :
                c = tag.split(':')[0] 
                print('looking at ' + c)
                sleep(4)
                if not c.startswith('Comment'):
                    print(c + " is not Comment")
                    continue
                print('exifGetComment returns a list' + tag)
                comments = tag.split(':')[1].strip().replace('"','')

        print('got tags: ' + comments)
        sleep(1)
        if comments == '':
            print(filename + ' looks empty')
            exifNukeAll(filename)
            exifSetComment(filename,'notags')
            sleep(1)
            return exifGetComment(filename)
        sleep(1)
        print('exifGetComment returning: ' + comments)
        sleep(1)
        return comments
        return tag.split(':')[1].strip().replace('"','')

        exifSetComment(filename,'notags')
        return "notags"
    except: 
        #print('exifGetComment returns notags')
        exifSetComment(filename,'notags')
        return "notags"

def exifSetComment(filename,tags):
    print('setcomment: ' + filename + ' , ' + tags  )
    exiflist = subprocess.check_output(["exiftool",'-Comment="' + tags + '"',filename,'-overwrite_original_in_place'], universal_newlines=True ).split("\n")
    print('command returned with: ' + str(exiflist) )
    return

def exifNukeAll(filename):
    exiflist = subprocess.check_output(["exiftool",'-All= ', filename], universal_newlines=True ).split("\n")
    shutils.move(filename+'_original',filename)
    print('command returned with: ' + str(exiflist)  )

def addtag(filename,tag):
    print("tag handler add tag: " + tag)

    # setup
    tag = tag.replace("%2C",',')
    print('looking at: ' + tag)
    currenttags = exifGetComment(filename).split(',')
    newtags = tag.split(',')

    # remove empty elements
    print('remove empty eles')
    currenttags[:] = [item for item in currenttags if item != '']
    newtags[:] = [item for item in newtags if item != '']

    # copy into another array because python
    print('copy into new array')
    tagstoadd = newtags[:]
    for t in tagstoadd:
        print(t)
   
    # process list of new tags
    print('looking at adding: ' + str(newtags))
    for ctag in currenttags:
        print('current tag: ' + ctag)
        for ntag in newtags:
            print('current tag: ' + ctag + ' vs ' + ntag)
            if ntag == ctag:
                print('tag already exists')
                tagstoadd.remove(ntag)

    print('adding newtags: '+ str(tagstoadd))
    if not tagstoadd:
        print('no tags to add')
    else:
        for tag in tagstoadd:
            currenttags.append(tag)
        newtags = ""
        for tag in currenttags:
            if 'notags' in tag:
                continue
            newtags += tag+','
        newtags = newtags[:-1]
        print(newtags)
        exifSetComment(filename,newtags)
            
    print('fin')
    return
