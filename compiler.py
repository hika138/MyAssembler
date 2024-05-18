# 入力ファイルの行を読み込んで、それを解析して、出力ファイルに書き込む。メモリのアドレスを直に触る。
# CPY dst src -> load src, save dst
# NOT(dst, src) -> NAND(dst, src, src)
# AND(dst, src1, src2) -> NAND(dst, src1, src2) + NOT(dst, dst)
# NAND(dst, src1, src2) -> "load src1\nnand a r r\nnand a a a\nload src2\nnand b r r\nnand b b b\nnand r a b\nsave dst\n"
# OR(dst, src1, src2) -> "load src1\nnand a r r\nload src2\nnand b r r\nnand a a b\nsave dst\n"
# NOR(dst, src1, src2) -> OR(dst, src1, src2) + NOT(dst, dst)
# XOR(dst, src1, src2) -> "load src1\nnand a r r\nnand a a a\nload src2\nnand b r r\nnand b b b\nnand r a b\nnand a r r\nnand b r r\nnand r a b\nsave dst\n"
# SET(dst, num) -> 8回シフトしてrを0にする -> シフトしてnumの各ビットを取り出して、1のときにrとtのorを取る -> rをdstに保存
# となるように変換する

import sys

def main(input_file, output_file):
    with open(output_file, "w") as f:
        f.write(Analyze(input_file))
    
# 入力ファイルを解析する
def Analyze(file):
    compile_code = ""
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            code = line.split()
            if code[0] == "cpy":
                compile_code += CPY(code[1], code[2])
            elif code[0] == "not":
                compile_code += NOT(code[1], code[2])
            elif code[0] == "and":
                compile_code += AND(code[1], code[2], code[3])
            elif code[0] == "nand":
                compile_code += NAND(code[1], code[2], code[3])
            elif code[0] == "or":
                compile_code += OR(code[1], code[2], code[3])
            elif code[0] == "nor":
                compile_code += NOR(code[1], code[2], code[3])
            elif code[0] == "xor":
                compile_code += XOR(code[1], code[2], code[3])
            elif code[0] == "set":
                compile_code += SET(code[1], int(code[2]))
            elif code[0] == "#":
                pass
            else:
                print("Invalid instruction")
    return compile_code


def CPY(dst, src):
    return f"load {src}\nsave {dst}\n"

def NOT(operand1, operand2):
    return NAND(operand1, operand2, operand2)

def AND(operand1, operand2, operand3):
    return NAND(operand1, operand2, operand3) + NOT(operand1, operand1)

def NAND(operand1, operand2, operand3):
    return f"load {operand2}\nnand a r r\nnand a a a\nload {operand3}\nnand b r r\nnand b b b\nnand r a b\nsave {operand1}\n"

def OR(operand1, operand2, operand3):
    return f"load {operand2}\nnand a r r\nload {operand3}\nnand b r r\nnand a a b\nsave {operand1}\n"

def NOR(operand1, operand2, operand3):
    return OR(operand1, operand2, operand3) + NOT(operand1, operand1)

def XOR(operand1, operand2, operand3):
    return f"load {operand2}\nnand a r r\nnand a a a\nload {operand3}\nnand b r r\nnand b b b\nnand r a b\nnand a r r\nnand b r r\nnand r a b\nsave {operand1}\n"

def SET(operand1, num: int):
    code = ""
    # aにnot(1)を入れる
    code += f'nand a t t\n'
    # rを0にする
    code += clear('r')

    # numの各ビットを取り出して、1のときにrとtのorを取る
    for i in range(8):
        now_degit = num >> (7-i)
        print(format(now_degit, "08b"), format(now_degit & 0b1, "08b"))
        if (now_degit & 0b1) == 1:
            # rとnot(1)のorをbにいれる
            code += f'nand r r r\nnand b r a\nnand r b b\nnand r r r\n'
        if i < 7:
            code += f'shift r r t\n'
    # rをdstに保存
    code += f'save {operand1}\n'
    return code

def clear(reg:str):
    code = ""
    for i in range(8):
        code += f'shift {reg} {reg} t\n'
    return code

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])