import os
import stat

@pre_open
def get_stat_info(f):
    print(os.stat(f))
