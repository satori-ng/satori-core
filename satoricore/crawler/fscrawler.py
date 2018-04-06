import os
import stat

from exts.crawler import _extensions as extensions
from satoricore.image import SatoriImage

system_root = os.path.abspath(os.sep)


def crawler(root_dir=system_root,
            plugins=None,
            excluded_dirs=set(),
            crawled_object=os,
            satori_image=SatoriImage(),
            ):

    extensions["on_start"](root_dir=root_dir,
                           excluded_dirs=excluded_dirs,
                           crawled_object=crawled_object,
                           satori_image=satori_image)

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
            satori_image.add_file(_dir)
            extensions["pre_open"](full_path=_dir, satori_image=satori_image)
            # fd = open(_dir)
            # extensions["with_open"](full_path=_dir, satori_image=satori_image)
            # fd.close()
            extensions["post_close"](full_path=_dir, satori_image=satori_image)

        for _file in files:
            mode = stat.S_IFMT(os.lstat(_file).st_mode)
            _type = st_mode_mapper.get(mode, _UNKNOWN_T)
            satori_image.add_file(_file, type_=_type)
            extensions["pre_open"](full_path=_file, satori_image=satori_image)
            try:
                fd = open(_file)
                extensions["with_open"](full_path=_file, satori_image=satori_image)
                fd.close()
            except Exception:
                pass
            extensions["post_close"](full_path=_file, satori_image=satori_image)

    extensions["on_end"](satori_image)
    return satori_image
