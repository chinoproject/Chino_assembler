
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
    return shift_n(check_par(reg[1:]),38,32)

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
    def __init__(self,inst,reg1,reg2,imm):
        self.raw_inst = inst
        self.inst = inst[:] + "ri " + str(reg1) + "," + str(reg2) + "," + str(imm)
        self.text_dict = {"or":0x2010000000000000}
        self.bytecode = str(hex(self.text_dict[inst] | set_reg1(reg1) | set_reg2(reg2) | set_imm(imm)))
        self.bin_bytecode = int(self.bytecode,base=16)

class TypeRR(InstType):
    def __init__(self,inst,reg1,reg2,reg3):
        self.raw_inst = inst
        self.raw_inst = inst[:] + "rr" + str(reg1) + "," + str(reg2) + "," + str(reg3)
        self.text_dict = {"or":0x1010000000000000}
        self.bytecode = str(hex(self.text_dict[inst] | set_reg1(reg1) | set_reg2(reg2) | set_reg3(reg3)))
        self.bin_bytecode = int(self.bytecode,base=16)

