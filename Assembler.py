with open('C:\\Users\\nikhil\\Desktop\\C0_Test.txt') as f:
    list = f.readlines()
    l = []
    for i in list:
        l.append((i.rstrip("\n").split()))
with open('binary.txt','w') as f:
    f.write("")


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

def decimal_to_b32(decimal_number):
    if decimal_number < -2 ** 31 or decimal_number >= 2 ** 31:
        raise ValueError("Decimal number out of range for 32 bits representation")
    if decimal_number < 0:
        decimal_number = 2 ** 32 + decimal_number
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
    try:
        regABItoBinary[rs2]
        regABItoBinary[rs1]
        regABItoBinary[rd]
    except:
        return -1

    if instruction[0] == "sub":
        return (f'0100000{regABItoBinary[rs2]}{regABItoBinary[rs1]}{funct3[instruction[0]]}'
                f'{regABItoBinary[rd]}{opcode}')
    return (f'0000000{regABItoBinary[rs2]}{regABItoBinary[rs1]}{funct3[instruction[0]]}'
            f'{regABItoBinary[rd]}{opcode}')

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

        try:
            regABItoBinary[rs]
            regABItoBinary[rd]
        except:
            return -1
        imm = temp[2]
        imm_b = decimal_to_b32(int(imm))
        return f'{imm_b[20:]}{regABItoBinary[rs]}{funct3[ins_name]}{regABItoBinary[rd]}{opcode[ins_name]}'
    else:
        temp = instruction[1].split(',')
        temp2 = temp[1].split('(')
        rd = temp[0]
        rs = temp2[1].rstrip(')')
        try:
            regABItoBinary[rs]
            regABItoBinary[rd]
        except:
            return -1
        imm = temp2[0]
        imm_b = decimal_to_b32(int(imm))
        return f'{imm_b[20:]}{regABItoBinary[rs]}{funct3[ins_name]}{regABItoBinary[rd]}{opcode[ins_name]}'

def convertS(instruction):
    opcode = {"sw": "0100011"}
    funct3 = {"sw": "010"}
    ins_name = instruction[0]
    temp = instruction[1].split(',')
    temp2 = temp[1].split('(')
    rs2 = temp[0]
    rs1 = temp2[1].rstrip(')')
    try:
        regABItoBinary[rs1]
        regABItoBinary[rs2]
    except:
        return -1
    imm = temp2[0]
    imm_b = decimal_to_b32(int(imm))
    return f'{imm_b[20:27]}{regABItoBinary[rs2]}{regABItoBinary[rs1]}{funct3[ins_name]}{imm_b[27:]}{opcode[ins_name]}'

def convertB(instruction, index):
    opcode = "1100011"
    funct3 = {"beq": "000",
              "bne": "001",
              "blt": "100",
              "bge": "101",
              "bltu": "110",
              "bgeu": "111"
              }
    ins_name = instruction[0]
    rs1, rs2, imm = instruction[1].split(',')
    try:
        imm_b = decimal_to_b32(int(imm))
    except:
        val = label[imm]
        imm = (val - index)*4
        imm_b = decimal_to_b32(int(imm))
    try:
        regABItoBinary[rs1]
        regABItoBinary[rs2]
    except:
        return -1
    return (f'{imm_b[19]}{imm_b[21:27]}{regABItoBinary[rs2]}{regABItoBinary[rs1]}{funct3[ins_name]}'
            f'{imm_b[27:31]}{imm_b[20]}{opcode}')

def convertU(instruction):
    opcode = {"lui": "0110111",
              "auipc": "0010111"}
    ins_name = instruction[0]
    rd, imm = instruction[1].split(',')
    try:
        regABItoBinary[rd]
    except:
        return -1
    imm_b = decimal_to_b32(int(imm))
    return f'{imm_b[:20]}{regABItoBinary[rd]}{opcode[ins_name]}'

def convertJ(instruction, index):
    opcode = "1101111"
    rd,imm = instruction[1].split(',')
    try:
        imm_b = decimal_to_b32(int(imm))
    except:
        val = label[imm]
        imm = (val - index)*4
        imm_b = decimal_to_b32(int(imm))
    try:
        regABItoBinary[rd]
    except:
        return -1
    return f'{imm_b[11]}{imm_b[21:31]}{imm_b[20]}{imm_b[12:20]}{regABItoBinary[rd]}{opcode}'



for address_instruction in range(len(l)):
    instruct = l[address_instruction]
    if len(instruct) == 0:
        continue
    if ":" in instruct[0]:
        lab = instruct[0][:-1]
        label[lab] = address_instruction

for index in range(len(l)):
    instruction = l[index]

    if len(instruction) == 0 or len(instruction) == 1:
        continue
    if len(instruction) == 3:
        instruction = instruction[1:]

    ins_type = getInstructionType(instruction[0])
    if ins_type == "R":
        s = convertR(instruction)
    elif ins_type == "I":
        s = convertI(instruction)
    elif ins_type == "S":
        s = convertS(instruction)
    elif ins_type == "B":
        s = convertB(instruction,index)
        if instruction == ["beq", "zero,zero,0"]:
            VH = True
    elif ins_type == "U":
        s = convertU(instruction)
    elif ins_type == "J":
        s = convertJ(instruction,index)
    else:
        with open("binary.txt", mode='w') as f:
            print(f"ERROR..Invalid Instruction name at line no {index+1}")
            f.write("ERROR..Invalid Instruction name")
        break
    if s==-1:
        with open("binary.txt", mode='w') as f:

            print(f"ERROR..Invalid ABI register name at line no {index+1}")
            f.write("ERROR..Invalid ABI register name")
        break
    with open("binary.txt", mode='a') as f:
        print(s)
        f.write(s + "\n")
else:
    if not VH:
        with open("binary.txt", mode='w') as f:
            print("ERROR..Virtual Halt not present")
            f.write("ERROR..Virtual Halt not present")
    else:
        with open('binary.txt', 'r') as f:
            l = f.readlines()
            l[-1] = l[-1].rstrip("\n")
            s = "".join(l)
        with open('binary.txt', 'w') as f:
            f.write(s)
