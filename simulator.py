with open('C:\\Users\\Vikram\\Desktop\\binary.txt') as f:
    list = f.readlines()
    l = []
    for i in list:
        l.append(i.rstrip("\n"))
l = []


def get_instruction_type(ins):
    opcode = ins[25:]
    if opcode == "0110011":
        return "R"
    if opcode == "0000011" or opcode == "0010011" or opcode == "1100111":
        return "I"
    if opcode == "0100011":
        return "S"
    if opcode == "1100011":
        return "B"
    if opcode == "0110111" or opcode == "0010111":
        return "U"
    if opcode == "1101111":
        return "J"
    return "Z"


def decimal_to_unsigned_binary(decimal_number):
    binary_string = bin(decimal_number & 0xFFFFFFFF)[2:].zfill(32)
    return binary_string


def decimal_to_twos_complement(decimal_number):
    binary_string = bin(decimal_number & 0xFFFFFFFF)[2:].zfill(32)
    if decimal_number >= 0:
        return binary_string
    inverted_string = ''.join('1' if bit == '0' else '0' for bit in binary_string)
    twos_complement = bin(int(inverted_string, 2) + 1)[2:].zfill(32)
    return twos_complement


def add_twos_complement(binary1, binary2):  ##ye overflow ko ignore karega aur addition kardega.eg: max number + 1 = 0
    num1 = int(binary1, 2)
    num2 = int(binary2, 2)
    result = num1 + num2
    result_binary = bin(result & 0xFFFFFFFF)[2:].zfill(32)
    if result >= 0:
        return result_binary
    inverted_string = ''.join('1' if bit == '0' else '0' for bit in result_binary)
    twos_complement = bin(int(inverted_string, 2) + 1)[2:].zfill(32)
    return twos_complement


def bitwise_and(binary1, binary2):
    num1 = int(binary1, 2)
    num2 = int(binary2, 2)
    result = num1 & num2
    result_binary = bin(result)[2:].zfill(len(binary1))
    return result_binary


def bitwise_or(binary1, binary2):
    num1 = int(binary1, 2)
    num2 = int(binary2, 2)
    result = num1 | num2
    result_binary = bin(result)[2:].zfill(len(binary1))
    return result_binary


def bitwise_xor(binary1, binary2):
    num1 = int(binary1, 2)
    num2 = int(binary2, 2)
    result = num1 ^ num2
    result_binary = bin(result)[2:].zfill(len(binary1))
    return result_binary

def sext(binary_str):
    return binary_to_decimal_twos_complement(binary_str)

def binary_to_decimal_twos_complement(binary_str):  ##converts 2's complement binary to decimal
    if binary_str[0] == '1':
        binary_str = ''.join(['1' if bit == '0' else '0' for bit in binary_str])
        binary_str = bin(int(binary_str, 2) + 1)[2:].zfill(32)
        decimal_value = int(binary_str, 2)
        decimal_value = -decimal_value
    else:
        decimal_value = int(binary_str, 2)
    return decimal_value
def unsigned(binary_str):
    num_zeroes = 32 - len(binary_str)
    extended_str = '0' * num_zeroes + binary_str
    return extended_str

def binary_to_decimal_signed(binary_str):  ##converts signed binary to decimal
    if binary_str[0] == '1':
        decimal_value = -int(binary_str[1:], 2)
    else:
        decimal_value = int(binary_str, 2)
    return decimal_value

def signed(binary_str):
    return binary_to_decimal_signed(binary_str)

