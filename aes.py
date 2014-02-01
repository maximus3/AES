nb = 4  # number of coloumn of State (for AES = 4)
nr = 10 # number of rounds ib ciper cycle (if nb = 4 nr = 10)
nk = 4

# This dict will be used in SubBytes(). 
hex_symbols_to_int = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e':14, 'f':15}

sbox = [ 
        '0x63', '0x7c', '0x77', '0x7b', '0xf2', '0x6b', '0x6f', '0xc5', '0x30', '0x01', '0x67', '0x2b', '0xfe', '0xd7', '0xab', '0x76', 
        '0xca', '0x82', '0xc9', '0x7d', '0xfa', '0x59', '0x47', '0xf0', '0xad', '0xd4', '0xa2', '0xaf', '0x9c', '0xa4', '0x72', '0xc0', 
        '0xb7', '0xfd', '0x93', '0x26', '0x36', '0x3f', '0xf7', '0xcc', '0x34', '0xa5', '0xe5', '0xf1', '0x71', '0xd8', '0x31', '0x15', 
        '0x04', '0xc7', '0x23', '0xc3', '0x18', '0x96', '0x05', '0x9a', '0x07', '0x12', '0x80', '0xe2', '0xeb', '0x27', '0xb2', '0x75', 
        '0x09', '0x83', '0x2c', '0x1a', '0x1b', '0x6e', '0x5a', '0xa0', '0x52', '0x3b', '0xd6', '0xb3', '0x29', '0xe3', '0x2f', '0x84', 
        '0x53', '0xd1', '0x00', '0xed', '0x20', '0xfc', '0xb1', '0x5b', '0x6a', '0xcb', '0xbe', '0x39', '0x4a', '0x4c', '0x58', '0xcf', 
        '0xd0', '0xef', '0xaa', '0xfb', '0x43', '0x4d', '0x33', '0x85', '0x45', '0xf9', '0x02', '0x7f', '0x50', '0x3c', '0x9f', '0xa8', 
        '0x51', '0xa3', '0x40', '0x8f', '0x92', '0x9d', '0x38', '0xf5', '0xbc', '0xb6', '0xda', '0x21', '0x10', '0xff', '0xf3', '0xd2', 
        '0xcd', '0x0c', '0x13', '0xec', '0x5f', '0x97', '0x44', '0x17', '0xc4', '0xa7', '0x7e', '0x3d', '0x64', '0x5d', '0x19', '0x73', 
        '0x60', '0x81', '0x4f', '0xdc', '0x22', '0x2a', '0x90', '0x88', '0x46', '0xee', '0xb8', '0x14', '0xde', '0x5e', '0x0b', '0xdb', 
        '0xe0', '0x32', '0x3a', '0x0a', '0x49', '0x06', '0x24', '0x5c', '0xc2', '0xd3', '0xac', '0x62', '0x91', '0x95', '0xe4', '0x79', 
        '0xe7', '0xc8', '0x37', '0x6d', '0x8d', '0xd5', '0x4e', '0xa9', '0x6c', '0x56', '0xf4', '0xea', '0x65', '0x7a', '0xae', '0x08', 
        '0xba', '0x78', '0x25', '0x2e', '0x1c', '0xa6', '0xb4', '0xc6', '0xe8', '0xdd', '0x74', '0x1f', '0x4b', '0xbd', '0x8b', '0x8a', 
        '0x70', '0x3e', '0xb5', '0x66', '0x48', '0x03', '0xf6', '0x0e', '0x61', '0x35', '0x57', '0xb9', '0x86', '0xc1', '0x1d', '0x9e', 
        '0xe1', '0xf8', '0x98', '0x11', '0x69', '0xd9', '0x8e', '0x94', '0x9b', '0x1e', '0x87', '0xe9', '0xce', '0x55', '0x28', '0xdf', 
        '0x8c', '0xa1', '0x89', '0x0d', '0xbf', '0xe6', '0x42', '0x68', '0x41', '0x99', '0x2d', '0x0f', '0xb0', '0x54', '0xbb', '0x16'
        ]

rcon = [['0x01', '0x02', '0x04', '0x08', '0x10', '0x20', '0x40', '0x80', '0x1b', '0x36'],
        ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'],
        ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'],
        ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00']
       ]

