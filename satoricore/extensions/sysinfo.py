import os
import platform

from hooker import hook
import satoricore

__name__ = 'sysinfo'


@hook("imager.on_start")
def sysinfo(parser, args, satori_image):
    satori_meta = {}
    system_meta = {}

    satori_meta = {}
    satori_meta['version'] = satoricore.__version__
    satori_meta['extensions'] = []

    system_meta['type'] = platform.system()
    system_meta['platform'] = platform.platform()
    system_meta['hostname'] = platform.node()
    system_meta['machine'] = platform.machine()
    system_meta['release'] = platform.release()
    system_meta['processor'] = platform.processor()
    # system_meta['specifics'] = {}

    satori_image.set_metadata(system_meta, 'system')
    satori_image.set_metadata(satori_meta, 'satori')

    try:
        # Why you "FileNotFoundError" dude?
        system_meta['user'] = os.getlogin()
    except:
        pass

    # try :
    #     system_meta['specifics']['win'] = \
    #        platform.win32_ver()
    # except :
    #     pass
    # try :
    #     system_meta['specifics']['mac'] = \
    #        platform.mac_ver()
    # except :
    #     pass
