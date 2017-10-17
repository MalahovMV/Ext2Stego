# -*-coding: utf-8 -*-
"""
Stego
Write
Todo

Create by MalahovMV on 02.10.2017 20:27
"""
# TODO написать описание в __doc__
import datetime
import os
import sys
import random
from Crypto.Cipher import AES

from Universal_Function import create_marker, prepare_fs

__author__ = 'MalahovMV'


def separate(fs, path_fail, file_with_key, file_with_marker):
    """
    Функция разбивает исходный файл на блоки, маркерует каждый блок, и пишет их в отдельные файлы
    :param fs: Файловая система, в которую планируется записывать файл
    :param path_fail: Путь к файлу, который нужно застеганографировать
    :param file_with_key: Файл с ключом шифрования
    :param file_with_marker: Файл с маркером
    :return: Возвращает количество блоков, на которые был разбит файл
    """
    # Длина ключа
    key_size = 128 / 8

    # Длина маркера
    marker_size = 16
    with open(file_with_key, 'rb') as file:
        key = file.read(key_size)

    # Определяется размер блока в ФС и битовая карта
    block_size, bitmap = prepare_fs(fs)

    # Размер стегонаграфируемого файла
    size = os.path.getsize(path_fail)

    # Счетчик обработанных байтов из исходного файла
    acc = 0

    # Номер следующего обрабатываемого блока
    number_block = 0

    # Получение маркеров для всех блоков
    marker_lot = create_marker(
        file_with_marker,
        key,
        marker_size,
        (size // block_size + 1),
    )
    with open(path_fail, 'rb') as file:
        while acc < size:
            inf = file.read(block_size - marker_size)
            # Последний блок заполняется нулями до конца
            while len(inf) < (block_size - marker_size):
                inf += b'0'

            # Шифрование информации
            cipher = AES.new(key)

            from_ = number_block * marker_size
            to_ = (number_block + 1) * marker_size
            inf = marker_lot[from_:to_] + cipher.encrypt(inf)

            with open('write' + str(number_block), 'wb') as file_w:
                file_w.write(inf)

            # Подсчет числа обработанных байтов
            acc += block_size - marker_size
            number_block += 1

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
    # Каждый считанный байт переводится в 8 бит
    for el in bitmap:
        if el != 255:
            for i in range(len(exp_binary)):
                if (el - exp_binary[i]) >= 0:
                    el -= exp_binary[i]

                else:
                    empty_blocks.append(blocks_now)

                blocks_now += 1
                continue

        else:
            blocks_now += 8

        if blocks_now >= last_block:
            break
        continue

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
    # Разбиение файла на блоки с добавлением маркера и шифрованием
    number_read_files = separate(fs, enter_file, file_with_key,
                                 file_with_marker)
    # Определение свойств файловой системы
    block_size, bitmap = prepare_fs(fs)
    # Возвращает номера пустых блоков в количестве, необходимом для записи файла
    empty_blocks = find_empty_blocks(bitmap, (os.path.getsize(fs) // block_size))[
                   :number_read_files]
    # Сортировка первых случайных N (необходимых для записи) пустых блоков
    sorted(empty_blocks)
    # Все блоки,на которые был разбит исходный файл, переносятся в список
    text = []
    for i in range(number_read_files):
        with open('write' + str(i), 'rb') as file_for_read:
            text.append(file_for_read.read(block_size))

    # Перемещивание порядка блоков исходного файла
    random.shuffle(text)

    with open(fs, 'rb') as file_old_fs:
        # Новая ФС
        with open(fs[:-4] + '_change.iso', 'wb') as file_new_fs:
            number_write_now = 0
            # Номер обрабатываемого блока в ФС
            now_block = 1
            # Запись в файловую систему
            while (now_block * block_size) < os.path.getsize(fs):
                if now_block in empty_blocks:
                    file_new_fs.write(text[number_write_now])
                    file_old_fs.seek(block_size * now_block)
                    number_write_now += 1

                else:
                    file_new_fs.write(file_old_fs.read(1024))

                now_block += 1


if __name__ == '__main__':
    print(u'Run Write.py {0}'.format(datetime.datetime.now()))
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        arg4 = sys.argv[4]
    except:
        print('Неверно введены параметры')

    main(arg1, arg2, arg3, arg4)