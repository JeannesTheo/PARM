# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os.path
import sys
from tkinter import filedialog, Tk


def bTen_bTwo(n, size = 0):
    str = "{0:b}".format(int(n))
    return '0'*(size-len(str)) + str

def signed_2_complement(n, size = 32):
    if(n >= 0):
        return bTen_bTwo(n,size)
    return str(bin(n & (2 ** size -1)))[2:]

def bTwo_bHex(str):
    return '%.*x' % (4, int('0b' + str, 0))

def getConditionValue(str):
    if(str == "eq"):
        return 0
    elif(str == "ne"):
        return 1
    elif(str == "cs" or str == "hs"):
        return 2
    elif(str == "cc" or str == "lo"):
        return 3
    elif(str == "mi"):
        return 4
    elif(str == "pl"):
        return 5
    elif(str == "vs"):
        return 6
    elif(str == "vc"):
        return 7
    elif(str == "hi"):
        return 8
    elif(str == "ls"):
        return 9
    elif(str == "ge"):
        return 10
    elif(str == "lt"):
        return 11
    elif(str == "gt"):
        return 12
    elif(str == "le"):
        return 13
    elif(str == "al"):
        return 14
    else:
        return 15


def print_hi():

    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)

    file_path = filedialog.askopenfilename(parent=root, title="Python Parser - Select File to Parse", filetypes=[("S File", ".s")])
    output_path, ignore = os.path.splitext(file_path)
    output_path += "-M.bin"

    dictionary = {}

    with open(file_path) as f:
        i = 0
        lines = f.readlines()
        for word in lines:
            word = word.lower().replace(',', '').replace('\n', '')
            if word and word[0] != "@":
                if(word[0] == "."):
                    dictionary[word[:-1]] = i
                else:
                    i += 1
        f.seek(0)

        with open(output_path, "w") as output:
            output.write("v2.0 raw\n")
            lines = f.readlines()
            i = -1
            for word in lines:
                word = word.lower()
                word = word.replace(',', '').replace('\n', '')
                if word and word[0] != "@" and word != "\n":
                    i += 1
                    if(word[0] == "."):
                        i -= 1
                        continue
                    b = "error"
                    word = word.split(" ")
                    word[0] = word[0][:3]
                    print(word[0])
                    if(word[0] == "lsl"):
                        if len(word) == 4:
                            b = "00000" + bTen_bTwo(word[3][1:],5) + bTen_bTwo(word[2][1:],3) + bTen_bTwo(word[1][1:],3)
                        elif len(word) == 3:
                            b = "0100000010" + bTen_bTwo(word[2][1:],3) + bTen_bTwo(word[1][1:],3)
                    elif(word[0] == "lsr"):
                        if len(word) == 4:
                            b = "00001" + bTen_bTwo(word[3][1:], 5) + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                        elif len(word) == 3:
                            b = "0100000011" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "asr"):
                        if len(word) == 4:
                            b = "00010" + bTen_bTwo(word[3][1:], 5) + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                        elif len(word) == 3:
                            b = "0100000100" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "add"):
                        print(len(word))
                        if(len(word) == 3):
                            b = "101100000" + bTen_bTwo(str(int(word[2][1:])//4), 7)
                        elif(len(word) == 4):
                            if(word[3][0] == "r"):
                                b = "0001100" + bTen_bTwo(word[3][1:], 3) + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)

                            elif(word[2][0] == "["):
                                b = "00110" + bTen_bTwo(word[1][1:], 3) + bTen_bTwo(word[3][1:], 8)
                            else:
                                b = "0001110" + bTen_bTwo(word[3][1:], 3) + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "sub"):
                        if(len(word) == 3):
                            b = "101100001" + bTen_bTwo(str(int(word[2][1:])//4), 7)
                        elif(len(word) == 4):
                            if(word[3][0] == "r"):
                                b = "0001101" + bTen_bTwo(word[3][1:], 3) + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)

                            elif(word[2][0] == "["):
                                b = "00111" + bTen_bTwo(word[1][1:], 3) + bTen_bTwo(word[3][1:], 8)
                            else:
                                b = "0001111" + bTen_bTwo(word[3][1:], 3) + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "mov"):
                        b = "00100" + bTen_bTwo(word[1][1:], 3) + bTen_bTwo(word[2][1:],8)
                    elif(word[0] == "cmp"):
                        if(word[2][0] == "r"):
                            b = "0100001010" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                        else:
                            b = "00101" + bTen_bTwo(word[1][1:], 3) + bTen_bTwo(word[2][1:], 8)
                    elif(word[0] == "and"):
                        b = "0100000000" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "eor"):
                        b = "0100000001" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "asr"):
                        if(len(word) == 4):
                            b = "00010" + bTen_bTwo(word[3][1:], 5) + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                        elif(len(word) == 3):
                            b = "0100000100" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "adc"):
                        b = "0100000101" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "sbc"):
                        b = "0100000110" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "ror"):
                        b = "0100000111" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "tst"):
                        b = "0100001000" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "rsb"):
                        b = "0100001001" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "cmn"):
                        b = "0100001011" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "orr"):
                        b = "0100001100" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "mul"):
                        b = "0100001101" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "bic"):
                        b = "0100001110" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "mvn"):
                        b = "0100001111" + bTen_bTwo(word[2][1:], 3) + bTen_bTwo(word[1][1:], 3)
                    elif(word[0] == "str"):
                        b = "10010" + bTen_bTwo(word[1][1:], 3) + bTen_bTwo(str(int(word[3][1:-1])//4), 8)
                    elif(word[0] == "ldr"):
                        b = "10011" + bTen_bTwo(word[1][1:], 3) + bTen_bTwo(str(int(word[3][1:-1])//4), 8)
                    elif(word[0][0] == "b"):
                        if(len(word[0]) == 3):
                            b = "1101" + bTen_bTwo(getConditionValue(word[0][1:]), 4) + signed_2_complement(dictionary[word[1]] - i - 3, 8)
                        elif(len(word[0]) == 1):
                                b = "11100" + signed_2_complement(dictionary[word[1]] - i - 3,11)
                    output.write(bTwo_bHex(b) + " ")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
