#!/bin/bash

# Копирует фаловую систему с застеганографированной информацией (fs_change.iso) на указанный раздел флешки
# Входной параметр - имя "Device"

User=$USER
sudo dd if=./fs_change.iso of=$1
rm fs_change.iso
