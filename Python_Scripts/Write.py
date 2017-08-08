import random, os, sys

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

    file.seek(6 * block_size)
    bit_map = file.read(block_size)
    file.close()
    return block_size, bit_map


def find_empty_blocks(block_size, bitmap):
    exp_binary = [128, 64, 32, 16, 8, 4, 2, 1]
    empty_blocks = []
    blocks_now = 1
    for el in bitmap:
        if el != 255:
            for i in range(len(exp_binary)):
                if (el - exp_binary[i]) > 0:
                    el -= exp_binary[i]

                else:
                    empty_blocks.append(blocks_now)

                blocks_now += 1

        else:
            blocks_now += 8

    #random.shuffle(empty_blocks)
    return empty_blocks


def main(fs, dir_from_read, number_read_files):
    block_size, bitmap = prepare_fs(fs)
    empty_blocks = find_empty_blocks(block_size, bitmap)
    file_with_blocks = open('/home/malahov/Documents/Stego/Files/file_with_blocks', 'w')
    print(block_size)
    text = []
    for i in range(number_read_files):
        file_for_read = open(dir_from_read + str(i) + '.txt', 'rb')
        text.append(file_for_read.read(block_size))
        file_for_read.close()

    print(len(text))
    file_with_fs = open(fs, 'rb')
    file_for_write = open(fs[:-4] + '_change' + '.iso', 'wb')
    number_write_now = 0
    now_block = 1
    while (True):
        if (now_block in empty_blocks) and (number_write_now < len(text)):
            file_for_write.write(text[number_write_now])
            file_with_fs.seek(block_size * now_block)
            file_with_blocks.write(str(now_block - 1) + ',')
            number_write_now += 1

        else:
            file_for_write.write(file_with_fs.read(1024))

        now_block += 1
        if (now_block * block_size) > os.path.getsize(fs):
            break


    file_for_write.close()
    file_with_fs.close()


if __name__ == "__main__":
    try:
        fs = sys.argv[1]
        dir_from_read = sys.argv[2]
        number_files = int(sys.argv[3])

    except:
        print('Неправильно заданы аргументы командной строки')

    main(fs, dir_from_read, number_files)