def encrypt(message, key):
    """Function encrypts the message according to AES(128) algorithm using the key

    Returns:
        List of hexidecimal numbers. They are ASCII codes.

    """

    # let's prepare our enter data: State array and KeySchedule
    # if len of the message less than 16, full gaps with '0x00'
    state = [[] for j in range(nb)] 
    hex_symbols = [hex(ord(symbol)) for symbol in message]

    if len(hex_symbols) < 16:
        for i in range(16 - len(hex_symbols)):
            hex_symbols.append('0x00')

    '''
    hex_symbols = ['0x32', '0x43', '0xf6', '0xa8', '0x88', '0x5a', '0x30',
                   '0x8d', '0x31', '0x31', '0x98', '0xa2', '0xe0', '0x37',
                   '0x07', '0x34']
    '''

    for r in range(4):
        for c in range(nb):
            state[r].append(hex_symbols[r + 4*c])

    key_schedule = key_expansion(key)
    
    state = add_round_key(state, key_schedule)
    state = kill_chaos_in(state)

    print('iteration 0:')
    for i in range(len(state)):
        print(state[i])

    for rnd in range(1, nr):
        print('iteration ', rnd)

        state = sub_bytes(state, sbox)
        print('after SubBytes:')
        for i in range(len(state)):
            print(state[i])

        state = shift_rows(state)
        print('after ShiftRows:')
        for i in range(len(state)):
            print(state[i])

        state = mix_columns(state)
        print('after MixColumns:')
        for i in range(len(state)):
            print(state[i])

        state = add_round_key(state, key_schedule, rnd)
        print('after AddRoundKey:')
        for i in range(len(state)):
             print(state[i])

        state = kill_chaos_in(state)

    print('iteration last:')
    state = sub_bytes(state, sbox)
    print('after SubBytes:')
    for i in range(len(state)):
        print(state[i])
    
    state = shift_rows(state)
    print('after ShiftRows:')
    for i in range(len(state)):
        print(state[i])

    state = add_round_key(state, key_schedule, rnd + 1)
    print('after AddRoundKey:')
    for i in range(len(state)):
         print(state[i])

    print('result!')
    for i in range(len(state)):
        print(state[i])

    # Make a normal string from State
    output = [None for i in range(nb*nb)]
    for r in range(4):
        for c in range(nb):
            output[r + 4*c] = hex(eval(state[r][c]))

    # If message is less than 16 symbols, gaps is fulled with '0x00' and we shouldn't see them
    return output[:len(message)]


def sub_bytes(state, sbox):
    """That transformation replace every element from State on element from Sbox
    according the algorithm: in hexadecimal notation an element from State 
    consist of two values: 0x<val1><val2>. We take elem from crossing 
    val1-row and val2-column in Sbox and put it instead of the element in State

    """

    for i in range(len(state)):
        for j in range(len(state[i])):
            
            pre_row = state[i][j][-2]
            pre_col = state[i][j][-1]
            row = pre_row if pre_row.isdigit() else hex_symbols_to_int[pre_row]
            col = pre_col if pre_col.isdigit() else hex_symbols_to_int[pre_col]
            
            # Our Sbox is a flat array, not a bable. So, we use this trich to find elem:
            # And DO NOT change list sbox! if you want it to work
            sbox_elem =  sbox[16*int(row) + int(col)]
            state[i][j] = sbox_elem

    return state


def shift_rows(state):
    """That transformation shift rows of State: the second rotate over 1 bytes,
    the third rotate over 2 bytes, the fourtg rotate over 3 bytes. The transformation doesn't
    touch the first row

    """

    count = 1
    for i in range(1, 4):
        state[i] =  left_shift(state[i], count)
        count += 1

    return state


def mix_columns(state):
    """That transformation multiplyes every column of State with 
    a fixed polinomial a(x) = {03}x**3 + {01}x**2 + {01}x + {02} in Galua field. 
    Detailed information in AES standart

    """

    for i in range(nb):

        s0 = mul_by_02(eval(state[0][i]))^mul_by_03(eval(state[1][i]))^eval(state[2][i])^eval(state[3][i])
        s1 = eval(state[0][i])^mul_by_02(eval(state[1][i]))^mul_by_03(eval(state[2][i]))^eval(state[3][i])
        s2 = eval(state[0][i])^eval(state[1][i])^mul_by_02(eval(state[2][i]))^mul_by_03(eval(state[3][i]))
        s3 = mul_by_03(eval(state[0][i]))^eval(state[1][i])^eval(state[2][i])^mul_by_02(eval(state[3][i]))


        state[0][i] = hex(s0)
        state[1][i] = hex(s1)
        state[2][i] = hex(s2)
        state[3][i] = hex(s3)
 
    return state

