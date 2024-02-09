def symboltonum(sym):
    return {
        'a': 10,
        'b': 11,
        'c': 12,
        'd': 13,
        'e': 14,
        'f': 15,
        'g': 16,
        'h': 17,
        'i': 18,
        'j': 19,
        'k': 20,
        'l': 21,
        'm': 22,
        'n': 23,
        'o': 24,
        'p': 25,
        'q': 26,
        'r': 27,
        's': 28,
        't': 29,
        'u': 30,
        'v': 31,
        'w': 32,
        'x': 33,
        'y': 34,
        'z': 35,
        'space':36,
        'backspace':37,
        'enter':38
    }[sym]

def number2bin(x):
    return bin(x)[2:].zfill(6)

def bintolist(x):
    x=str(x)
    return [int(x[0]),int(x[1]),int(x[2]),int(x[3]),int(x[4]),int(x[5])]

def listdecode(list):
        
        sym=str(list[0])+str(list[1])+str(list[2])+str(list[3])+str(list[4])+ str(list[5])

        return {
        '000000' :'0',
        '000001' :'1',
        '000010' :'2',
        '000011' :'3',
        '000100' :'4',
        '000101' :'5',
        '000110' :'6',
        '000111' :'7',
        '001000' :'8',
        '001001' :'9',
        '001010' :'a',
        '001011' :'b',
        '001100' :'c',
        '001101' :'d',
        '001110' :'e',
        '001111' :'f',
        '010000' :'g',
        '010001' :'h',
        '010010' :'i',
        '010011' :'j',
        '010100' :'k',
        '010101' :'l',
        '010110' :'m',
        '010111' :'n',
        '011000' :'o',
        '011001' :'p',
        '011010' :'q',
        '011011' :'r',
        '011100' :'s',
        '011101' :'t',
        '011110' :'u',
        '011111' :'v',
        '100000' :'w',
        '100001' :'x',
        '100010' :'y',
        '100011' :'z',
        '100100' :'space',
        '100101' :'backspace',
        '100110' :'enter'
    }[sym]

def main():

    y='space'
    x = symboltonum(y)
    x = number2bin(x)
    x= bintolist(x)
    print(x)
    x=listdecode(x)
    print(x)

if __name__ == "__main__":
    main()