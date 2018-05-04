import os
import operator
import pathlib
import functools
import collections
from stat import S_ISDIR

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

            # Yield all directories up to the entrypoint:
            # Entrypoint: /var/www/html
            # Becomes: /, /var, /var/www, /var/www/html
            entry_parts = pathlib.PurePath(entrypoint).parts
            to_yield_parts = []
            entry_path_construct = pathlib.PurePath()
            for entry_part in entry_parts:
                entry_path_construct /= entry_part
                to_yield_parts.append(str(entry_path_construct))
            yield (to_yield_parts, [])

            # Create a Queue with the folder paths to crawl 
            _folder_list = [entrypoint]
            for _folder_consume in _folder_list:
                root_path = _folder_consume
                dirs = []
                files = []

                # For Every Folder to crawl get its contents
                try:
                    _folder_consume_contents = self.image.listdir(_folder_consume)
                except PermissionError: # TODO: log the failure as at 'info' level 
                    # If listing fails, just ignore
                    continue

                for _file in _folder_consume_contents:
                    # Contruct the full path of each file
                    file_full_path = self.image.path.join(root_path, _file)

                    # If file/folder is to be excluded - ignore
                    if file_full_path in self.excluded_dirs:
                        continue

                    # By default - treat it as regular file
                    list_to_append = files

                    # If it is a dorectory
                    mode = self.image.lstat(file_full_path).st_mode
                    if S_ISDIR(mode):
                        # Treat it as a directory
                        # Get it into queue to dive in later
                        list_to_append = dirs
                        _folder_list.append(file_full_path)

                    list_to_append.append(file_full_path)
                # yield all collected files from consumed directory
                yield (dirs, files)


    def __call__(self):
        for dirs, files in self._iter_entrypoints():
            for _dir in dirs:
                yield (_dir, SE.DIRECTORY_T)

            for _file in files:
                yield (_file, SE.UNKNOWN_T)
