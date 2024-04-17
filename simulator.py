import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
with open(input_file) as f:
    list = f.readlines()
    li = []
    for i in list:
        li.append(i.rstrip("\n"))


# l = []


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
    if opcode == "1111111" or "0000000" or "1100110":
        return "Bonus"
    return "Z"


def decimal_to_unsigned_binary(decimal_number):
    binary_string = bin(decimal_number & 0xFFFFFFFF)[2:].zfill(32)
    return binary_string


def decimal_to_twos_complement(decimal_number):
    binary_string = bin(abs(decimal_number) & 0xFFFFFFFF)[2:].zfill(32)
    if decimal_number < 0:
        inverted_string = ''.join('1' if bit == '0' else '0' for bit in binary_string)
        twos_complement = bin(int(inverted_string, 2) + 1)[2:].zfill(32)
        return twos_complement
    return binary_string


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


def binary_to_decimal_twos_complement(binary_str):  ##converts 2's complement binary to decimal
    if binary_str[0] == '1':
        binary_str = ''.join(['1' if bit == '0' else '0' for bit in binary_str])
        binary_str = bin(int(binary_str, 2) + 1)[2:].zfill(32)
        decimal_value = int(binary_str, 2)
        decimal_value = -decimal_value
    else:
        decimal_value = int(binary_str, 2)
    return decimal_value


def sext(binary_str):
    return binary_to_decimal_twos_complement(binary_str)


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


def sign_extend(binary_str):
    is_negative = binary_str[0] == '1'
    extension = '1' if is_negative else '0'
    extend_length = 32 - len(binary_str)
    extended_binary_str = extension * extend_length + binary_str
    return extended_binary_str


