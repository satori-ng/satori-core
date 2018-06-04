import logging

try:
	from colorama import colored
except ImportError:
	def colored(*args, **kwargs):
		return args[0] 

LOG_LEVEL = logging.WARN

handler = logging.StreamHandler()
fmt = logging.Formatter('%(message)s')
handler.setFormatter(fmt)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)

handler = logging.StreamHandler()
fmt = logging.Formatter('%(filename)s:%(lineno)d:%(message)s')
handler.setFormatter(fmt)

logger = logging.getLogger("{}_debug"__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)


class MyFormatter(logging.Formatter):

    err_fmt  = "ERR: %(msg)s"
    dbg_fmt  = "DBG: %(module)s: %(lineno)d: %(msg)s"
    warn_fmt = "[!] "
    info_fmt = "%(msg)s"


    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)


    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = MyFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._fmt = MyFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._fmt = MyFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._fmt = format_orig

        return result