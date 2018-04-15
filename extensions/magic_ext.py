import binascii
import magic

from satoricore.hooker import hook

__name__ = 'mime'


@hook("with_open")
def hash_file(satori_image, file_path, file_type, fd):
    fd.seek(0)
    magic_obj = magic.Magic(flags=magic.MAGIC_MIME_TYPE)
    chunk = fd.read(1024)
    mime = magic_obj.id_buffer(chunk)
    satori_image.set_attribute(file_path, mime, __name__, force_create=True)
