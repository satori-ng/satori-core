#!/usr/bin/env python
# Taken from:
#   https://github.com/skorokithakis/python-fuse-sample
#   

from __future__ import with_statement

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations
from satoricore.image import SatoriImage


class ReadOnlyException(Exception):
    """Filesystem loaded in Read-Only mode."""

class Passthrough(Operations):
    def __init__(self, root, satori_image, read_only = True):
        print(root)
        self.root = root
        self.read_only = read_only
        self.satori_image = satori_image

    # Helpers
    # =======

    def _full_path(self, partial):
        partial = partial.lstrip("/")
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        return True        
        # if not os.access(full_path, mode):
        #     raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")        
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):

        full_path = self._full_path(path)
        # st = os.lstat(full_path)
        satori_stat = self.satori_image.get_attribute(full_path, 'stat')
        st = {}
        st_list = ['st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid']
        
        # st[k] = None
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        if self.read_only:
            raise ReadOnlyException("Filesystem loaded in Read-Only mode.")
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True, nonempty=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
