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


@hook("imager.pre_open")
def get_stat_info(satori_image, file_path, file_type, os_context):
    file_stat = os_context.lstat(file_path)

    if file_type != _STANDARD_EXT.DIRECTORY_T:
        mode = stat.S_IFMT(file_stat.st_mode)
        file_type = ST_MODE_MAPPER.get(mode, _STANDARD_EXT.UNKNOWN_T)
    if file_type == _STANDARD_EXT.LINK_T:
        points_to = os_context.path.realpath(file_path)
        # print(points_to)
        satori_image.set_attribute(file_path, points_to,
                                   'link', force_create=False)

    # print (file_stat)
    times_dict = {}
    time_tags = ['st_atime', 'st_mtime', 'st_ctime']

    for tag in time_tags:
        try:
            # print (dir(file_stat))
            times_dict[tag.replace('st_','')] = getattr(file_stat, tag)
        except AttributeError:
            pass

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
def diff_stat_info(file_path, file_type, source, destination, results, diff_name):
    s_stat = source.lstat(file_path)
    d_stat = destination.lstat(file_path)

    stat_keys = set(x for x in dir(s_stat) if x.startswith('st_') ) & set(x for x in dir(d_stat) if x.startswith('st_') )
    time_keys = [ x for x in stat_keys if x.endswith('time') ]
    # print (file_path)
    s_times_dict = {}
    d_times_dict = {}
    for time_key in time_keys:
        s_times_dict[time_key] = getattr(s_stat, time_key)
        d_times_dict[time_key] = getattr(d_stat, time_key)

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

    times_attr = 'times.{diff_name}'.format(diff_name=diff_name)
    stat_attr = 'stat.{diff_name}'.format(diff_name=diff_name)
    diff_dict = {}

    if time_diff_dict:
        diff_dict['times'] = time_diff_dict

    if diffs:
        diff_dict['stat'] = diffs

    if diff_dict:
        results.set_attribute(file_path, diff_dict, diff_name, force_create=True)

