import os

from hooker import hook


@hook("imager.pre_open")
def get_statfs_info(satori_image, file_path, file_type):
    # pass
    if os.path.islink(file_path):
        return
    file_stat = os.statvfs(file_path)

    # Translates statvfs' attributes to a dict
    stat_dict = {x[2:]:
        getattr(file_stat, x)
        for x in dir(file_stat)
        if x.startswith("f_")
        }

    satori_image.set_attribute(file_path, stat_dict, 'statfs', force_create=True)
