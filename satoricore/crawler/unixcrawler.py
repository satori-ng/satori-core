from .basecrawler import BaseCrawler


class UnixCrawler(BaseCrawler):
    def __init__(self, entrypoints, excluded_dirs=set()):
        excluded_dirs.union([
            '/proc',
            '/sys',
            '/dev',
            '/tmp'
        ])

        super().__init__(entrypoints, excluded_dirs)
