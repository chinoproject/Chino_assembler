class IntRangeError(Exception):
    def __init__(self):
        self.str = "输入的数大于%s(2**64-1)" % hex(2**64-1)
    def __str__(self):
        return self.str

class InstBin:
    #format example:63-52_51-47_46-42_41-10
    def __init__(self,inst,format="63-52_51-47_46-42_41-10"):
        if type(inst) == str:
            if inst[:2] == "0b":
                self.inst = int(inst,base=2)
            elif inst[:2] == "0x":
                self.inst = int(inst,base=16)
            else:
                self.inst = int(inst)
                #raise TypeError("输入的类型不为16进制，二进制或十进制")
        elif type(inst) == int:
            self.inst = inst
        else:
            raise TypeError("输入的类型不为16进制，二进制或十进制")

        if self.inst > 2**64 - 1:
            raise IntRangeError

        self.hex = hex(self.inst)
        if len(bin(self.inst)[2:]) < 64:
            self.bin = "0" * (64 - len(bin(self.inst)[2:])) + bin(self.inst)[2:]
        else:
            self.bin = bin(self.inst)

        self.reverse_bin = self.bin[::-1]

        self.format_bin = ""
        if format == None:
            for i in range(64):
                if (i + 1) % 4 == 0:
                    self.format_bin += self.bin[i] + "_"
                else:
                    self.format_bin += self.bin[i]
            self.format_bin = self.format_bin[0:-1]
        else:
            split_list = format.split("_")
            save_bits = []
            for i in split_list:
                if len(save_bits):
                    #计算分割点
                    save_bits.append(save_bits[-1] + eval(i) + 1)
                else:  
                    save_bits.append(eval(i))
            save_bits.append(65)    #防止抛出IndexError
            i = 0
            for j in range(64):
                if j == save_bits[i]:
                    self.format_bin += self.bin[j] + "_"
                    i += 1
                else:
                    self.format_bin += self.bin[j]

        
    def __str__(self):
        return "hex:" + self.hex + "\n" + "bin:" + self.format_bin + "\n" + "raw bin:" + self.bin

    def __getitem__(self,i):
        s = slice(i.stop,i.start + 1)
        return self.reverse_bin[s][::-1]

    def __or__(self,i):
        return InstBin(self.inst | i.inst)
    def __and__(self,i):
        return InstBin(self.inst & i.inst)
    def __xor__(self,i):
        return InstBin(self.inst ^ i.inst)
    def __invert__(self):
        return InstBin((~self.inst) & (2**64-1))

def tips():
    help()
    print("运算仅支持位运算")
def help():
    print("现支持的指令:")
    print("new")
    print("calc")
    print("show")
    print("list")
    print("exit")
    print("help")

def new():
    name = input("name=")
    inst = input("value=")
    format = input("format(default 63-52_51-47_46-42_41-10)=")
    if format == '':
        format="63-52_51-47_46-42_41-10"
    return name,InstBin(inst,format)
def calc():
    global var_list
    while True:
        x = input("calc?>")
        if x == "exit":
            return
        else:
            try:
                print(eval(x,var_list))
            except Exception as e:
                print(e)
if  __name__ == "__main__":
    var_list = {}
    tips()
    while True:
        cmd = input("?>").replace(" ","")
        if len(cmd) == 0:
            continue
        if cmd == "help":
            help()
        elif cmd == "new":
            name,inst = new()
            var_list[name] = inst
        elif cmd == "list":
            for i in var_list:
                print(i)
        elif cmd[:4] == "show":
            x = cmd.split(" ")
            print(var_list[x[1]])
        elif cmd == "calc":
            calc()
        elif cmd == "exit":
            exit()
        else:
            print("无效命令")

