import os
import operator
import pathlib
import functools
import collections

from satoricore.common import _STANDARD_EXT as SE


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

    def __init__(self, entrypoints, excluded_dirs, image=os):

        if not isinstance(entrypoints, collections.Iterable):
            entrypoints = [entrypoints]

        entrypoints_valid = functools.reduce(
            operator.and_,
            [isinstance(entrypoint, str) for entrypoint in entrypoints]
        )

        if not entrypoints_valid:
            raise Exception('Invalid list of entrypoints provided')

        if excluded_dirs is None:
            excluded_dirs = set()

        self.image = image
        self.entrypoints = entrypoints
        self.excluded_dirs = [
            d.rstrip(self.image.path.sep)
            for d in excluded_dirs
        ]

    def _iter_entrypoints(self):
        for entrypoint in self.entrypoints:
            # Iterate over the list from top top bottom so that we may edit the
            # list of directories to be traversed according to the list of
            # excluded dirs.

            entry_parts = pathlib.PurePath(entrypoint).parts
            to_yield_parts = []
            entry_path_construct = pathlib.PurePath()
            for entry_part in entry_parts:
                entry_path_construct /= entry_part
                to_yield_parts.append(str(entry_path_construct))
            print (to_yield_parts)
            yield (to_yield_parts, [])

            for _root, _dirs, _files in self.image.walk(entrypoint, topdown=True):
                root = self.image.path.abspath(_root)
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

                yield (dirs, files)

    def __call__(self):
        for dirs, files in self._iter_entrypoints():
            for _dir in dirs:
                yield (_dir, SE.DIRECTORY_T)

            for _file in files:
                yield (_file, SE.UNKNOWN_T)
