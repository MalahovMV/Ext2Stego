#!/bin/bash
# Копирует флешку побайтово в файл fs.iso.
# Входной параметр - имя "Device"

User=$USER
sudo dd if=$1 of=./fs.iso
sudo chown $User fs.iso
chmod 666 fs.iso
