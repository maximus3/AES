import os
import time

from m3crypto import encrypt, decrypt

def cls():
    # os.system('clear') # LINUX
    os.system('cls') # WINDOWS

if __name__ == '__main__':
    # WAY

    print('Step 1:')
    while True:
        print('Press:\n1 - encription smth\n2 - decription')
        way = input()
        if way not in ['1', '2']:
            cls()
            print('Action denied')
            continue
        else:
            break
    print()
    cls()

    # TYPE

    print('Step 2:')
    while True:
        print('Press:\n1 - string\n2 - file\n3 - folder (all files in folder)')
        tp = input()
        if tp not in ['1', '2', '3']:
            cls()
            print('Action denied')
            continue
        else:
            break
    print()
    cls()

    # PATH OR STRING

    tp = int(tp)
    s = ['Enter string', 'Enter full name of file', 'Enter full name of folder']

    print('Step 3:')
    while True:
        print(s[tp - 1])

        data = input()
        input_path = None
        if tp > 1:
            input_path = os.path.abspath(data)
            data = ''

            if tp == 1:
                break
            if tp == 2 and os.path.isfile(input_path):
                break
            elif tp == 3 and os.path.isdir(input_path):
                break
            else:
                cls()
                s = ['This is not a text', 'This is not a file', 'This is not a folder']
                print(s[tp - 1])
                continue
    print()
    cls()

    print('Step 4:')
    while True:
        print('Enter your Key for encription/decription. The Key must be less than 16 symbols. Please, don\'t forget it!')
        key = input()
        
        if len(key) > 16:
            print('Too long Key. Imagine another one')
            continue
        
        for symbol in key:
            if ord(symbol) > 0xff:
                print('That key won\'t work. Try another using only latin alphabet and numbers')
                continue
        
        break
    cls()

    if tp == 3:
        print("In working")
        exit(0)

    print('\r\nPlease, wait...')

    time_before = time.time()

    if way == '1':
        data = encrypt(key, data = data, filename = input_path)
    else: # if way == '2'
        data = decrypt(key, data = data, filename = input_path)
            
    time_after = time.time()

    if tp == 0:
        print(str(data))
    if tp == 1:
        print('New file here:', data)
    print(time_after - time_before, ' seconds')
    print('If smth wrong check the key you entered')
    print('Press enter to exit')
    a = input()