# Small helpful functions block

def left_shift(array, count):
    """Rotate the array over count times"""

    res = array[:]
    for i in range(count):
        temp = [res[i] for i in range(1, len(array))]
        temp.append(res[0])
        res[:] = temp[:]

    return(res)

def kill_chaos_in(array):

    array = array[:]

    for row in range(len(array)):
        for col in range(len(array[row])):
            if array[row][col][-2] == 'x':
                array[row][col] = array[row][col][:-1] + '0' + array[row][col][-1]

    return array

def mul_by_02(num):
    """The function multiplies by 2 in Galua space"""

    if num < 0x80:
        return (num << 1)
    else:
        return (num << 1)^0x1b

def mul_by_03(num):
    """The function multiplies by 3 in Galua space
    example: 0x03*num = (0x02 + 0x01)num = num*0x02 + num
    Addition in Galua field is oparetion XOR

    """

    return (mul_by_02(num)^num)

# End of small helpful functions block

def key_expansion(key):
    """It makes list of RoundKeys for function AddRoundKey. All details 
    about algorithm is is in AES standart

    """

    key_symbols = [hex(ord(symbol)) for symbol in key]

    # ChipherKey shoul contain 16 symbols to full 4*4 table. If it's less
    # complement key with "0x0"
    if len(key_symbols) < 16:
        for i in range(16 - len(key_symbols)):
            key_symbols.append('0x00')

    # make ChipherKey(which is base of KeySchedule)
    key_schedule = [[], [], [], []]     
    for r in range(4):
        for c in range(nb):
            key_schedule[r].append(key_symbols[r + 4*c])

    '''
    key_schedule = [['0x2b', '0x28', '0xab', '0x09'],
                    ['0x7e', '0xae', '0xf7', '0xcf'],
                    ['0x15', '0xd2', '0x15', '0x4f'],
                    ['0x16', '0xa6', '0x88', '0x3c']]
    '''

    # Comtinue to fill KeySchedule
    for col in range(nb, nb*(nr + 1)): # col - column number
        if col % nk == 0:
            # take shifted (col - 1)th column...
            tmp = [key_schedule[row][col-1] for row in range(1, nb)]
            tmp.append(key_schedule[0][col-1])

            # change its elements using Sbox-table like in SubBytes...
            for j in range(len(tmp)):        
                pre_row = tmp[j][-2]
                pre_col = tmp[j][-1]
                true_row = pre_row if pre_row.isdigit() else hex_symbols_to_int[pre_row]
                true_col = pre_col if pre_col.isdigit() else hex_symbols_to_int[pre_col]
                
                sbox_elem =  sbox[16*int(true_row) + int(true_col)]
                tmp[j] = sbox_elem

            # and finally make XOR of 3 columns
            for i in range(nk):
                s = eval(key_schedule[i][col - 4])^eval(tmp[i])^eval(rcon[i][int(col/nk - 1)])
                
                key_schedule[i].append(hex(s))

            key_schedule = kill_chaos_in(key_schedule)
        else:
            # just make XOR of 2 columns
            for i in range(nk):
                s = eval(key_schedule[i][col - 4])^eval(key_schedule[i][col - 1])
                key_schedule[i].append(hex(s))
            
            key_schedule = kill_chaos_in(key_schedule)

    return key_schedule

def add_round_key(state, key_schedule, round=0):
    """That transformation combines State and KeySchedule together. Xor 
    of State and RoundSchedule(part of KeySchedule).

    """
    
    for col in range(nk):
        # nk*round is a shift which indicates start of a part of the KeySchedule
        s0 = eval(state[0][col])^eval(key_schedule[0][nk*round + col])
        s1 = eval(state[1][col])^eval(key_schedule[1][nk*round + col])
        s2 = eval(state[2][col])^eval(key_schedule[2][nk*round + col])
        s3 = eval(state[3][col])^eval(key_schedule[3][nk*round + col])

        state[0][col] = hex(s0)
        state[1][col] = hex(s1)
        state[2][col] = hex(s2)
        state[3][col] = hex(s3)

    return state

if __name__ == '__main__':
    
    message = 'ABCD'
    key = 'banana'
    cipher = encrypt(message, key)
    print('111 ', cipher)