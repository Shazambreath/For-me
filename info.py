import re
import logging
import base64
from os import environ
from struct import pack
from pyrogram.file_id import FileId

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
API_ID = int(environ.get('API_ID', '22546779'))
API_HASH = environ.get('API_HASH', '4f6b00d7d42d8c87d389f77e2f8583ef')
BOT_TOKEN = environ.get('BOT_TOKEN', "6032544530:AAGnxDUqjob-UJNG4wqMI_phMx4mG4AB8EA")
SESSION = environ.get('SESSION', 'Media_search')

# Admin, Channels
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5708316660').split()]
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1001960002947'))
TARGET_CHANNEL = int(environ.get("TARGET_CHANNEL", '-1001894788266'))
FILE_CAPTION = environ.get('FILE_CAPTION', '@casinova65')

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])


def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref





