#自作CPUのエミュレータ
import os
import sys
# レジスタとメモリ空間の初期化
register = [1, 0, 0, 0] # t, r, a, b
memory = [0] * 64

def main(file: str):
    input()
    with open(file, "rb") as f:
        # 8bitずつ読み込む
        while True:
            draw_memory()
            code = f.read(1)
            if not code:
                break
            opcode_decode(code)
    input()

def draw_memory():
    global memory
    os.system("cls")
    for i in range(8):
        for j in range(8):
            # メモリ表示
            print(format(memory[i*8+j], "02x"), end=" ")
        if i < 4:
            # レジスタ表示
            print(f"r[{i}] {format(register[i], "02x")}", end="")
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
    if operand0 != 0b00:
        register[operand0] = ~(register[operand1] & register[operand2])
        register[operand0] &= 0b11111111

def shift(operand: bytes):
    global register
    # 2bitずつに分割
    operand0 = operand >> 4 & 0b11
    operand1 = operand >> 2 & 0b11
    operand2 = operand & 0b11
    # 演算
    if operand0 != 0b00:
        register[operand0] = (register[operand1] << register[operand2])
        register[operand0] &= 0b11111111

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