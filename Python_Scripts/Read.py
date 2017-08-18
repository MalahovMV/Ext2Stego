from Crypto.Cipher import AES
from os import path


def prepare_fs(fs):
    file = open(fs, "rb")
    file.seek(1024)
    smth = file.read(1)
    if smth[0] != 0:
        block_size = 1024

    else:
        file.seek(2048)
        smth = file.read(1)
        if smth[0] != 0:
            block_size = 2048

        else:
            block_size = 4096

    file.close()
    return block_size

def test_marker(text, file_with_marker):
    file_w_m = open(file_with_marker, 'rb')
    marker = file_w_m.read()
    file_w_m.close()
    if text[:len(marker.decode())] == marker:
        print(marker)
        return True

    else:
        return False


def decryption_text(text, file_with_key, key_size):
    file_w_k = open(file_with_key, 'rb')
    key = file_w_k.read(key_size)
    file_w_k.close()
    cypher = AES.new(key)
    return cypher.decrypt(text)

def main (file_where_read, fs):
    file = open(file_where_read, 'wb')
    fs_file = open(fs, "rb")
    block_size = prepare_fs(fs)
    size_fs = path.getsize('/home/malahov/Documents/Stego/Files/file_with_audio_change.iso')
    byte_in_file = 0
    while byte_in_file < size_fs:
        fs_file.seek(byte_in_file)
        text = fs_file.read(block_size)
        key_size = 16
        text = decryption_text(text, '/home/malahov/Documents/Stego/Files/Cipher_Key', key_size)
        if test_marker(text, '/home/malahov/Documents/Stego/Files/Marker'):
            file.write(text[20:])

        byte_in_file += block_size

    file.close()
    fs_file.close()

if __name__ == '__main__':
    main('/home/malahov/Documents/Stego/Files/Read',
         '/home/malahov/Documents/Stego/Files/file_with_audio_change.iso')