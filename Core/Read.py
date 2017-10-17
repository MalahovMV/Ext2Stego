# -*-coding: utf-8 -*-
"""
Stego
Read
Todo

Create by MalahovMV on 02.10.2017 20:27
"""
# TODO написать описание в __doc__
import datetime
from Universal_Function import create_marker, prepare_fs
from os import path
from Crypto.Cipher import AES
import sys

__author__ = 'MalahovMV'


def calc_all_markers(file_with_marker, key, marker_size):
    """
    Вычисление маркеров для каждого блока в исходном файле
    :param file_with_marker: Файл с маркером
    :param key: Файл с ключом, которым шифровался исходный файл
    :param marker_size:
    :return: Возвращает список маркеров
    """
    marker_str = create_marker(file_with_marker, key, marker_size)
    marker_list = []
    while marker_str:
        marker_list.append(marker_str[:marker_size])
        marker_str = marker_str[marker_size:]

    return marker_list


def test_marker(text,  marker_list, marker_size):
    # Проверяется находится ли маркер в начале данного блока информации
    if text[:marker_size] in marker_list:
        return True, marker_list.index(text[:marker_size])

    else:
        return False, False


def recovery_on_file(piece_of_file, output_file):
    """
    Востанавливает исходный файл из блоков
    :param piece_of_file: Словарь, где ключом является номер блока в исходном файле, а значением сам блок
    :param output_file: Файл, куда будет записан получившийся файл
    :return: 
    """
    with open(output_file, 'wb') as file:
        i = 0
        while i in piece_of_file:
            file.write(piece_of_file[i])
            i += 1


def main(fs, file_with_key, file_with_marker):
    # Размер ключа шифрования
    key_size = 128 / 8

    # Словарь, где ключом является номер блока в исходном файле, а значением сам блок
    piece_of_file = {}

    # Чтение ключа
    with open(file_with_key, 'rb') as file_w_k:
        key = file_w_k.read(key_size)

    marker_size = 16
    marker_list = calc_all_markers(file_with_marker, key, marker_size)

    with open(fs, "rb") as fs_file:
        # Определение размера блока ФС
        block_size = prepare_fs(fs)[0]

        # Размер ФС
        size_fs = path.getsize(fs)

        # Счетчик обработанных байтов на данный момент
        current_byte = 0

        # Чтение информации из ФС
        while current_byte < size_fs:
            fs_file.seek(current_byte)
            text = fs_file.read(block_size)
            # Проверка на принадлежность блока застеганографированному файлу
            bool, ind = test_marker(text, marker_list, marker_size)
            if bool:
                # Расшифровка файла
                cypher = AES.new(key)
                text = cypher.decrypt(text)

                # Запись полученного блока с указанием его номера в искомом файле
                piece_of_file[ind] = text[marker_size:]

            current_byte += block_size
            continue

    # Сборка блоков в один выходной файл
    recovery_on_file(piece_of_file, 'Read')

if __name__ == '__main__':
    print(u'Run Read.py {0}'.format(datetime.datetime.now()))
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
    except Exception as e:
        print('Неверно введены параметры')

    main(arg1, arg2, arg3)