def binary_to_hex(binary_str):
    binary_str = binary_str.zfill((len(binary_str) + 3) // 4 * 4)
    chunks = [binary_str[i:i + 4] for i in range(0, len(binary_str), 4)]
    hex_str = ''.join(hex(int(chunk, 2))[2:] for chunk in chunks)
    return hex_str


#
# def hex_to_binary(hex_str):
#     binary_digits = [bin(int(hex_digit, 16))[2:].zfill(4) for hex_digit in hex_str]
#     binary_str = ''.join(binary_digits)
#     binary_str = binary_str.zfill(32)
#     return binary_str

PC = "00000000000000000000000000000000"
data_mem = {
    "0x00010000": "00000000000000000000000000000000",
    "0x00010004": "00000000000000000000000000000000",
    "0x00010008": "00000000000000000000000000000000",
    "0x0001000c": "00000000000000000000000000000000",
    "0x00010010": "00000000000000000000000000000000",
    "0x00010014": "00000000000000000000000000000000",
    "0x00010018": "00000000000000000000000000000000",
    "0x0001001c": "00000000000000000000000000000000",
    "0x00010020": "00000000000000000000000000000000",
    "0x00010024": "00000000000000000000000000000000",
    "0x00010028": "00000000000000000000000000000000",
    "0x0001002c": "00000000000000000000000000000000",
    "0x00010030": "00000000000000000000000000000000",
    "0x00010034": "00000000000000000000000000000000",
    "0x00010038": "00000000000000000000000000000000",
    "0x0001003c": "00000000000000000000000000000000",
    "0x00010040": "00000000000000000000000000000000",
    "0x00010044": "00000000000000000000000000000000",
    "0x00010048": "00000000000000000000000000000000",
    "0x0001004c": "00000000000000000000000000000000",
    "0x00010050": "00000000000000000000000000000000",
    "0x00010054": "00000000000000000000000000000000",
    "0x00010058": "00000000000000000000000000000000",
    "0x0001005c": "00000000000000000000000000000000",
    "0x00010060": "00000000000000000000000000000000",
    "0x00010064": "00000000000000000000000000000000",
    "0x00010068": "00000000000000000000000000000000",
    "0x0001006c": "00000000000000000000000000000000",
    "0x00010070": "00000000000000000000000000000000",
    "0x00010074": "00000000000000000000000000000000",
    "0x00010078": "00000000000000000000000000000000",
    "0x0001007c": "00000000000000000000000000000000",
}
regBinToName = {"00000": "00000000000000000000000000000000",
                "00001": "00000000000000000000000000000000",
                "00010": "00000000000000000000000100000000",
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

    if funct7 == "0000000":
        if funct3 == "000":  # add
            rd = add_twos_complement(rs1, rs2)
            regBinToName[ins[20:25]] = rd
        elif funct3 == "001":  # sll
            shift_amount = int(rs2[-5:], 2)
            result = int(rs1, 2) << shift_amount
            rd = bin(result)[2:].zfill(32)
            regBinToName[ins[20:25]] = rd
        elif funct3 == "010":  # slt
            if sext(rs1) < sext(rs2):
                rd = "00000000000000000000000000000001"
                regBinToName[ins[20:25]] = rd
            else:
                rd = "00000000000000000000000000000000"
                regBinToName[ins[20:25]] = rd
        elif funct3 == "011":  # sltu
            if int(unsigned(rs1), 2) < int(unsigned(rs2), 2):
                rd = "00000000000000000000000000000001"
                regBinToName[ins[20:25]] = rd
            else:
                rd = "00000000000000000000000000000000"
                regBinToName[ins[20:25]] = rd
        elif funct3 == "100":  # xor
            rd = bitwise_xor(rs1, rs2)
            regBinToName[ins[20:25]] = rd
        elif funct3 == "101":  # srl
            shift_amount = int(unsigned(rs2)[-5:], 2)
            result = int(rs1, 2) >> shift_amount
            rd = bin(result)[2:].zfill(32)
            regBinToName[ins[20:25]] = rd
        elif funct3 == "110":  # or:
            rd = bitwise_or(rs1, rs2)
            regBinToName[ins[20:25]] = rd
        elif funct3 == "111":  # and
            rd = bitwise_and(rs1, rs2)
            regBinToName[ins[20:25]] = rd
    elif funct7 == "0100000":  # sub
        rs1 = signed(rs1)
        rs2 = signed(rs2)
        rd = rs1 - rs2
        rd = decimal_to_twos_complement(rd)
        regBinToName[ins[20:25]] = rd
    elif funct7 == "1111111":  # mul
        rs1 = sext(rs1)
        rs2 = sext(rs2)
        rd = rs1 * rs2
        rd = str(bin(rd))
        if len(rd) > 34: 
            rd = rd[-32:]
        else:
            rd = rd[2:].zfill(32)
        regBinToName[ins[20:25]] = rd


def func_I(ins):
    imm_bin = ins[0:12]
    rs1 = regBinToName[ins[12:17]]
    funct3 = ins[17:20]
    rd = regBinToName[ins[20:25]]
    opcode = ins[25:]
    global PC
    if funct3 == "010":  # lw
        mem_ind = add_twos_complement(rs1, sign_extend(imm_bin))
        mem_ind = binary_to_hex(mem_ind)
        mem_ind = "0x" + mem_ind
        rd = data_mem[mem_ind]
        regBinToName[ins[20:25]] = rd
        PC = add_twos_complement(PC, "100")
    elif funct3 == "000" and opcode == "0010011":  # addi
        rd = add_twos_complement(rs1, sign_extend(imm_bin))
        regBinToName[ins[20:25]] = rd
        PC = add_twos_complement(PC, "100")
    elif funct3 == "011":  # sltiu
        if int(rs1, 2) < int(sign_extend(imm_bin), 2):
            rd = "00000000000000000000000000000001"
            regBinToName[ins[20:25]] = rd
            PC = add_twos_complement(PC, "100")
        else:
            rd = "00000000000000000000000000000000"
            regBinToName[ins[20:25]] = rd
            PC = add_twos_complement(PC, "100")
    elif funct3 == "000":  # jalr
        # global PC
        rd = add_twos_complement(PC, unsigned("100"))  # rd = PC+4
        PC = add_twos_complement(rs1, sign_extend(imm_bin))
        PC = PC[:-1] + "0"
        # print("PC:", PC)
        regBinToName[ins[20:25]] = rd


def func_S(ins):
    # global PC
    imm_bin = ins[0:7] + ins[20:25]
    rs2 = regBinToName[ins[7:12]]
    rs1 = regBinToName[ins[12:17]]
    funct3 = ins[17:20]
    mem_ind = add_twos_complement(rs1, sign_extend(imm_bin))
    mem_ind = binary_to_hex(mem_ind)
    mem_ind = "0x" + mem_ind
    data_mem[mem_ind] = rs2


def func_B(ins):
    global PC
    imm_bin = ins[0] + ins[24] + ins[1:7] + ins[20:24]
    rs2 = regBinToName[ins[7:12]]
    rs1 = regBinToName[ins[12:17]]
    funct3 = ins[17:20]
    if funct3 == "000":  # beq
        if rs1 == rs2:
            PC = add_twos_complement(PC, sign_extend(imm_bin + "0"))
        else:
            PC = add_twos_complement(PC, "100")
    elif funct3 == "001":  # bne
        if rs1 != rs2:
            PC = add_twos_complement(PC, sign_extend(imm_bin + "0"))
        else:
            PC = add_twos_complement(PC, "100")
    elif funct3 == "100":  # blt
        if sext(rs1) < sext(rs2):
            PC = add_twos_complement(PC, sign_extend(imm_bin + "0"))
        else:
            PC = add_twos_complement(PC, "100")
    elif funct3 == "101":
        if sext(rs1) >= sext(rs2):
            PC = add_twos_complement(PC, sign_extend(imm_bin + "0"))
        else:
            PC = add_twos_complement(PC, "100")


def func_U(ins, PC):
    # global PC
    imm = ins[0:20]
    opcode = ins[25:]
    if opcode == "0110111":  # lui
        rd = imm + 12 * "0"
        regBinToName[ins[20:25]] = rd
    elif opcode == "0010111":  # auipc
        rd = add_twos_complement(imm + 12 * "0", PC)
        regBinToName[ins[20:25]] = rd


def func_J(ins):
    global PC
    imm = ins[0] + ins[12:20] + ins[11] + ins[1:11]
    imm = sign_extend(imm + "0")
    rd = add_twos_complement(PC, unsigned("100"))  # rd = PC+4
    PC = add_twos_complement(PC, imm)
    PC = PC[:-1] + "0"
    regBinToName[ins[20:25]] = rd


def func_Bonus(ins):
    opcode = ins[25:]
    if opcode == "0000000":
        return
    if opcode == "1111111":  # reset (rst)
        for i in regBinToName.keys():
            regBinToName[i] = "00000000000000000000000000000000"
        regBinToName["00010"] = "00000000000000000000000100000000"
        return
    if opcode == "1100110":  # rvrs
        rs = regBinToName[ins[12:17]]
        rd = rs[::-1]
        regBinToName[ins[20:25]] = rd
        return


l = dict()
for i in range(len(li)):
    l[decimal_to_unsigned_binary(i * 4)] = li[i]
# print(l)
with open(output_file, 'w') as f:
    f.write("")
while True:
    ins = l[PC]
    print("ins", ins)
    ins_type = get_instruction_type(ins)
    if ins_type == "R":
        func_R(ins)
        PC = add_twos_complement(PC, "100")
    elif ins_type == "I":
        func_I(ins)
    elif ins_type == "S":
        func_S(ins)
        PC = add_twos_complement(PC, "100")
    elif ins_type == "B":
        func_B(ins)

    elif ins_type == "U":
        func_U(ins, PC)
        PC = add_twos_complement(PC, "100")
    elif ins_type == "J":
        func_J(ins)
    elif ins_type == "Bonus":
        func_Bonus(ins)
        PC = add_twos_complement(PC, "100")
    regBinToName["00000"] = "00000000000000000000000000000000"
    # print(PC)
    # print(regBinToName)
    # print(data_mem)
    with open(output_file, 'a') as f:
        f.write("0b" + PC + " ")
        for key, value in regBinToName.items():
            f.write("0b" + value + " ")
        f.write("\n")
    if ins == "00000000000000000000000001100011" or ins =="00000000000000000000000000000000":
        # print("HALT MET")
        break
with open(output_file, 'a') as f:
    for key, value in data_mem.items():
        f.write(key + ":0b" + value + "\n")
for key,val in l.items():
    print(key,val)
