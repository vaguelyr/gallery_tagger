# vague
# tag handler using sql in python

import time

import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()

table = 'tagtable'
imageStorageDir = 'testdbdir/files/'
default_tag = 'all'
imageDir = '/home/vague/Pictures/walls/'

def init_tag_table(table):
    """ Create the table. 
        Hash is declared unique to avoid duplicate files efficiently .
    """
    c.execute(f'''CREATE TABLE IF NOT EXISTS {table}
                 ( id INTEGER PRIMARY KEY,  hash text, tags text, ext text, date text, UNIQUE(hash)
)''')

def add_row(table,data1, data2, data3):
    """ Adds fields to the db. 
        Since all the values are handled by hash, and hash is declared unique,
            the table has no duplicate entries. 
        This allows for duplicate files to be automatically handled since 
            1) Only one copy is kept internally, named by hash.
                State changes caused by possible collisions can be avoided by 
                not overwriting files or by overwriting files completely.
            2) Managing by hash assures any duplicates are ignored completely. 
    """
    c.execute(f'''INSERT or ignore into {table} VALUES (NULL, '{data1}', '{data2}', '{data3}', '{str(int(time.time()))}'
)''')


def process_folder(folderpath):
    """ Walk through a specified folder and all its subfolders 
        and add files to the db according to file extention. 
        Copies found files to the storage directory.
            This removes the need to keep track of external files. 
    """
    exts = ('.jpg' , '.jpeg', '.gif' , '.png' )
    # files are loaded into ram for hashing
    file_size_limit = (500 * 1000 * 1024 ) # limit 500 MB
    write_every = 1000
    count = 0

    import os
    import hashlib
    from shutil import copyfile

    hasher = hashlib.md5()

    for root, dirs, files in os.walk(folderpath, topdown = False):
        for name in files:
            if (name.endswith(exts)):
                name = os.path.join(root, name)
                if ( os.path.getsize(name) > file_size_limit): 
                    print('actually too big')
                    continue
                print('=================================================')
                print(name)
                with open (name, 'rb') as n:
                    hasher.update(n.read())
                    result = hasher.hexdigest()

                print(result)
                print(default_tag)
                ext = os.path.splitext(name)[1][1:]
                print(ext)

                copyfile(name, imageStorageDir + '/' + result)
                add_row(table,result,default_tag,ext)

                count += 1
                if ( count >= write_every ):
                    conn.commit()
                    count = 0

def set_tags(hashvalue,tags):
    """ Overwrite the current tags with new tags """
    print('set_tags ' + hashvalue + ' ' + tags)
    c.execute(f'''update tagtable
        set tags = '{tags}'
        where hash = '{hashvalue}'; ''')

def get_tags(hashvalue):
    """ Returns the tags string from a specified entry """
    print('get_tags')
    result = c.execute(f'''select tags from tagtable where hash = '{hashvalue}'; ''').fetchone()[0]
    return result

def append_tags(hashvalue,new_tags):
    """ Appends tags to the tag field. 
        Tags are stored in the db as 
        comma delimited strings.  
        Removes duplicates.
    """
    print('append_tags')
    tags = get_tags(hashvalue).split(',')
    tags.append(new_tags)
    tags = list(set(tags)) # set conversion removes duplicates
    set_tags(hashvalue,','.join(tags))

def delete_tags(hashvalue, del_tags):
    """ Removes tags from specific entries specified by hash. """
    print('delete_tags')
    tags = get_tags(hashvalue).split(',')
    for dt in del_tags.split(','):
        try:
            tags.remove(dt)
        except:
            pass
    set_tags(hashvalue,','.join(tags))

def search_tags(tags):
    """ Returns a list of hashes corresponding to the search. """
    print('search_tags')
    results = []
    for t in tags.split(','):
        # returns a list of sets
        r = c.execute(f'''select hash from {table} 
                        where tags like '%{t}%'; 
        ''').fetchall()
        # turn the list of sets into a list
        for res in r:
                results.append(','.join(list(res)))
    return results


#init_tag_table(table)
#process_folder(imageDir)
#set_tags('cd294fc5f88ad67d17fce5ce245d7411' , 'flip')
#append_tags('cd294fc5f88ad67d17fce5ce245d7411' , 'flip')
#append_tags('cd294fc5f88ad67d17fce5ce245d7411' , 'flip2')
#delete_tags('cd294fc5f88ad67d17fce5ce245d7411' , 'flip2')
#append_tags('cd294fc5f88ad67d17fce5ce245d7411' , 'flip3')
#print(get_tags('cd294fc5f88ad67d17fce5ce245d7411'))
#print(search_tags('flip3'))
#append_tags('cdca4c55c3117d0ae307588aea58f7e5' , 'tile')

#conn.commit()
#conn.close()
print('done')
