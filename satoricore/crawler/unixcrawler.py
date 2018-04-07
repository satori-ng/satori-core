import collections

from .basecrawler import BaseCrawler


class UnixCrawler(BaseCrawler):
    """
    Like BaseCrawler, performs filesystem crawling excluding Unix specific
    paths that contain temporary files that may disrupt the iteration of the
    filesystem. The following paths are excluded:
        /proc
        /sys
        /dev
        /tmp
    """
    def __init__(self, entrypoints, excluded_dirs):
        _excluded_dirs = {
            '/proc',
            '/sys',
            '/dev',
            '/tmp'
        }
        if isinstance(excluded_dirs, collections.Iterable):
            _excluded_dirs = _excluded_dirs.union(excluded_dirs)

        super().__init__(entrypoints, _excluded_dirs)
