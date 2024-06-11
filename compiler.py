# 入力ファイルの行を読み込んで、それを解析して、出力ファイルに書き込む。メモリのアドレスを直に触る。
import sys

variable = [""] * 64
malloc = [False] * 64

def main(input_file, output_file):
    with open(output_file, "w") as f:
        compiled_code = Analyze(input_file)
        f.write(compiled_code)
    
# 入力ファイルを解析する
def Analyze(file):
    compile_code = ""
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == "#":
                continue
            code = line.split()
            for i in range(len(code) - 1):
                if code[i+1].isdecimal() & (code[0] != "set"):
                    temp = code[i+1]
                    code[i+1] = f"imme{i}"
                    VAR(code[i+1])
                    compile_code += SET(search_var(code[i+1]), temp)
            try:
                if code[0] == "cpy":
                    code[1] = search_var(code[1])
                    code[2] = search_var(code[2])
                    compile_code += CPY(code[1], code[2])
                elif code[0] == "not":
                    code[1] = search_var(code[1])
                    code[2] = search_var(code[2])
                    compile_code += NOT(code[1], code[2])
                elif code[0] == "and":
                    code[1] = search_var(code[1])
                    code[2] = search_var(code[2])
                    code[3] = search_var(code[3])
                    compile_code += AND(code[1], code[2], code[3])
                elif code[0] == "nand":
                    code[1] = search_var(code[1])
                    code[2] = search_var(code[2])
                    code[3] = search_var(code[3])
                    compile_code += NAND(code[1], code[2], code[3])
                elif code[0] == "or":
                    code[1] = search_var(code[1])
                    code[2] = search_var(code[2])
                    code[3] = search_var(code[3])
                    compile_code += OR(code[1], code[2], code[3])
                elif code[0] == "nor":
                    code[1] = search_var(code[1])
                    code[2] = search_var(code[2])
                    code[3] = search_var(code[3])
                    compile_code += NOR(code[1], code[2], code[3])
                elif code[0] == "xor":
                    code[1] = search_var(code[1])
                    code[2] = search_var(code[2])
                    code[3] = search_var(code[3])
                    compile_code += XOR(code[1], code[2], code[3])
                elif code[0] == "set":
                    code[1] = search_var(code[1])
                    compile_code += SET(code[1], code[2])
                elif code[0] == "var":
                    VAR(code[1])
                elif code[0] == "shift":
                    code[1] = search_var(code[1])
                    code[2] = search_var(code[2])
                    compile_code += SHIFT(code[1], code[2])
                elif code[0] == "add":
                    code[1] = search_var(code[1])
                    code[2] = search_var(code[2])
                    code[3] = search_var(code[3])
                    code[4] = search_var(code[4])

                    compile_code += ADD(code[1], code[2], code[3], code[4])
                elif code[0] == "free":
                    clear(search_var(code[1]))
                    free(code[1])
                else:
                    print("Invalid instruction")
            except:
                pass
            for i in range(len(code) - 1):
                var = search_var(f"imme{i}")
                if var != None:
                    compile_code += SET(var, "0")
                    free(f"imme{i}")
    return compile_code

# 変数をコピー
def CPY(dst:str, src:str):
    return f"load {src}\nsave {dst}\n"

# NOT演算
def NOT(operand1:str, operand2:str):
    return NAND(operand1, operand2, operand2)

# AND演算
def AND(operand1:str, operand2:str, operand3:str):
    return NAND(operand1, operand2, operand3) + NOT(operand1, operand1)

# NAND演算
def NAND(operand1:str, operand2:str, operand3:str):
    return f"load {operand2}\nnand a r r\nnand a a a\nload {operand3}\nnand b r r\nnand b b b\nnand r a b\nsave {operand1}\n"

# OR演算
def OR(operand1:str, operand2:str, operand3:str):
    return f"load {operand2}\nnand a r r\nload {operand3}\nnand b r r\nnand a a b\nsave {operand1}\n"

# NOR演算
def NOR(operand1:str, operand2:str, operand3:str):
    return OR(operand1, operand2, operand3) + NOT(operand1, operand1)

# XOR演算
def XOR(operand1:str, operand2:str, operand3:str):
    return f"load {operand2}\nnand a r r\nnand a a a\nload {operand3}\nnand b r r\nnand b b b\nnand r a b\nnand a r a\nnand b r b\nnand r a b\nsave {operand1}\n"

# operand2をoperand3ビットシフト
def SHIFT(operand1:str, operand2:str):
    code = ""
    code += f"load {operand2}\n"
    code += f"shift r r t\n"
    code += f"save {operand1}\n"
    return code

# 8bitの加算器
def ADD(sum:str, carry:str, operand3:str, operand4:str):
    code = ""
    code += XOR(sum, operand3, operand4)
    code += AND(carry, operand3, operand4)
    code += SHIFT(carry, carry)
    VAR("temp") # 一時変数
    code += CPY(search_var("temp"), sum)
    for i in range(7):
        code += XOR(search_var("temp"), search_var("temp"), carry)
        code += AND(carry, sum, carry)
        code += CPY(sum, search_var("temp"))
        code += SHIFT(carry, carry)
    code += SET(search_var("temp"), 0)
    free("temp")
    return code

# numをdstにセット
def SET(operand1:str, num: str):
    num = int(num)
    code = ""
    # aにnot(1)を入れる
    code += f'nand a t t\n'
    # rを0にする
    code += clear('r')

    # numの各ビットを取り出して、1のときにrとtのorを取る
    for i in range(8):
        now_degit = num >> (7-i)
        if (now_degit & 0b1) == 1:
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
        ValueError("Variable already exists")

# 変数ののメモリ空間上の位置を検索
def search_var(operand:str):
    global variable
    for i in range(64):
        if operand == variable[i]:
            return str(i)
    ValueError("Variable not found")

# 変数を解放
def free(var:str):
    global variable
    global malloc
    for i in range(len(variable)):
        if var == variable[i]:
            malloc[i] = False
            variable[i] = ""
            return
    ValueError("Variable not found")

# レジスタをクリアする
def clear(reg:str):
    code = ""
    code += "nand r r t\nnand r r r\nshift r r t\nnand r r t\nnand r r r\n"
    return code

if __name__ == "__main__":
        # 出力ファイル名が指定されていない場合は、入力ファイル名の拡張子を.tcpに変更
    if len(sys.argv) == 2:
        main(sys.argv[1], sys.argv[1].replace(".tby", ".tcp"))
    else:
        main(sys.argv[1], sys.argv[2])