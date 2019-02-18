# myapp.py
# this is the server that runs everything

import os
import time
import tagpage
import taghandler
import json # for the tag page. maybe move to new file

# =========================================================== functions
def str_get_txt(file):
    try:
        with open(file,'r') as f:
            return f.read()
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        x, y = inst.args     # unpack args
        print('x =', x)
        print('y =', y)
        print("we are in : " + os.getcwd())

def get_file(file):
    print("get file getting: " +file)
    try:
        with open(file.replace("%20"," "),'rb') as f:
            return f.read()
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        x, y = inst.args     # unpack args
        print('x =', x)
        print('y =', y)
        print("we are in : " + os.getcwd())

# =========================================================== setup

htmldir = os.getcwd() + "/html/"

# pick the fastest worker to go and do some other stuff
first=False
try:
    os.mkdir("fight")
    print("i win")
    first=True
except:
    pass

if first == True:
    time.sleep(0.5)
    os.rmdir("fight")


if first == True:
    print('thread1 start tagcacher')
    import tagcacher

# go to where the images are
os.chdir(htmldir+'/..')
os.chdir('..')

print("well...")

# =========================================================== app - main

def app(environ, start_response):
    uri=environ['RAW_URI']
    print(uri)

    print('worker running at: ' + os.getcwd() )

    # handle /
    # the only page this has to server is the dynamic one that shows all the tags
    # that should be handled in the page itself.
    # the page makes a javascript ask for the images for a given tag which
    # defaults to the 'all' tag
    if uri == '/':
        data = str_get_txt('project_display/html/header.html')
        data += str_get_txt('project_display/html/content.html')
        data += str_get_txt('project_display/html/footer.html')
        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data.encode()])

    # tag page poc
    if '/tagpage?tag=' in uri:
        print('====tagpage')
        tags = uri.split('=')[1]         
        print( tags )
        data = str_get_txt('project_display/html/header.html')
        data += "<script> tag = \"" + tags + "\"</script> \n"
        data += str_get_txt('project_display/html/content.html')
        data += str_get_txt('project_display/html/footer.html')
        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data.encode()])

    # req tags list
    if '/reqtags?tag=' in uri:
        print('====reqtags')
        # for sanity sake taghandler should make this json object
        tags = uri.split('=')[1]         
        print( tags )

        files = taghandler.getFiles(tags) 
        files = files.split(',')
        print(files)

        jsono = {}
        count=0
        for f in files:
            jsono['key'+str(count)] = f
            count+=1
        	
     
        #jsono['key99999'] = 'value'
        data = json.dumps(jsono)

        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data.encode()])     

    # handle jpg 
    if uri.endswith("jpg"):
        print('requested a jpg')
        try :
            data = get_file("."+uri)
            start_response("200 OK", [
                ("Content-Type", "image/jpeg"),
                ("Content-Length", str(len(data)))
            ])
            print("jpg return")
            return iter([data])    
        except:
            print("get jpg failed")
 
    # handle png
    if uri.endswith(".png"):
        print('requested a png')
        try :
            data = get_file("."+uri)
            start_response("200 OK", [
                ("Content-Type", "image/png"),
                ("Content-Length", str(len(data)))
            ])
            print("png return")
            return iter([data])    
        except:
            print("get png failed")

    # handle gif
    if uri.endswith(".gif"):
        print('requested a gif')
        try :
            data = get_file("."+uri)
            start_response("200 OK", [
                ("Content-Type", "image/gif"),
                ("Content-Length", str(len(data)))
            ])
            print("gif return")
            return iter([data])    
        except:
            print("gif png failed")

    # handle ico
    if uri.endswith(".ico"):
        print('requested a ico')
        try :
            data = get_file(htmldir + "favicon.ico" )
            start_response("200 OK", [
                ("Content-Type", "image/ico"),
                ("Content-Length", str(len(data)))
            ])
            print("ico return")
            return iter([data])    
        except:
            print("ico failed")

    # handle show tags
    #if 'tagfilter' in uri:
    #    print('tag filter page')
    #    data = str_get_txt('project_display/html/header.html')
    #    data += "\n the uri was " + uri + " \n"
    #    data += tagpage.maketagpage(uri)
    #    data += str_get_txt('project_display/html/footer.html')
    #    start_response("200 OK", [
    #        ("Content-Type", "text/html"),
    #        ("Content-Length", str(len(data)))
    #    ])
        return iter([data.encode()])     

    # handle add tag
    if '/command:addtag:item:' in uri:
        print('add tag!')
        taghandler.addTagsFromUri(uri)
        data = "tag accepted"
        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data.encode()])

    # easteregg
    # if uri is /cats or something, have a funny picture or whatever

    # 404 page catchall 
    data = str_get_txt('project_display/html/404.html')
    start_response("404 Not Found", [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(data)))
    ])
    print("404 return")
    return iter([data.encode()])     
