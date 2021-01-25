import sys
from arg import *
import struct
from gen_bytecode import bytecode,check_par
inst_lineno = 0
lineno = 0
tag_to_addr = {}
postpone_calc = {}
jump_inst = {"jng":True,"jg":True,"jnl":True,"jl":True,"je":True,"jne":True}
data_inst = {"loadb":True,"loadh":True,"loadw":True,"loadbu":True,"loadhu":True,
                "loadwl":True,"loadwr":True,"storeb":True,"storeh":True,"storew":True,
                "storewl":True,"storewr":True}

def main():
    inst_list = []
    global lineno
    global tag_to_addr
    global postpone_calc
    global inst_lineno
    flag = False
    with open(input_filename,encoding="utf-8") as f:
        for inst in f:
            if len(inst.replace("\n","").replace("\t","")) == 0:
                continue
            if inst.replace("\t","").replace("\n","").replace(" ","")[0] == "#": #跳过注释
                continue

            temp = inst.replace("\n","").split("#") 
            if len(temp) >= 2:
                temp = temp[0].split(",")   #有注释
            else:
                temp = temp[0].split(",")   #无注释
            if temp[0] == "nop":
                inst_list.append("0x0000000000000000")
                continue
            inst = temp[0].split(" ")
            print(inst)
            lineno = lineno + 1
            if inst[0][-1] == ':':
                #有标号
                if lineno == 1:
                    tag_to_addr[inst[0][:-1]] = 0
                else:
                    tag_to_addr[inst[0][:-1]] = 8*(inst_lineno)   #计算跳转地址
                print(inst[0])
                continue
            else:
                inst_lineno = inst_lineno + 1
            op = temp[1:]
            if inst[0] == "ret":
                inst_list.append("0x4190000000000000")
                continue
            op.insert(0,inst[1])
            inst = inst[0]
            if inst == "jmp" or inst == "call":
                if op[0][0] != '$':
                    try:
                        op[0] = tag_to_addr[op[0]]
                        hex_str = hex(0x2110000000000000 | op[0] << 20)
                    except:
                        postpone_calc[inst_lineno] = [inst,op]
                        continue
                else:
                    op.append("$0")
            else:
                try:
                    if not (op[-1][0] == '$' or (check_par(op[-1]) + 1)):
                        op[-1] = tag_to_addr[op[-1]]

                except:
                    postpone_calc[inst_lineno] = [inst,op]
                    continue
            if inst == "loop":
                if op[0][0] == '$':
                    op.append("$0")
            if len(op) == 3:
                hex_str = bytecode(inst,op[0],op[1],op[2])
            elif len(op) == 2:
                hex_str = bytecode(inst,op[0],op[1])
            inst_list.append(hex_str)

    for i in postpone_calc:
        inst = postpone_calc[i][0]
        op = postpone_calc[i][1]
        print(op)
        op[-1] = str(tag_to_addr[op[-1]])
        if len(op) < 2:
            op.append("0")

        if len(op) == 3:
            hex_str = bytecode(inst,op[0],op[1],op[2])
        elif len(op) == 2:
            hex_str = bytecode(inst,op[0],op[1])
        
        inst_list.insert(i - 1,hex_str)

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