def prepare_fs(fs):
    #fs = input("Please, wrire a file system for sganography")
    file = open(fs, "rb")
    empty = file.read(1024)
    smth = file.read(10)
    empty.decode("utf-32")
    smth.decode("utf-16")
    print(empty)
    print(smth)
    file.close()

def main():
    number_files = int(input("Kol-vo failov = "))
    massive_filenames = []
    for i in range(number_files):
        massive_filenames.append(input("Please write a new name file for read"))


if __name__ == "__main__":
    prepare_fs('/home/malahov/Documents/Stego/Files/file_with_audio.iso')