import base64
import shutil, os

import qrcode

FILE_NAME = 'q.txt'
# CHUNK_SIZE = 2953
CHUNK_SIZE = 800
OUTPUT_DIR = 'img'

def read_file_chunks(file_name, size):
    l = []
    with open(file_name) as file:
        while True:
            s = file.read(size)
            if not s:
                break
            l.append(base64.b64encode(s.encode('ascii')))
    return l


def read_all_file(file_name):
    with open(file_name) as file:
        s = file.read()
    return base64.b64encode(s.encode('ascii'))


def make_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def file2qr(file_name):
    pass


if __name__ == '__main__':
    try:
        data =read_all_file(FILE_NAME)
        img = make_qr(data)
        l = [data]
    except (SystemError, SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        l = read_file_chunks(FILE_NAME, CHUNK_SIZE)
    if os.path.isdir(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    for i, data in enumerate(l):
        data = base64.b64decode(data).decode('utf-8')
        print(data)
        img = make_qr(data)
        file_name = os.path.join(OUTPUT_DIR, '{}.png'.format(i))
        with open(file_name, 'wb') as file:
            img.save(file, 'png')


