import random, os

def prepare_fs(fs):
    #fs = input("Please, wrire a file system for sganography")
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

    random.shuffle(empty_blocks)
    return empty_blocks


def main():
    block_size, bitmap = prepare_fs('/home/malahov/Documents/Stego/Files/file_with_audio.iso')
    empty_blocks = find_empty_blocks(block_size, bitmap)
    print(block_size)
    file_for_read = open('/home/malahov/Documents/Stego/Files/write0.txt', 'rb')
    text = file_for_read.read(block_size)
    file_for_read.close()
    file_with_fs = open('/home/malahov/Documents/Stego/Files/file_with_audio.iso', 'rb')
    file_for_write = open('/home/malahov/Documents/Stego/Files/file_with_audio_change.iso', 'wb')
    print(empty_blocks[0])
    now_block = 1
    while (True):
        if now_block == empty_blocks[0]:
            file_for_write.write(text)
            file_with_fs.seek(block_size * now_block)

        else:
            file_for_write.write(file_with_fs.read(1024))

        now_block += 1
        if (now_block * block_size) > os.path.getsize('/home/malahov/Documents/Stego/Files/file_with_audio.iso'):
            break

    file_for_write.close()
    file_with_fs.close()


if __name__ == "__main__":
    main()