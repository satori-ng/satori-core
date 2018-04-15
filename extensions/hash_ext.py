import binascii
import hashlib

from satoricore.hooker import hook

__name__ = 'sha256'

@hook("with_open")
def hash_file(satori_image, file_path, file_type, fd):
    fd.seek(0)
    sha256_obj = hashlib.sha256()

    n_chunk = 1024**2
    bytechunk = fd.read(n_chunk)
    while bytechunk:
        sha256_obj.update(bytechunk)
        bytechunk = fd.read(n_chunk)
    
    hex_digest_256 = sha256_obj.hexdigest()
    satori_image.set_attribute(file_path, hex_digest_256, __name__, force_create=True)
