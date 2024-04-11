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
     
def add_twos_complement(binary1, binary2): ##ye overflow ko ignore karega aur addition kardega.eg: max number + 1 = 0
    num1 = int(binary1, 2)
    num2 = int(binary2, 2)
    result = num1 + num2
    result_binary = bin(result & 0xFFFFFFFF)[2:].zfill(32)
    if result >= 0:
        return result_binary
    inverted_string = ''.join('1' if bit == '0' else '0' for bit in result_binary)
    twos_complement = bin(int(inverted_string, 2) + 1)[2:].zfill(32)
    return twos_complement

PC = 0
x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12 = 0,0,0,0,0,0,0,0,0,0,0,0,0
x13,x14,x15,x16,x17,x18,x19,x20,x21,x22,x23,x24,x25 = 0,0,0,0,0,0,0,0,0,0,0,0,0
x26,x27,x28,x29,x30,x31 = 0,0,0,0,0,0
regBinToName = {"00000" : x0,
                  "00001" : x1,
                  "00010" : x2,
                  "00011": x3,
                  "00100": x4,
                  "00101": x5,
                  "00110": x6,
                  "00111": x7,
                  "01000": x8, #"fp": "01000",
                  "01001": x9,
                  "01010": x10,
                  "01011": x11,
                  "01100": x12,
                  "01101": x13,
                  "01110": x14,
                  "01111": x15,
                  "10000": x16,
                  "10001": x17,
                  "10010": x18,
                  "10011": x19,
                  "10100": x20,
                  "10101": x21,
                  "10110": x22,
                  "10111": x23,
                  "11000": x24,
                  "11001": x25,
                  "11010": x26,
                  "11011": x27,
                  "11100": x28,
                  "11101": x29,
                  "11110": x30,
                  "11111": x31,
                  }

def func_R(ins):
    funct7 = ins[0:7]
    rs2 = regBinToName[ins[7:12]]
    rs1 = regBinToName[ins[12:17]]
    funct3 = ins[17:20]
    rd = regBinToName[ins[20:25]]

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

while PC<len(l):
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
