# Main Code
list_of_registor_name = ["x0","x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11","x12","x13","x14","x15","x16","x17","x18","x19","x20","x21","x22","x23","x24","x25","x26","x27","x28","x29","x30","x31"]
list_of_ABI_registor_name = ["zero","ra","sp","gp","tp","t0","t1","t2","s0/fp","s1","a0","a1","a2","a3","a4","a5","a6","a7","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","t3","t4","t5","t6"]


link_ABI_registor = dict([(key, value) for i, (key, value) in enumerate(zip(list_of_ABI_registor_name, list_of_registor_name))])

value_of_registor = [0]*32

def int_to_binary_with_bits(number, num_bits):
    binary_representation = format(number, f'0{num_bits}b')
    return binary_representation

def get_registor(ABI_name):
    return link_ABI_registor[ABI_name]

def get_Address(ABI_name):
    x = get_registor
    x = int(x[1:])
    return int_to_binary_with_bits(x,5)

funct7 = "0000000"
## Working...
# LET i be the input instruction
# Let t denote type of instruction
if i.split(",")[0] in [add,...]:
    t = 0










