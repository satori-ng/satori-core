import logging

try:
	from termcolor import colored
except ImportError:
	def colored(*args, **kwargs):
		return args[0] 

LOG_LEVEL = logging.INFO

class MyFormatter(logging.Formatter):

	dbg_fmt  = colored("[@]: %(module)s: %(lineno)d: %(msg)s", "grey")
	err_fmt  = colored("[-]: %(msg)s", "red")
	warn_fmt = "[!] %(msg)s"
	info_fmt = colored("[+] %(msg)s", "green")


	def __init__(self, fmt="%(levelno)s: %(msg)s"):
		# logging.Formatter.__init__(self, fmt=fmt)
		super().__init__(fmt=fmt, datefmt=None, style='%')

	def format(self, record):

		# Save the original format configured by the user
		# when the logger formatter was instantiated
		format_orig = self._style._fmt

		# Replace the original format with one customized by logging level
		if record.levelno == logging.DEBUG:
			self._style._fmt = MyFormatter.dbg_fmt

		elif record.levelno == logging.INFO:
			self._style._fmt = MyFormatter.info_fmt

		elif record.levelno == logging.ERROR:
			self._style._fmt = MyFormatter.err_fmt

		elif record.levelno == logging.WARN:
			self._style._fmt = MyFormatter.warn_fmt

		# Call the original formatter class to do the grunt work
		result = logging.Formatter.format(self, record)

		# Restore the original format configured by the user
		self._style._fmt = format_orig

		return result


handler = logging.StreamHandler()
fmt = MyFormatter('%(message)s')
handler.setFormatter(fmt)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)

