#!/bin/bash

# В виде параметров последовательно передаются: 
# 1) Образ файловой системы (ext2) или раздел флешки с ext2
# 2) Путь к файлу, который нужно застеганографировать
# 3) Путь к файлу с ключом для шифрования
# 4) Путь к файлу с маркером, который отмечает какие именно блоки принадлежат файлу


# Приходится применять sudo, так как dd без нее не работает
sudo dd if=$1 of=./fs.iso
sudo chmod 666 fs.iso
# Установка виртуального окружения и скачивания библиотеки для шифрования 
pyvenv Stego_Python 
source Stego_Python/bin/activate
pip install --upgrade pip
pip install pycrypto
# Запуск скрипта на запись файла в ФС
python Python_Scripts/Write.py fs.iso $2 $3 $4
# Замена старой файловой системы на скоректированную
sudo dd if=./fs_change.iso of=$1
# Удаление временных файлов
rm writ*
rm -rf Stego_Python
rm fs.iso
rm fs_change.iso
