import sys

def main(input_file: str, output_file: str):
    with open(input_file, "r", encoding='UTF-8') as p:
        program = p.readlines()
        convert = bytearray()
        # Convert the program to binary
        for line in program:
            code = line.split()
            instuction = opcode_convert(code)
            convert.append(instuction)

    with open(output_file, "wb") as c:
        c.write(convert)

def opcode_convert(code: str):
    opcode = 0b0
    # Convert the opcode to binary
    try:
        if code[0] == "nand":
            opcode += 0b00
            opcode = opcode << 6
            opcode += operand_convert(code)

        elif code[0] == "shift":
            opcode += 0b01
            opcode = opcode << 6
            opcode += operand_convert(code)

        elif code[0] == "save":
            opcode += 0b10
            opcode = opcode << 6
            opcode += int(code[1])

        elif code[0] == "load":
            opcode += 0b11
            opcode = opcode << 6
            opcode += int(code[1])
        
        elif code[0] == "#":
            pass
        else:
            print("Invalid instruction")
    except:
        pass
    return opcode

def operand_convert(code: str):
    operand = 0b0
    for i in range(1, 4):
        operand = operand << 2
        try :
            code[i]
        except:
            print("No operand")
            return operand

    # Convert the operand to binary
        if code[i] == "t":
            operand += 0b00
        elif code[i] == "r":
            operand += 0b01
        elif code[i] == "a":
            operand += 0b10
        elif code[i] == "b":
            operand += 0b11
        else:
            print("Invalid operand")
            break
    return operand
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
