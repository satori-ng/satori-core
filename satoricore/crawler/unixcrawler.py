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
    def __init__(self, entrypoints, excluded_dirs=set()):
        excluded_dirs.union([
            '/proc',
            '/sys',
            '/dev',
            '/tmp'
        ])

        super().__init__(entrypoints, excluded_dirs)
