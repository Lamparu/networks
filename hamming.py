# Task:
dlen = 19
src_q = [157, 99, 110, 11, 76, 205, 6, 137, 23, 115, 173, 213, 130, 229, 67, 34, 49, 179, 157, 88, 52, 120, 4, 28, 15,
         84, 51, 17, 226, 147, 195, 128, 98, 64, 39, 180, 3, 124]
# To have a self-check:
src_ans = [169, 12, 24, 30, 124, 230, 85, 251, 1, 211, 156, 197, 129, 224, 64, 229, 136, 0, 30]


def get_bin(num):  # Getting binary from decimal
    b = ''
    while num > 0:
        b = str(num % 2) + b
        num = num // 2
    return '0' * (8 - len(b)) + b


def get_dec(num):  # Getting decimal from binary
    res = 0
    i = 7
    for x in num:
        res += int(x) * 2 ** i
        i -= 1
    return res


def get_ascii(num):  # Getting ASCII of a symbol
    res = ''
    for x in num:
        anum = ord(x)
        res += get_bin(anum)
    return res


def get_pure_word(num):  # Making a list of words to encrypt (without control bits)
    res = []
    i = 0
    while i < len(num):
        j = 0
        strn = ''
        while j < dlen - 5:
            if i >= len(num):
                strn += '0'
            else:
                strn += num[i]
            i += 1
            j += 1
        res.append(strn)
    return res


def get_c1(num):  # Counting 1'st control bit
    c = 0
    for x in num[2::2]:
        c += int(x)
    return str(c % 2)


def get_c(num, i):  # Counting 2,4,8,16 control bits
    c = 0
    save = i
    while i < len(num):
        j = 0
        while j < save + 1 and i < len(num):
            if i != save:
                c += int(num[i])
            i += 1
            j += 1
        i += save + 1
    return str(c % 2)


def get_dlen(num):  # Making a word with control bits
    num = "00" + num[0] + '0' + num[1:4] + '0' + num[4:11] + '0' + num[11:]
    numr = get_c1(num) + get_c(num, 1) + num[2] + get_c(num, 3) + num[4:7] + get_c(num, 7) + num[8:15] \
           + get_c(num, 15) + num[16:]
    return numr


def get_bin_lword(num):  # Making a list of binary numbers with length 8
    i = 0
    bin_lst = []
    while i < len(num):
        j = 0
        strn = ''
        while j < 8:
            if i >= len(num):
                strn += '0'
            else:
                strn += num[i]
            j += 1
            i += 1
        bin_lst.append(strn)
    return bin_lst


def to_dec(num):  # Making a list of decimal numbers
    bin_lst = get_bin_lword(num)
    res_lst = []
    for x in bin_lst:
        res_lst.append(get_dec(x))
    return res_lst


def to_code(num):  # Main function for encryption
    num = str(num)
    bin_num = get_ascii(num)
    bin_lst = get_pure_word(bin_num)
    bin_num = ''
    for x in bin_lst:
        x = get_dlen(x)
        bin_num += x[::-1]
    dec_lst = to_dec(bin_num)
    return dec_lst


def split_q(data):  # Splitting string to a list with the words of given length
    data_lst = []
    i = 0
    while i < len(data):
        num = 0
        strn = ''
        while num < dlen:
            strn = strn + data[i]
            num += 1
            i += 1
        data_lst.append(strn[::-1])
    return data_lst


def get_c_res(data_contr, contr):  # Counting the index of the wrong bit
    x = 0
    res = 0
    while x < len(contr):
        if data_contr[x] != contr[x]:
            res += 2 ** x
        x += 1
    return res - 1


def get_num_index(strs, res):  # Making a string with the right bit (if there was 1 wrong)
    if res > 0:
        if strs[res] == '1':
            i = '0'
        else:
            i = '1'
        return strs[:res] + i + strs[res + 1:]
    return strs


def to_letters(bin_lst):  # Getting encrypted string
    res = ''
    for x in bin_lst:
        result = 0
        for i in range(len(x)):
            result += int(x[i]) * 2 ** (len(x) - i - 1)
        res += chr(result)
    return res


def from_code(src):  # Main function for decryption
    bin_src = []
    for x in src:  # Getting binary representation of decimal numbers in task
        bin_src.append(get_bin(x))
    data = ''
    for x in bin_src:  # Collecting all numbers in 1 string
        data += x
    if len(data) % dlen != 0:  # Adding 0 to the end of string so it has a whole number of words given length
        data = data + '0' * (dlen - len(data) % dlen)
    data_lst = split_q(data)  # Getting a list of word with given length
    count = 0
    result = ''
    while count < len(data_lst):
        #  Counting control bits from word
        data_contr = [int(get_c1(data_lst[count])), int(get_c(data_lst[count], 1)), int(get_c(data_lst[count], 3)),
                      int(get_c(data_lst[count], 7)), int(get_c(data_lst[count], 15))]
        #  Getting control bits from given word
        contr = [int(data_lst[count][0]), int(data_lst[count][1]), int(data_lst[count][3]),
                 int(data_lst[count][7]), int(data_lst[count][15])]
        res = get_c_res(data_contr, contr)  # Counting index of the wrong bit
        data_lst[count] = get_num_index(data_lst[count], res)  # Changing the wrong bit if necessarily
        # Getting rid of control bits
        strn = data_lst[count][2] + data_lst[count][4:7] + data_lst[count][8:15] + data_lst[count][16:]
        result += strn
        count += 1
    bin_lst = get_bin_lword(result)  # Splitting to octets the result string
    return to_letters(bin_lst)  # Getting ASCII symbols from bits


print(from_code(src_q))  # Decryption
print("ANSWER:", 6349624 * 280695)
print(to_code(6349624 * 280695))  # Encryption
print("CHECK:", from_code(src_ans))  # Check
