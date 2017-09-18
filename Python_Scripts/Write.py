#Скрипт, реализующий запись файла в ФС

from Universal_Function import create_marker, prepare_fs
import os, sys, random
from Crypto.Cipher import AES
import time

def separate(fs, path_fail, file_with_key, file_with_marker):
    """
    Функция разбивает исходный файл на блоки, маркерует каждый блок, и пишет их в отдельные файлы
    :param fs: Файловая система, в которую планируется записывать файл
    :param path_fail: Путь к файлу, который нужно застеганографировать
    :param file_with_key: Файл с ключом шифрования
    :param file_with_marker: Файл с маркером
    :return: Возвращает количество блоков, на которые был разбит файл
    """
    key_size = 16 # Задается длина ключа
    marker_size = 16 # Задается длина маркера
    file = open(file_with_key, 'rb')
    key = file.read(key_size)
    file.close()
    file = open(path_fail, 'rb')
    block_size, bitmap = prepare_fs(fs) # Вызов функции, определяющей размер блока в ФС и возвращающей битовую карту
    size = os.path.getsize(path_fail) # Определение размера стегонаграфируемого файла
    acc = 0 # Переменная, определяет сколько байтов из исходного файла уже обработано
    number_block = 0 # Переменная, определяет номер следующего обрабатываемого блока
    marker_lot = create_marker(file_with_marker, key, marker_size, (size//block_size + 1)) # Получение из функции всех необходимых маркеров для каждого блока
    while acc < size:
        inf = file.read(block_size - marker_size)
        while len(inf) < (block_size - marker_size): #Последний блок дозаполняем нулевыми байтами до конца
            inf += b'0'

        cipher = AES.new(key)
        inf = marker_lot[number_block * marker_size : (number_block + 1) * marker_size]+ cipher.encrypt(inf)
        file_w = open('write' + str(number_block), 'wb')
        file_w.write(inf)
        file_w.close()
        acc += block_size - marker_size
        number_block += 1

    file.close()
    return number_block


def find_empty_blocks(bitmap, last_block):
    """
    Из битовой карты достаются номера пустых блоков
    :param bitmap: Битовая карта
    :return: Возвращается список пустых блоков, расположенных в случайном порядке
    """
    exp_binary = [128, 64, 32, 16, 8, 4, 2, 1]
    empty_blocks = []
    blocks_now = 1
    #Каждый считанный байт переводится в 8 бит
    for el in bitmap:
        if el != 255:
            for i in range(len(exp_binary)):
                if (el - exp_binary[i]) >= 0:
                    el -= exp_binary[i]

                else:
                    empty_blocks.append(blocks_now)

                blocks_now += 1

        else:
            blocks_now += 8

        if blocks_now >= last_block:
            break

    random.shuffle(empty_blocks)
    return empty_blocks


def main(fs, enter_file, file_with_key, file_with_marker):
    """
    
    :param fs: Файловая система
    :param enter_file: Файл, который должен быть застеганографирован
    :param file_with_key: Файл с ключом шифрования
    :param file_with_marker: Файл с маркером
    :return: 
    """
    number_read_files = separate(fs, enter_file, file_with_key, file_with_marker) #Разбивка файла на блоки с доьавлением маркера и шифрованием
    block_size, bitmap = prepare_fs(fs) #Определение свойств файловой системы
    empty_blocks = find_empty_blocks(bitmap, (os.path.getsize(fs) // block_size))[:number_read_files] #Возвращает номера пустых блоков в количестве, необходимом для записи файла
    sorted(empty_blocks) #Сортируем пустые блоки, так как ищз-за особенностей алгоритма, сначала информация должна быть записана в более ранние блоки
    text = [] #Все блоки,на которые был разбит исходный файл, переносятся в список
    for i in range(number_read_files):
        file_for_read = open('write' + str(i), 'rb')
        text.append(file_for_read.read(block_size))
        file_for_read.close()

    random.shuffle(text) #Происходит перемещивание порядка блоков исходного файла
    file_with_fs = open(fs, 'rb')
    file_for_write = open(fs[:-4] + '_change.iso', 'wb') #Новая ФС
    number_write_now = 0
    now_block = 1 #Номер обрабатываемого блока в ФС
    while (now_block * block_size) < os.path.getsize(fs):
        if (now_block in empty_blocks) :
            file_for_write.write(text[number_write_now])
            file_with_fs.seek(block_size * now_block)
            number_write_now += 1

        else:
            file_for_write.write(file_with_fs.read(1024))

        now_block += 1

    file_for_write.close()
    file_with_fs.close()


if __name__ == '__main__':
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        arg4 = sys.argv[4]

    except:
        print('Неверно введены параметры')

    main(arg1, arg2, arg3, arg4)