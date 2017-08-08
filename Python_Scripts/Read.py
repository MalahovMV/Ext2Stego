def get_blocks(file_with_blocks):
    file = open(file_with_blocks, 'r')
    text = file.readline()[:-1]
    block_list = text.split(',')
    return block_list

def prepare_fs(fs):
    file = open(fs, "rb")
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


def main (file_where_read, fs):
    block_massiv = get_blocks('/home/malahov/Documents/Stego/Files/file_with_blocks')
    file = open(file_where_read, 'w')
    fs_file = open(fs, "rb")
    block_size = prepare_fs(fs)
    for block in block_massiv:
        fs_file.seek(block_size * int(block))
        text = fs_file.read(block_size)
        file.write(text)

    file.close()
    fs_file.close()

if __name__ == '__main__':
    main('/home/malahov/Documents/Stego/Files/Read.txt',
         '/home/malahov/Documents/Stego/Files/file_with_audio_change.iso')