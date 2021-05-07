import csv
import time
from Crypto.Cipher import AES
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import info as session_info


# open the file
# def collect_file():
#        file = file_upload(label = 'Upload your CSV file', accept = '.csv')
#        return file
def open_file(sheet):
    content = open(sheet)
    csv_data = csv.reader(content)
    data_lines = list(csv_data)
    return data_lines


# extracting the rows with military data information
def extracting(y):
    military_satellite = []
    for lines in y[1:1421]:
        if lines[4] == 'Military':
            military_satellite.append(lines)
    return military_satellite


"""AES requires unencrypted message to be multiples of 16, as such, I am adding extra spacing to important
positional data"""


def padding(military_satellite):
    aes_list = []
    for lists in military_satellite[:243]:
        relevant_data = lists[9:16]
        name = lists[0].ljust(16)
        aes_list.append(name)
        for numbers in relevant_data:
            if len(numbers) < 16:
                padding = abs(16 - len(numbers))
                length_added = padding + len(numbers)
                aes_numbers = numbers.ljust(length_added)
                aes_list.append(aes_numbers)
    return aes_list


# encrypter
def encrypter(aes_list):
    ciphertext_list = []
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    f = open("encrypt.txt", "w+")
    for i in range(len(aes_list)):
        message = aes_list[i]
        ciphertext = obj.encrypt(message * 16)
        encrypted_file = f.write("{}\r\n".format(ciphertext))
        ciphertext_list.append(ciphertext)
    
    return encrypted_file, ciphertext_list

    
 # decrypter
def decrypter(ciphertext_list, aes_list):
   
    obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    f = open("decrypted.txt", "w+")
    for i in range(len(ciphertext_list)):
        message = aes_list[i]
        ciphertext = ciphertext_list[i]
        decrypted_text = obj2.decrypt(ciphertext)
        decrypted_text = decrypted_text[0:len(message)]
        dtfile = f.write("{}\r\n".format(decrypted_text))
    return dtfile


def GUI(x, y):

    "Graphical user interface for the Naval Project"
    put_markdown('# ENCRYPTION/DECRYPTION SOFTWARE')

    put_text("""Encryption and Decryption of military software using AES-256 algorithm""")

    put_markdown("""The dataset used for this project is obtined from [kaggle](https://www.kaggle.com/ucsusa/active-satellites)  """)

    put_processbar('bar')
    for i in range(1, 11):
        set_processbar('bar', i / 10)
        time.sleep(0.1)
    
    put_link("Encrypted_text", url = "https://replit.com/@Emeka_/BurlyFunnyParallelport#encrypt.txt")
    put_text("")
    put_link("Decrypted_text", url = "https://replit.com/@Emeka_/decrypt#decrypted.txt")
    
    put_text("")
    put_markdown('The source code for this application can be found [here](https://github.com/emeka-obi/encrypter_decrypter/blob/main/ED.py)')


   
def main():
    x = open_file("Satellite.csv")
    military_satellite1 = extracting(x)
    aes_list = padding(military_satellite1)
    encrypt_txt, csl = encrypter(aes_list)
    decrypt_txt = decrypter(csl, aes_list)
    GUI(encrypt_txt, decrypt_txt)






if __name__ == "__main__":
    main()
