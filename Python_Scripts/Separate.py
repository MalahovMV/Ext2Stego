from Crypto.Cipher import AES
from Read import prepare_fs
import os, sys


def cipher_text(text, number_block, file_with_key, key_size, file_with_marker):
    file = open(file_with_marker, 'rb')
    marker = file.read(key_size)
    file.close()
    number_block = str(number_block)
    while len(number_block) < 4:
        number_block = '0' + number_block

    if len(number_block) != 4:
        raise Exception('Колчество блоков, на которые был разбит файл, не подлежит обработке')

    text = marker +  number_block.encode('ASCII') + text
    while len(text) % key_size != 0:
        text += b'0'

    file = open(file_with_key, 'rb')
    key = file.read(key_size)
    file.close()
    cipher = AES.new(key)
    inf = cipher.encrypt(text)
    return inf

def main(path_fail, fs):
    file = open(path_fail, 'rb')
    block_size = prepare_fs(fs)
    i = 0
    size = os.path.getsize(path_fail)
    acc = 0
    while acc < size:
        key_size = 16
        inf = file.read(block_size - key_size - 4)
        text = cipher_text(inf, i, '/home/malahov/Documents/Stego/Files/Cipher_Key',
                           key_size, '/home/malahov/Documents/Stego/Files/Marker')
        file_w = open('/home/malahov/Documents/Stego/Files/write' + str(i), 'wb')
        file_w.write(text)
        file_w.close()
        acc += block_size - key_size - 4
        i += 1

    file.close()
    print('Файл был разбит на ', i, ' файлов(а)')

if __name__ == '__main__':
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]

    except:
        print('Неверно введены параметры')

    main(arg1, arg2)
