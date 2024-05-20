# 入力ファイルの行を読み込んで、それを解析して、出力ファイルに書き込む。メモリのアドレスを直に触る。
import sys

variable = [""] * 64
malloc = [False] * 64

def main(input_file, output_file):
    with open(output_file, "w") as f:
        f.write(Analyze(input_file))
    
# 入力ファイルを解析する
def Analyze(file):
    compile_code = ""
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            code = line.split()
            try:
                if code[0] == "cpy":
                    code[1] = check_var(code[1])
                    code[2] = check_var(code[2])
                    compile_code += CPY(code[1], code[2])
                elif code[0] == "not":
                    code[1] = check_var(code[1])
                    code[2] = check_var(code[2])
                    compile_code += NOT(code[1], code[2])
                elif code[0] == "and":
                    code[1] = check_var(code[1])
                    code[2] = check_var(code[2])
                    code[3] = check_var(code[3])
                    compile_code += AND(code[1], code[2], code[3])
                elif code[0] == "nand":
                    code[1] = check_var(code[1])
                    code[2] = check_var(code[2])
                    code[3] = check_var(code[3])
                    compile_code += NAND(code[1], code[2], code[3])
                elif code[0] == "or":
                    code[1] = check_var(code[1])
                    code[2] = check_var(code[2])
                    code[3] = check_var(code[3])
                    compile_code += OR(code[1], code[2], code[3])
                elif code[0] == "nor":
                    code[1] = check_var(code[1])
                    code[2] = check_var(code[2])
                    code[3] = check_var(code[3])
                    compile_code += NOR(code[1], code[2], code[3])
                elif code[0] == "xor":
                    code[1] = check_var(code[1])
                    code[2] = check_var(code[2])
                    code[3] = check_var(code[3])
                    compile_code += XOR(code[1], code[2], code[3])
                elif code[0] == "set":
                    code[1] = check_var(code[1])
                    compile_code += SET(code[1], int(code[2]))
                elif code[0] == "var":
                    VAR(code[1])
                elif code[0] == "shift":
                    code[1] = check_var(code[1])
                    code[2] = check_var(code[2])
                    compile_code += SHIFT(code[1], int(code[2]))
                elif code[0] == "add":
                    code[1] = check_var(code[1])
                    code[2] = check_var(code[2])
                    code[3] = check_var(code[3])
                    code[4] = check_var(code[4])
                    compile_code += ADD(code[1], code[2], code[3], code[4])
                elif code[0] == "#":
                    pass
                else:
                    print("Invalid instruction")
            except:
                pass
    return compile_code


def CPY(dst:str, src:str):
    
    return f"load {src}\nsave {dst}\n"

def NOT(operand1:str, operand2:str):
    return NAND(operand1, operand2, operand2)

def AND(operand1:str, operand2:str, operand3:str):
    return NAND(operand1, operand2, operand3) + NOT(operand1, operand1)

def NAND(operand1:str, operand2:str, operand3:str):
    return f"load {operand2}\nnand a r r\nnand a a a\nload {operand3}\nnand b r r\nnand b b b\nnand r a b\nsave {operand1}\n"

def OR(operand1:str, operand2:str, operand3:str):
    return f"load {operand2}\nnand a r r\nload {operand3}\nnand b r r\nnand a a b\nsave {operand1}\n"

def NOR(operand1:str, operand2:str, operand3:str):
    return OR(operand1, operand2, operand3) + NOT(operand1, operand1)

def XOR(operand1:str, operand2:str, operand3:str):
    return f"load {operand2}\nnand a r r\nnand a a a\nload {operand3}\nnand b r r\nnand b b b\nnand r a b\nnand a r a\nnand b r b\nnand r a b\nsave {operand1}\n"

def SHIFT(operand1:str, operand2:str, operand3:int):
    code = ""
    code += f"load {operand2}\n"
    for i in range(int(operand3)):
        code += f"shift r r t\n"
    code += f"save {operand1}\n"
    return code

def ADD(sum:str, carry:str, operand3:str, operand4:str):
    code = ""
    code += XOR(sum, operand3, operand4)
    code += AND(carry, operand3, operand4)
    code += SHIFT(carry, carry, 1)
    VAR("temp") # 一時変数
    code += CPY(check_var("temp"), sum)
    for i in range(7):
        code += XOR(check_var("temp"), check_var("temp"), carry)
        code += AND(carry, sum, carry)
        code += CPY(sum, check_var("temp"))
        code += SHIFT(carry, carry, 1)
    code += SET(check_var("temp"), 0)
    free("temp")

    return code

def SET(operand1:str, num_str: str):
    num = int(num_str)
    code = ""
    # aにnot(1)を入れる
    code += f'nand a t t\n'
    # rを0にする
    code += clear('r')

    # numの各ビットを取り出して、1のときにrとtのorを取る
    for i in range(8):
        now_degit = num >> (7-i)
        if (now_degit & 0b1) == 1:
            # rとnot(1)のorをbにいれる
            code += f'nand r r r\nnand b r a\nnand r b b\nnand r r r\n'
        if i < 7:
            code += f'shift r r t\n'
    # rをdstに保存
    code += f'save {operand1}\n'
    return code

# 変数を保存
def VAR(operand:str):
    global variable
    global malloc
    if operand not in variable:
        for exist in range(64):
            if malloc[exist] == False:
                malloc[exist] = True
                variable[exist] = operand
                break
    else:
        print("Variable already exists")

def check_var(operand:str):
    global variable
    for i in range(64):
        if operand == variable[i]:
            return str(i)
    print("Variable not found")

def free(operand:str):
    global variable
    global malloc
    for i in range(len(variable)):
        if operand == variable[i]:
            malloc[i] = False
            variable[i] = ""
            return
    print("Variable not found")

def clear(reg:str):
    code = ""
    for i in range(8):
        code += f'shift {reg} {reg} t\n'
    return code

if __name__ == "__main__":
        # 出力ファイル名が指定されていない場合は、入力ファイル名の拡張子を.tcpに変更
    if len(sys.argv) == 2:
        main(sys.argv[1], sys.argv[1].replace(".tby", ".tcp"))
    else:
        main(sys.argv[1], sys.argv[2])