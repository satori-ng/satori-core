import logging

try:
	from termcolor import colored
except ImportError:
	def colored(*args, **kwargs):
		return args[0] 

LOG_LEVEL = logging.INFO

# Found in:
# 'https://stackoverflow.com/questions/14844970/modifying-logging-message-format-based-on-message-logging-level-in-python3'

class SatoriLogFormatter(logging.Formatter):

	def __init__(self, fmt="%(levelno)s: %(msg)s", extension=False):
		super().__init__(fmt=fmt, datefmt=None, style='%')
		if extension:
			mod_tag = "<ext:%(module)s>"
		else:
			mod_tag = ""

		self.dbg_fmt  = colored(
			"[@]{} %(module)s: %(lineno)d: %(msg)s"
			.format(mod_tag),
			"grey", "on_green"
			)
		self.crit_fmt = colored("[X]{} %(msg)s".format(mod_tag), "red", attrs=["bold"])
		self.err_fmt  = colored("[-]{} %(msg)s".format(mod_tag), "red")
		self.warn_fmt = colored("[!]{} %(msg)s".format(mod_tag), "green")
		self.info_fmt = colored("[+]{} %(msg)s".format(mod_tag), "cyan")

	def format(self, record):

		# Save the original format configured by the user
		# when the logger formatter was instantiated
		format_orig = self._style._fmt

		# Replace the original format with one customized by logging level
		if record.levelno == logging.DEBUG:
			self._style._fmt = self.dbg_fmt

		elif record.levelno == logging.INFO:
			self._style._fmt = self.info_fmt

		elif record.levelno == logging.ERROR:
			self._style._fmt = self.err_fmt

		elif record.levelno == logging.WARN:
			self._style._fmt = self.warn_fmt

		elif record.levelno == logging.CRITICAL:
			self._style._fmt = self.crit_fmt

		# Call the original formatter class to do the grunt work
		result = logging.Formatter.format(self, record)

		# Restore the original format configured by the user
		self._style._fmt = format_orig

		return result


handler = logging.StreamHandler()
fmt = SatoriLogFormatter()
handler.setFormatter(fmt)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)


def set_quiet_logger():
	global logger
	logger.setLevel(logging.WARN)


def set_debug_logger():
	global logger
	logger.setLevel(logging.DEBUG)



ext_handler = logging.StreamHandler()
ext_fmt = SatoriLogFormatter('%(message)s', extension=True)
ext_handler.setFormatter(ext_fmt)

ext_logger = logging.getLogger("{}_ext".format(__name__))
ext_logger.setLevel(LOG_LEVEL)
ext_logger.addHandler(ext_handler)
