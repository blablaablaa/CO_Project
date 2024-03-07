with open("C:\\Users\\nikhil\Documents\\C0_Test.txt") as f:
    list = f.readlines()
    l = []
    for i in list:
        l.append((i.rstrip("\n").split()))
print(l)

R_type = ["add", "sub", "slt", "sltu", "xor", "sll", "srl", "or", "and"]
I_type = ["lb", "lh", "lw", "ld", "addi", "sltiu", "jalr"]
S_type = ["sb", "sh", "sw", "sd"]
B_type = ["beq", "bne", "bge", "bgeu", "blt", "bltu"]
U_type = ["auipc", "lui"]
J_type = ["jal"]

label = {} 

regABItoBinary = {"zero": "00000",
                  "ra": "00001",
                  "sp": "00010",
                  "gp": "00011",
                  "tp": "00100",
                  "t0": "00101",
                  "t1": "00110",
                  "t2": "00111",
                  "s0": "01000", "fp": "01000",
                  "s1": "01001",
                  "a0": "01010",
                  "a1": "01011",
                  "a2": "01100",
                  "a3": "01101",
                  "a4": "01110",
                  "a5": "01111",
                  "a6": "10000",
                  "a7": "10001",
                  "s2": "10010",
                  "s3": "10011",
                  "s4": "10100",
                  "s5": "10101",
                  "s6": "10110",
                  "s7": "10111",
                  "s8": "11000",
                  "s9": "11001",
                  "s10": "11010",
                  "s11": "11011",
                  "t3": "11100",
                  "t4": "11101",
                  "t5": "11110",
                  "t6": "11111",
                  }

VH = False

def decimal_to_b11(decimal_number):
    if decimal_number < -2**11 or decimal_number >= 2**11:
        raise ValueError("Decimal number out of range for 12 bits representation")
    if decimal_number < 0:
        decimal_number = 2**12 + decimal_number
    binary_representation = bin(decimal_number)[2:]
    padded_binary = binary_representation.zfill(12)
    return str(padded_binary)
    
def decimal_to_b20(decimal_number):
    if decimal_number < -2**19 or decimal_number >= 2**19:
        raise ValueError("Decimal number out of range for 20 bits representation")
    if decimal_number < 0:
        decimal_number = 2**20 + decimal_number
    binary_representation = bin(decimal_number)[2:]
    padded_binary = binary_representation.zfill(20)
    return str(padded_binary)

def decimal_to_b32(decimal_number):
    if decimal_number < -2**31 or decimal_number >= 2**31:
        raise ValueError("Decimal number out of range for 12 bits representation")
    if decimal_number < 0:
        decimal_number = 2**32 + decimal_number
    binary_representation = bin(decimal_number)[2:]
    padded_binary = binary_representation.zfill(32)
    return str(padded_binary)

def getInstructionType(ins):
    if ins in R_type:
        return "R"
    if ins in I_type:
        return "I"
    if ins in S_type:
        return "S"
    if ins in B_type:
        return "B"
    if ins in U_type:
        return "U"
    if ins in J_type:
        return "J"
    return "INVALID"

def convertR(instruction):
    funct3 = {"add": "000",
              "sub": "000",
              "sll": "001",
              "slt": "010",
              "sltu": "011",
              "xor": "100",
              "srl": "101",
              "or": "110",
              "and": "111"}
    opcode = "0110011"
    temp = instruction[1].split(',')
    rd = temp[0]
    rs1 = temp[1]
    rs2 = temp[2]

    if instruction[0] == "sub":
        return (f'0100000{regABItoBinary[rs2]} {regABItoBinary[rs1]} {funct3[instruction[0]]}'
                f' {regABItoBinary[rd]} {opcode}')
    return (f'0000000{regABItoBinary[rs2]} {regABItoBinary[rs1]} {funct3[instruction[0]]} '
                f'{regABItoBinary[rd]} {opcode}')

