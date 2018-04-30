import os
import os.path
import stat
from hooker import hook
from satoricore.common import _STANDARD_EXT

ST_MODE_MAPPER = {
    stat.S_IFBLK: _STANDARD_EXT.BLOCK_DEVICE_T,
    stat.S_IFCHR: _STANDARD_EXT.CHAR_DEVICE_T,
    stat.S_IFIFO: _STANDARD_EXT.FIFO_T,
    stat.S_IFLNK: _STANDARD_EXT.LINK_T,
    stat.S_IFSOCK: _STANDARD_EXT.SOCKET_T,
    stat.S_IFREG: _STANDARD_EXT.FILE_T,
}


__name__ = 'stat'

def stat_obj_to_dict(stat_obj):
    pass

@hook("imager.pre_open")
def get_stat_info(satori_image, file_path, file_type):
    file_stat = os.lstat(file_path)

    if file_type != _STANDARD_EXT.DIRECTORY_T:
        mode = stat.S_IFMT(file_stat.st_mode)
        file_type = ST_MODE_MAPPER.get(mode, _STANDARD_EXT.UNKNOWN_T)
    if file_type == _STANDARD_EXT.LINK_T:
        points_to = os.path.realpath(file_path)
        print(points_to)
        satori_image.set_attribute(file_path, points_to,
                                   'link', force_create=False)

    times_dict = {
        'atime': file_stat.st_atime,
        'mtime': file_stat.st_mtime,
        'ctime': file_stat.st_ctime,
    }

    # Translates lstat's attributes to a dict
    stat_dict = {x[3:]: getattr(file_stat, x) for x in dir(file_stat)
                 if x.startswith("st_") and "time" not in x}

    satori_image.set_multiple_attributes(
                file_path,
                    ('stat', stat_dict),
                    ('times', times_dict),
                    ('type', file_type),
                force_create=False,
                )



@hook("differ.pre_open")
def diff_stat_info(file_path, file_type, source, destination, results):
    s_stat = source.lstat(file_path)
    d_stat = destination.lstat(file_path)

    stat_keys = set(x for x in dir(s_stat) if x.startswith('st') ) | set(x for x in dir(d_stat) if x.startswith('st') )

    s_times_dict = {
        'atime': s_stat.st_atime,
        'mtime': s_stat.st_mtime,
        'ctime': s_stat.st_ctime,
    }
    d_times_dict = {
        'atime': d_stat.st_atime,
        'mtime': d_stat.st_mtime,
        'ctime': d_stat.st_ctime,
    }

    time_diff_dict = {}
    diffs = {}
    for k in stat_keys:
        try:
            s_value = getattr(s_stat, k)
            d_value = getattr(d_stat, k)
            diff = d_value - s_value
            if diff != 0:

                if "time" in k:
                    time_diff_dict[k] = diff
                    continue

                diffs[k] = diff
        except AttributeError:
            pass
            continue

    if time_diff_dict:
        results.set_attribute(file_path, time_diff_dict, 'times.diff', force_create=True)

    if diffs:
        results.set_attribute(file_path, diffs, 'stat.diff', force_create=True)


