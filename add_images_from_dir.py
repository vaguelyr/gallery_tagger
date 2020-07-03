# vague
# this script uses gallery_manager to add images to the db
# adds images from everywhere

import gallery_manager
import glob, os

gallery_manager.deletetable()
gallery_manager.createtable()

target_dir = "/"

valid_images = ["jpg","jpeg","gif","png","tga"]
for root, subdirs, files in os.walk(target_dir):
    for f in files:
        if (f.lower()[::-1].split('.')[0][::-1] not in valid_images):
            continue
        path = root+'/'+f
        if not os.path.exists(path):
            continue
        print(path)
        gallery_manager.add_image(path)
