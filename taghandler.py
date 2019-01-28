# taghandler.py
# this handles tagging

# dependancies = exiftool
# python{2,3} cant into exif

import subprocess

def exifGetComment(filename):
    #print('exifGetComment')
    try: # some images have no comment field. 
        exiflist = subprocess.check_output(["exiftool",filename], universal_newlines=True ).split("\n")
        for tag in exiflist:
            if 'Comment' in tag :
                #print('exifGetComment returns a list')
                return tag.split(':')[1].strip().replace('"','')
                break
        return "notags"
    except: 
        #print('exifGetComment returns notags')
        return "NoTags"

def exifSetComment(filename,tags):
    print('setcomment')
    exiflist = subprocess.check_output(["exiftool",'-Comment="' + tags+ '"',filename,'-overwrite_original_in_place'], universal_newlines=True ).split("\n")
    print(exiflist)
    return

def addtag(filename,tag):
    print("tag handler add tag: " + tag)

    # setup
    tag = tag.replace("%2C",',')
    print('looking at: ' + tag)
    currenttags = exifGetComment(filename).split(',')
    newtags = tag.split(',')

    # remove empty elements
    currenttags[:] = [item for item in currenttags if item != '']
    newtags[:] = [item for item in newtags if item != '']

    # copy into another array because python
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

    # add tags
    print('adding newtags: '+ str(tagstoadd))
    if not tagstoadd:
        print('no tags to add')
    else:
        for tag in tagstoadd:
            currenttags.append(tag)
        newtags = ""
        for tag in currenttags:
            newtags += tag+','
        newtags = newtags[:-1]
        print(newtags)
        exifSetComment(filename,newtags)
            
    print('fin')
    return
