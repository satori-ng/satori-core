import queue
import os
import os.path

import satoricore
import satoricore.image

system_root = os.path.abspath(os.sep)
__file_queue = queue.Queue()



def crawler(root_dir = system_root,
            plugins = None,
            excluded_dirs = set(),
            crawled_object = os,
            satori_image = satoricore.image.SatoriImage(),
            ):

    global __file_queue

    # while not __file_queue.empty():

    for f in crawled_object.listdir(root_dir) :
        full_path = os.path.join([root_dir, f])

        if os.path.isdir(full_path) :
            
            if full_path in excluded_dirs:
                continue
            __file_queue.put(full_path)

        elif os.path.islink(full_path):
            pass
        elif os.path.isfile(full_path):
            pass