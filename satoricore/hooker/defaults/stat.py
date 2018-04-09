import os
import stat

from satoricore.hooker import hook

_DIRECTORY_T = 'D'
_FILE_T = 'F'
_LINK_T = 'L'
_BLOCK_DEVICE_T = 'B'
_CHAR_DEVICE_T = 'C'
_FIFO_T = 'I'
_SOCKET_T = 'S'
_UNKNOWN_T = 'U'

ST_MODE_MAPPER = {
    stat.S_IFBLK: _BLOCK_DEVICE_T,
    stat.S_IFCHR: _CHAR_DEVICE_T,
    stat.S_IFIFO: _FIFO_T,
    stat.S_IFLNK: _LINK_T,
    stat.S_IFSOCK: _SOCKET_T,
}


@hook("pre_open")
def get_stat_info(satori_image, file_path, file_type):
    file_stat = os.lstat(file_path)

    if file_type != _DIRECTORY_T:
        mode = stat.S_IFMT(file_stat.st_mode)
        file_type = ST_MODE_MAPPER.get(mode, _UNKNOWN_T)
