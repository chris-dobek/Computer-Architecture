"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0         

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            print("Insufficient arguments, re-evaluate and try again")
            print("Usage: filename file_to_open")

        address = 0

        # For now, we've just hardcoded a program:
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')
                    potential_num = comment_split[0]

                    if potential_num == "":
                        continue

                    if potential_num[0] == "1" or potential_num[0] == "0":
                        num = potential_num[:8]

                        self.ram[address] = int(num, 2)
                        address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")

        #program = [
            # From print8.ls8
            #0b10000010, # LDI R0,8
            #0b00000000,
            #0b00001000,
            #0b01000111, # PRN R0
            #0b00000000,
            #0b00000001, # HLT
        #]
    

        # for instruction in program:
          #  self.ram[address] = instruction
           # address += 1
    
    def ram_read(self, mar):
         return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

        ADD = 0b10100000
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001

        SP = 7

        running = True

        while running:
            instruction = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                running = False
                self.pc += 1
                sys.exit()

            elif instruction == MUL:
                print(self.reg[reg_a] * self.reg[reg_b])
                self.pc += 3

            elif instruction == PRN:
                print(self.reg[reg_a])
                self.pc += 2

            elif instruction == LDI:
                self.reg[reg_a] = reg_b
                self.pc += 3
            
             # PUSH
            elif instruction == PUSH:
                # decrement the stack pointer
                self.reg[SP] -= 1
                # store value from reg to ram
                self.ram_write(self.reg[reg_a], self.reg[SP])
                self.pc += 2

            # POP
            elif instruction == POP:
                # read value of SP and overwrite next register
                value = self.ram_read(self.reg[SP])
                self.reg[reg_a] = value
                # increment SP
                self.reg[SP] += 1
                self.pc += 2

            # ADD
            elif instruction == ADD:
                add = self.reg[reg_a] + self.reg[reg_b]
                self.reg[reg_a] = add
                self.pc += 3
                
            else:
                print(f'this instruction is not valid: {hex(instruction)}')
                running = False
                sys.exit()
