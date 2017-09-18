from Universal_Function import create_marker, prepare_fs
from os import path
from Crypto.Cipher import AES
import sys


def calc_all_markers(file_with_marker, key, marker_size):
    """
    Вычисление маркеров для каждого блока в исходном файле
    :param file_with_marker: Файл с маркером
    :param key: Файл с ключом, которым шифровался исходный файл
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
        return (True, marker_list.index(text[:marker_size]))

    else:
        return (False, False)


def recovery_on_file(piece_of_file, file_where_write):
    """
    Востанавливает исходный файл из блоков
    :param piece_of_file: Словарь, где ключом является номер блока в исходном файле, а значением сам блок
    :param file_where_write: Файл, куда будет записан получившийся файл
    :return: 
    """
    file = open(file_where_write, 'wb')
    i = 0
    while i in piece_of_file:
        file.write(piece_of_file[i])
        i += 1

    file.close()

def main (fs, file_with_key, file_with_marker):
    key_size = 16 # Размер ключа шифрования
    piece_of_file = {} # Словарь, где ключом является номер блока в исходном файле, а значением сам блок
    file_w_k = open(file_with_key, 'rb')
    key = file_w_k.read(key_size)
    file_w_k.close()
    marker_size = 16
    marker_list = calc_all_markers(file_with_marker, key, marker_size)
    fs_file = open(fs, "rb")
    block_size = prepare_fs(fs)[0] #Определение размера блока ФС
    size_fs = path.getsize(fs) #Размер ФС
    byte_in_file = 0
    while byte_in_file < size_fs:
        fs_file.seek(byte_in_file)
        text = fs_file.read(block_size)
        bool, ind = test_marker(text, marker_list, marker_size) #Проверка на принадлежность блока застеганографированному файлу
        if bool:
            cypher = AES.new(key)
            text = cypher.decrypt(text)
            piece_of_file[ind] = text[marker_size:]

        byte_in_file += block_size

    fs_file.close()
    recovery_on_file(piece_of_file, 'Read')

if __name__ == '__main__':
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]

    except:
        print('Неверно введены параметры')

    main(arg1, arg2, arg3)