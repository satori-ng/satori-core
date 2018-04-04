import os
import os.path

from satoricore.image import SatoriImage, _DIRECTORY_T, _FILE_T

system_root = os.path.abspath(os.sep)


def crawler(root_dir=system_root,
            plugins=None,
            excluded_dirs=set(),
            crawled_object=os,
            satori_image=SatoriImage(),
            ):

    # Iterate over the list from top top bottom so that we may edit the list
    # of directories to be traversed according to the list of excluded dirs.
    for _root, _dirs, _files in os.walk(root_dir, topdown=True):

        root = os.path.abspath(_root)
        # TODO: This is most probably not needed. Remove after further testing.
        if root in excluded_dirs:
            continue

        # Edit _dirs inplace to avoid iterating over subdirectories of
        # directories in the excluded_dirs iterable.
        # Only works with topdown=True
        _dirs[:] = [
            d
            for d in _dirs
            if os.path.join(root, d) not in excluded_dirs
        ]
        dirs = [os.path.join(root, d) for d in _dirs]
        files = [os.path.join(root, f) for f in _files]

        for _dir in dirs:
            satori_image.add_file(_dir, type=_DIRECTORY_T)

        for _file in files:
            satori_image.add_file(_file, type=_FILE_T)

    return satori_image
