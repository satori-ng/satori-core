import os
import time

from hooker import hook
from satoricore.image import _META_SECTION

__name__ = 'sysinfo'


@hook("imager.on_start")
def set_timestamp(parser, args, satori_image):

	times = {}
	times['tstamp'] = time.time()
	times['unix'] = date=time.ctime()
	times['tz-secs'] = tz=time.timezone

	satori_image.add_class("timestamp", section=_META_SECTION, data=times)