PC = 0
regBinToName = {"00000": "00000000000000000000000000000000",
                "00001": "00000000000000000000000000000000",
                "00010": "00000000000000000000000000000000",
                "00011": "00000000000000000000000000000000",
                "00100": "00000000000000000000000000000000",
                "00101": "00000000000000000000000000000000",
                "00110": "00000000000000000000000000000000",
                "00111": "00000000000000000000000000000000",
                "01000": "00000000000000000000000000000000",  # "fp": "01000",
                "01001": "00000000000000000000000000000000",
                "01010": "00000000000000000000000000000000",
                "01011": "00000000000000000000000000000000",
                "01100": "00000000000000000000000000000000",
                "01101": "00000000000000000000000000000000",
                "01110": "00000000000000000000000000000000",
                "01111": "00000000000000000000000000000000",
                "10000": "00000000000000000000000000000000",
                "10001": "00000000000000000000000000000000",
                "10010": "00000000000000000000000000000000",
                "10011": "00000000000000000000000000000000",
                "10100": "00000000000000000000000000000000",
                "10101": "00000000000000000000000000000000",
                "10110": "00000000000000000000000000000000",
                "10111": "00000000000000000000000000000000",
                "11000": "00000000000000000000000000000000",
                "11001": "00000000000000000000000000000000",
                "11010": "00000000000000000000000000000000",
                "11011": "00000000000000000000000000000000",
                "11100": "00000000000000000000000000000000",
                "11101": "00000000000000000000000000000000",
                "11110": "00000000000000000000000000000000",
                "11111": "00000000000000000000000000000000",
                }

def func_R(ins):
    funct7 = ins[0:7]
    rs2 = regBinToName[ins[7:12]]
    rs1 = regBinToName[ins[12:17]]
    funct3 = ins[17:20]
    rd = regBinToName[ins[20:25]]

    if funct7 == "0000000":
        if funct3 == "000": #add
            rd = add_twos_complement(sext(rs1), sext(rs2))
            regBinToName[ins[20:25]] = rd
        elif funct3 == "001": #sll
            shift_amount = int(unsigned(rs2)[-5:], 2)
            result = int(rs1, 2) << shift_amount
            rd = bin(result)[2:].zfill(32)
            regBinToName[ins[20:25]] = rd
        elif funct3 == "010": #slt
            if sext(rs1) < sext(rs2):
                rd = "00000000000000000000000000000001"
                regBinToName[ins[20:25]] = rd
        elif funct3 == "011": #sltu
            if int(unsigned(rs1),2) < int(unsigned(rs2),2):
                rd = "00000000000000000000000000000001"
                regBinToName[ins[20:25]] = rd
        elif funct3 == "100": #xor
            rd = bitwise_xor(rs1,rs2)
            regBinToName[ins[20:25]] = rd
        elif funct3 == "101": #srl
            shift_amount = int(unsigned(rs2)[-5:], 2)
            result = int(rs1, 2) >> shift_amount
            rd = bin(result)[2:].zfill(32)
            regBinToName[ins[20:25]] = rd
        elif funct3 == "110": #or:
            rd = bitwise_or(rs1, rs2)
            regBinToName[ins[20:25]] = rd
        elif funct3 == "111": #and
            rd = bitwise_and(rs1, rs2)
            regBinToName[ins[20:25]] = rd
    elif funct7 == "0100000": #sub
        rs1 = signed(rs1)
        rs2 = signed(rs2)
        rd = rs1-rs2
        rd = decimal_to_twos_complement(rd)
        regBinToName[ins[20:25]] = rd

def func_I(ins):
    imm_bin = ins[0:12]
    rs1 = regBinToName[ins[12:17]]
    funct3 = ins[17:20]
    rd = regBinToName[ins[20:25]]


def func_S(ins):
    imm_bin = ins[0:7] + ins[20:25]
    rs2 = ins[7:12]
    rs1 = ins[12:17]
    funct3 = ins[17:20]


def func_B(ins):
    imm_bin = ins[0:7] + ins[20:25]
    rs2 = ins[7:12]
    rs1 = ins[12:17]
    funct3 = ins[17:20]


def func_U(ins):
    imm = ins[0:20]
    rd = ins[20:25]


def func_J(ins):
    imm = ins[0:20]
    rd = ins[20:25]


while PC < len(l):
    ins = l[PC]
    ins_type = get_instruction_type(ins)
    if ins_type == "R":
        func_R(ins)
    elif ins_type == "I":
        func_I(ins)
    elif ins_type == "S":
        func_S(ins)
    elif ins_type == "B":
        func_B(ins)
    elif ins_type == "U":
        func_U(ins)
    elif ins_type == "J":
        func_J(ins)
