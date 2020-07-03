import sqlite3
import hashlib # hash file
import shutil # copy file
import os
import time

database="gallery.db"
gallerydirectorypath="/home/vague/personal_projects/pythondbms/development/gallerydir/"

def deletetable():
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("drop TABLE IF EXISTS gallery")
    conn.commit()
    conn.close()

def createtable():
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS gallery (id INTEGER PRIMARY KEY,hash text unique,postdate bigint,sizekb int, filename text, meta bigtext )")
    conn.commit()
    conn.close()

def insert(thehash, postdate, sizekb,filename, meta):
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("INSERT or ignore INTO gallery (hash,postdate,sizekb,filename,meta) VALUES (?,?,?,?,?)",(thehash,postdate,sizekb,filename,meta))
    conn.commit()
    conn.close()

def show():
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("SELECT * FROM gallery ")
    rows=cur.fetchall()
    conn.close()
    return rows

def add_image(path):
    # hash the image
    hasher = hashlib.sha1() 
    with open(path, 'rb') as myfile:
        hasher.update(myfile.read())
    myhash = hasher.hexdigest()

    # get file size in kb
    sizekb = os.stat(path).st_size / 1000
    print(sizekb)
    
    # get file basename
    filename = os.path.basename(path)
    print(filename)

    # copy it to the gallery dir
    dest = gallerydirectorypath+"/"+myhash
    if not os.path.exists(dest):
        shutil.copyfile(path,dest)

    # insert data to db
    insert( myhash, time.time(), sizekb, path, "none" );
    conn.commit()

def set_meta(thehash, newmeta):
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("update gallery set meta='"+newmeta+"' where hash='"+thehash+"';")
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return get_meta(thehash)

def get_meta(thehash):
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("select meta from gallery where hash=\""+thehash+"\";")
    rows=cur.fetchall()[0][0]
    conn.close()
    return rows

