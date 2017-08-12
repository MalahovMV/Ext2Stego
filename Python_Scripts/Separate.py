from Read import prepare_fs
import os, sys

def main(path_fail, fs):
    file = open(path_fail, 'rb')
    block_size = prepare_fs(fs)
    i = 0
    size = os.path.getsize(path_fail)
    acc = 0
    while acc < size:
        text = file.read(block_size)
        file_w = open('/home/malahov/Documents/Stego/Files/write' + str(i), 'wb')
        file_w.write(text)
        file_w.close()
        acc += block_size
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