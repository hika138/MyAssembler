#自作CPUのエミュレータ
import os
import sys
# レジスタとメモリ空間の初期化
register = [1, 0, 0, 0] # t, r, a, b
memory = [0] * 64

memory[0] = 10
memory[1] = 15

def main(file: str):
    with open("code.bin", "rb") as f:
        # 8bitずつ読み込む
        while True:
            code = f.read(1)
            if not code:
                break
            opcode_decode(code)
            draw_memory()

def draw_memory():
    global memory
    os.system("cls")
    for i in range(8):
        for j in range(8):
            print(format(memory[i*8+j], "02x"), end=" ")
        if i < 4:
            print(f"r[{i}] {register[i]}", end="")
        print()

def opcode_decode(code: bytes):
    IntCode = int.from_bytes(code, "big")
    opcode = IntCode >> 6
    operand = IntCode & 0b111111
    if (opcode == 0b00):
        nand(operand)
    elif (opcode == 0b01):
        shift(operand)
    elif (opcode == 0b10):
        save(operand)
    elif (opcode == 0b11):
        load(operand)

def nand(operand: bytes):
    global register
    # 2bitずつに分割
    operand0 = operand >> 4 & 0b11
    operand1 = operand >> 2 & 0b11
    operand2 = operand & 0b11
    # 演算
    if operand != 0b00:
        register[operand0] = ~(register[operand1] & register[operand2])

def shift(operand: bytes):
    global register
    # 2bitずつに分割
    operand0 = operand >> 4 & 0b11
    operand1 = operand >> 2 & 0b11
    operand2 = operand & 0b11
    # 演算
    if operand != 0b00:
        register[operand0] = (register[operand1] << register[operand2])

def save(operand: bytes):
    global register
    global memory
    # メモリに格納
    memory[operand] = register[1]

def load(operand: bytes):
    global register
    global memory
    # メモリからロード
    register[1] = memory[operand]
    return

if __name__ == "__main__":
    main(sys.argv[1])