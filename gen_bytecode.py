
def check_par(v):
    if type(v) == str:
        base = v[:2]
        if base == "0x":
            return int(v,base=16)
        elif base == "0b":
            return int(v,base=2)
        else:
            return int(v)
    elif type(v) == int:
        return v
    else:
        raise TypeError

def shift_n(v,n,max_value):
    if v < max_value:
        return v << n
    else:
        raise IndexError

def set_reg1(reg):
    return shift_n(check_par(reg[1:]),47,32)

def set_reg2(reg):
    return shift_n(check_par(reg[1:]),42,32)

def set_reg3(reg):
    return shift_n(check_par(reg[1:]),37,32)

def set_imm(imm):
    return shift_n(check_par(imm),10,2**32)


class InstType:
    def __init__(self,inst,op1,op2,op3):
        self.inst = ""
        self.bytecode = 0x00

    def __str__(self):
        text  = self.inst + "\n" + "bytecode:" + str(self.bytecode)
        return text
class TypeRI(InstType):
    def __init__(self,inst,reg1,op2,imm=None):
        self.raw_inst = inst
        self.text_dict = {"or":0x2010000000000000,"and":0x2020000000000000,"xor":0x2030000000000000,"not":0x2040000000000000,"shl":0x2050000000000000,\
                        "shr":0x2060000000000000,"sar":0x2070000000000000,"mov":0x2080000000000000,"movz":0x2090000000000000,"movn":0x20a0000000000000,\
                        "add":0x20b0000000000000,"sub":0x20c0000000000000}
        spec_list = {"sar":True,"shl":True,"shr":True}
        if imm:
            if spec_list.get(inst):
                self.bytecode = hex(self.text_dict[inst] | set_reg1(reg1) | set_reg2(op2) | set_reg3("$" + imm))
            else:
                self.bytecode = hex(self.text_dict[inst] | set_reg1(reg1) | set_reg2(op2) | set_imm(imm))
            self.inst = inst[:] + str(reg1) + "," + str(op2) + "," + str(imm)
        else:
            if inst == "mov":
                self.bytecode = hex(self.text_dict[inst] | set_reg1(reg1) | shift_n(check_par(op2),15,2**32))
            else:
                self.bytecode = hex(self.text_dict[inst] | set_reg1(reg1) | shift_n(check_par(op2),16,2**32))
            self.inst = inst[:] + str(reg1) + "," + str(op2)

        self.bin_bytecode = int(self.bytecode,base=16)

class TypeRR(InstType):
    def __init__(self,inst,reg1,reg2,reg3=None):
        self.raw_inst = inst
        if reg3:
            self.raw_inst = inst[:] + str(reg1) + "," + str(reg2) + "," + str(reg3)
        else:
            self.raw_inst = inst[:] + str(reg1) + "," + str(reg2)
            reg3 = "$0"

        self.text_dict = {"or":0x1010000000000000,"and":0x1020000000000000,"xor":0x1030000000000000,"not":0x1040000000000000,"shl":0x1050000000000000,\
                        "shr":0x1060000000000000,"sar":0x1070000000000000,"mov":0x1080000000000000,"movz":0x1090000000000000,"movn":0x10a0000000000000,\
                        "add":0x10b0000000000000,"sub":0x10c0000000000000}
        self.bytecode = str(hex(self.text_dict[inst] | set_reg1(reg1) | set_reg2(reg2) | set_reg3(reg3)))
        self.bin_bytecode = int(self.bytecode,base=16)

def bytecode(inst,op1,op2,op3=None):
    if op3 == None:
        if op2[0] == '$':
            return TypeRR(inst,op1,op2).bytecode
        else:
            return TypeRI(inst,op1,op2).bytecode
    else:
        if op3[0] == '$':
            return TypeRR(inst,op1,op2,op3).bytecode
        else:
            return TypeRI(inst,op1,op2,op3).bytecode
