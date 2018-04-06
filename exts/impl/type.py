import os
import stat

from exts.crawler import hook

_DIRECTORY_T = 'D'
_FILE_T = 'F'
_LINK_T = 'L'
_BLOCK_DEVICE_T = 'B'
_CHAR_DEVICE_T = 'C'
_FIFO_T = 'I'
_SOCKET_T = 'S'
_UNKNOWN_T = 'U'

st_mode_mapper = {
    stat.S_IFBLK: _BLOCK_DEVICE_T,
    stat.S_IFCHR: _CHAR_DEVICE_T,
    stat.S_IFIFO: _FIFO_T,
    stat.S_IFLNK: _LINK_T,
    stat.S_IFSOCK: _SOCKET_T,
}


@hook("pre_open")
def filetype(satori_image, full_path):
    mode = stat.S_IFMT(os.lstat(full_path).st_mode)
    _type = st_mode_mapper.get(mode, _UNKNOWN_T)
    filedict = satori_image.set_attribute(full_path, {},
                                          "type", force_create=True)
    filedict["type"] = _type
