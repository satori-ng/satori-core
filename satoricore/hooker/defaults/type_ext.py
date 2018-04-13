import os
import stat

from exts.crawler import hook
from satoricore.common import _STANDARD_EXT as SE

st_mode_mapper = {
    stat.S_IFBLK: SE.BLOCK_DEVICE_T,
    stat.S_IFCHR: SE.CHAR_DEVICE_T,
    stat.S_IFIFO: SE.FIFO_T,
    stat.S_IFLNK: SE.LINK_T,
    stat.S_IFSOCK: SE.SOCKET_T,
}


@hook("pre_open")
def filetype(satori_image, full_path):
    mode = stat.S_IFMT(os.lstat(full_path).st_mode)
    _type = st_mode_mapper.get(mode, SE.UNKNOWN_T)
    filedict = satori_image.set_attribute(full_path, {},
                                          "type", force_create=True)
    filedict["type"] = _type
