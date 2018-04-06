import os
import stat
import operator
import functools
import collections

from satoricore.image import (
    _LINK_T,
    _BLOCK_DEVICE_T,
    _CHAR_DEVICE_T,
    _FIFO_T,
    _SOCKET_T,
    _UNKNOWN_T,
    _DIRECTORY_T
)

st_mode_mapper = {
    stat.S_IFBLK: _BLOCK_DEVICE_T,
    stat.S_IFCHR: _CHAR_DEVICE_T,
    stat.S_IFIFO: _FIFO_T,
    stat.S_IFLNK: _LINK_T,
    stat.S_IFSOCK: _SOCKET_T,
}


class BaseCrawler:
    """
    A basic filesystem crawler. Iterates recursively over the specified
    entrypoints and yields file/folder name, type, and the structure returned
    by os.lstat.

    Examples:
        crawler = BaseCrawler('/')
        for filename, filetype, filestats in crawler():
            # Do stuff

        crawler = BaseCrawler(['C:\\', 'D:\\Backup'], ['C:\\Users\\Admin'])
        for filename, filetype, filestats in crawler():
            # Do stuff
    """

    def __init__(self, entrypoints, excluded_dirs=set()):

        if not isinstance(entrypoints, collections.Iterable):
            entrypoints = [entrypoints]

        entrypoints_valid = functools.reduce(
            operator.and_,
            [isinstance(entrypoint, str) for entrypoint in entrypoints]
        )

        if not entrypoints_valid:
            raise Exception('Invalid list of entrypoints provided')
        self.entrypoints = entrypoints
        self.excluded_dirs = excluded_dirs

    def __call__(self):
        for entrypoint in self.entrypoints:
            # Iterate over the list from top top bottom so that we may edit the
            # list of directories to be traversed according to the list of
            # excluded dirs.
            for _root, _dirs, _files in os.walk(entrypoint, topdown=True):

                root = os.path.abspath(_root)
                # TODO: This is most probably not needed. Remove after further
                # testing.
                if root in self.excluded_dirs:
                    continue

                # Edit _dirs inplace to avoid iterating over subdirectories of
                # directories in the excluded_dirs iterable.
                # Only works with topdown=True
                _dirs[:] = [
                    d
                    for d in _dirs
                    if os.path.join(root, d) not in self.excluded_dirs
                ]
                dirs = [os.path.join(root, d) for d in _dirs]
                files = [os.path.join(root, f) for f in _files]

                for _dir in dirs:
                    dir_stat = os.lstat(_dir)
                    yield (_dir, _DIRECTORY_T, dir_stat)

                for _file in files:
                    file_stat = os.lstat(_file)
                    mode = stat.S_IFMT(file_stat.st_mode)
                    _type = st_mode_mapper.get(mode, _UNKNOWN_T)
                    yield (_file, _type, file_stat)
