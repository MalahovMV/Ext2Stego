#В данном файле представлены функции, которые используются и при чтении и при записи в ФС

from Crypto.Cipher import AES

def prepare_fs(fs):
    """
    Функция предназначена для выяснения размеров блоков в файловой системе и нахождения битовой карты
    :param fs:  Передается образ файловой системы
    :return: Возвращается размер блока и битовая карта
    """
    file = open(fs, "rb")
    file.seek(1024)
    #Для вычисления размера блока используется тот факт, что в ext2 первый блок всегда пустой,
    #а второй блок всегда ничнается с ненулевого бита
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

    #Битовая карта находится в 7-ом блоке с начала ФС
    file.seek(6 * block_size)
    bit_map = file.read(block_size)
    file.close()
    return block_size, bit_map


def create_marker(file_with_marker, key, marker_size, lot_blocks=1000):
    """
    Функция создает маркеры для каждого блока файла, по которым эти блоки потом можно будет опознать
    :param file_with_marker: Файл, откуда берется сам маркер 
    :param key: Файл, откуда берется ключ для шифрования
    :param lot_blocks: Количество блоков, на которые был разбит файл (максимальное значение=1000) 
    :return: Возвращает строку, представляющую из себя индивидуальный маркер для каждого блока
    """
    file = open(file_with_marker, 'r')
    resul = ''
    marker = file.read(marker_size - 4)
    #Добавление в конец маркера номера блока, которому соответсвует данный маркер
    for i in range(lot_blocks):
        number_block = str(i)
        while len(number_block) < 4:
            number_block = '0' + number_block

        resul += marker + number_block

    cipher = AES.new(key)
    resul = cipher.encrypt(resul)
    file.close()
    return resul