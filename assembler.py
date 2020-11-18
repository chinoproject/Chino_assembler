import sys
from arg import *
import struct
def gen_orri_opcode():
    return 0x2010000000000000
def set_reg1(reg):
    if reg < 31:
        return reg << 47
    else:
        raise IndexError
def set_reg2(reg):
    if reg < 31:
        return reg << 42
def set_imm(imm):
    if imm < (2**32-1):
        return imm << 10
def gen_orri(reg1,reg2,imm):
    return gen_orri_opcode() | set_reg1(reg1) | set_reg2(reg2) | set_imm(imm)

def main():
    inst_list = []
    with open(input_filename) as f:
        for inst in f:
            temp = inst.replace("\n","").split(",")
            inst = temp[0].split(" ")
            op = temp[1:]
            op.insert(0,inst[1])
            hex_str = ""

            if inst[0][-2:] == "ri":
                op1 = int(op[0][1:])
                op2 = int(op[1][1:])
                op3 = int(op[2])
                hex_str = hex(gen_orri(op1,op2,op3)) 

            inst_list.append(hex_str)
    if output_hex:
        with open(output_filename,"w+") as f:
            for inst in inst_list:
                f.write(inst + "\n")
    else:
        with open(output_filename,"wb+") as f:
            for inst in inst_list:
                f.write(struct.pack(">Q",int(inst,base=16)))

if __name__ == "__main__":
    main()