def convertI(instruction):
    funct3 = {"lw": "010",
              "addi": "000",
              "sltiu": "011",
              "jalr": "000"
              }
    opcode = {"lw": "0000011",
              "addi": "0010011",
              "sltiu": "0010011",
              "jalr": "1100111"
              }
    ins_name = instruction[0]
    if ins_name == "addi" or ins_name == "sltiu" or ins_name == "jalr":
        temp = instruction[1].split(',')
        rd = temp[0]
        rs = temp[1]
        imm = temp[2]
        imm_b = decimal_to_b32(int(imm))
        return f'{imm_b[20:]} {regABItoBinary[rs]} {funct3[ins_name]} {regABItoBinary[rd]} {opcode[ins_name]}'
    else:
        temp = instruction[1].split(',')
        temp2 = temp[1].split('(')
        rd = temp[0]
        rs = temp2[1].rstrip(')')
        imm = temp2[0]
        imm_b = decimal_to_b32(int(imm))
        return f'{imm_b[20:]} {regABItoBinary[rs]} {funct3[ins_name]} {regABItoBinary[rd]} {opcode[ins_name]}'

def convertS(instruction):
    opcode = {"sw": "0100011"}
    funct3 = {"sw": "010"}
    ins_name = instruction[0]
    temp = instruction[1].split(',')
    temp2 = temp[1].split('(')
    rs2 = temp[0]
    rs1 = temp2[1].rstrip(')')
    imm = temp2[0]
    imm_b = decimal_to_b11(int(imm))
    return f'{imm_b[0:7]} {regABItoBinary[rs2]} {regABItoBinary[rs1]} {funct3[ins_name]} {imm_b[7:]} {opcode[ins_name]}'

def convertB(instruction):
    opcode = "1100011"
    funct3 = {"beq": "000",
              "bne": "001",
              "blt": "100",
              "bge": "101",
              "bltu": "110",
              "bgeu": "111"
              }
    ins_name = instruction[0]
    rs1,rs2,imm = instruction[1].split(',')
    imm_b = decimal_to_b32(int(imm))
    return (f'{imm_b[19]} {imm_b[21:27]} {regABItoBinary[rs2]} {regABItoBinary[rs1]} {funct3[ins_name]}'
            f' {imm_b[27:31]} {imm_b[20]} {opcode}')

def convertU(instruction):
    opcode = {"lui": "0110111",
              "auipc": "0010111"}
    ins_name = instruction[0]
    rd, imm = instruction[1].split(',')
    imm_b = decimal_to_b32(int(imm))
    return f'{imm_b[:20]} {regABItoBinary[rd]} {opcode[ins_name]}'

def convertJ(instruction):
    opcode = "1100111"
    rd,imm = instruction[1].split(',')
    imm_b = decimal_to_b32(int(imm))
    return f'{imm_b[11]} {imm_b[21:31]} {imm_b[20]} {imm_b[12:20]} {regABItoBinary[rd]} {opcode}'


l = [instruction for instruction in l if instruction]

for address_instruction in range(len(l)):
    instruct = l[address_instruction]
    if len(instruct)==3:
        x = (instruct[0])[:-1]
        l[address_instruction] =  instruct[1:]
        label[x] = address_instruction
    
for instruction in l:
    ins_type = getInstructionType(instruction[0])
    if ins_type == "R":
        s = convertR(instruction)
    elif ins_type == "I":
        s = convertI(instruction)
    elif ins_type == "S":
        s = convertS(instruction)
    elif ins_type == "B":
        s = convertB(instruction)
        if instruction == ["beq", "zero,zero,0"]:
             VH = True
    elif ins_type == "U":
        s = convertU(instruction)
    elif ins_type == "J":
        s = convertJ(instruction)
    else:
        print(instruction[0])
        with open("binary.txt", mode='w') as f:
            f.write("ERROR1")
        break
    print("adding....",end = " ")
    print(" ".join(instruction))
    with open("binary.txt", mode='a') as f:
        f.write(s+"\n")

if not VH:
    with open("binary.txt", mode='w') as f:
        f.write("ERROR")
else:
    pass

# s = convertJ(['jal', 'ra,-1024'])
# print(s)