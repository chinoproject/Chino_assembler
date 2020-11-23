import sys
from arg import *
import struct
from gen_bytecode import *

def main():
    inst_list = []
    with open(input_filename,encoding="utf-8") as f:
        for inst in f:
            if len(inst.replace("\n","").replace("\t","")) == 0:
                continue
            if inst.replace("\t","").replace("\n","").replace(" ","")[0] == "#": #跳过注释
                continue
            temp = inst.replace("\n","").split("#")
            if len(temp) >= 2:
                temp = temp[0].split(",")
            else:
                temp = temp[0].split(",")
            inst = temp[0].split(" ")
            op = temp[1:]
            op.insert(0,inst[1])
            if len(op) == 3:
                hex_str = bytecode(inst[0],op[0],op[1],op[2])
            elif len(op) == 2:
                hex_str = bytecode(inst[0],op[0],op[1])
            inst_list.append(hex_str)
    if output_hex:
        with open(output_filename,"w+") as f:
            for inst in inst_list:
                f.write(inst + "\n")
    else:
        with open(output_filename,"wb+") as f:
            for inst in inst_list:
                f.write(struct.pack(">Q",int(inst,base=16)))

    if rtl_code_gen:
        with open("rtl_" + output_filename,"w+") as f:
            for i in range(len(inst_list)):
                f.write("inst_mem[" + str(i) + "]" + " <= " + "64'h" + inst_list[i][2:] + ";\n")

if __name__ == "__main__":
    main()