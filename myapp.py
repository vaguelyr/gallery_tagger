# myapp.py
# this is the server that runs everything

import os
import time
import tagpage

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

# go to where the images are
os.chdir(htmldir+'/..')
os.chdir('..')

if first == True:
    try:
        os.remove(htmldir + "content.html")
    except:
        pass
    os.symlink( htmldir + "content_waiting.html", htmldir + "content.html" )
    import builder
    builder.buildPage()
    import tagcacher

print("well...")

# =========================================================== app - main

def app(environ, start_response):
    uri=environ['RAW_URI']
    print(uri)

    print('worker running at: ' + os.getcwd() )

    # handle /
    if uri == '/':
        data = str_get_txt('project_display/html/header.html')
        data += str_get_txt('project_display/html/content.html')
        data += str_get_txt('project_display/html/footer.html')
        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data.encode()])     

    # handle jpg 
    if uri.endswith("jpg"):
        print('requested a jpg lmao')
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
    if 'tagfilter' in uri:
        print('tag filter page')
        data = str_get_txt('project_display/html/header.html')
        data += "\n the uri was " + uri + " \n"
        data += tagpage.maketagpage(uri)
        data += str_get_txt('project_display/html/footer.html')
        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data.encode()])     

    # handle add tag
    if '/command:add_tag:item:' in uri:
        print('add tag!')
        tagpage.tagImageFromURI(uri)
        data = "tag accepted"
        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
        ])
        return iter([data.encode()])

    # 404 page
    data = str_get_txt('project_display/html/404.html')
    start_response("404 Not Found", [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(data)))
    ])
    print("404 return")
    return iter([data.encode()])     
