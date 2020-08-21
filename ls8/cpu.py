"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0    

        # Flag
        self.flag = 0b00000000   

    def load(self, filename = None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if filename:
            with open(sys.argv[1]) as f:
                address = 0
                for line in f:
                    value = line.split("#")[0].strip()
                    if value == "":
                        continue

                    else:
                        instruction = int(line, 2)
                        self.ram[address] = instruction
                        address += 1

        
        else:
            program = [
                # From print8.ls8
                0b10000010,  # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111,  # PRN R0
                0b00000000,
                0b00000001,  # HLT
            ]

        for address, instruction in enumerate(program):
            self.ram[address] = instruction
    
    def ram_read(self, address):
         return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001

            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b10000010

            else:
                self.flag = 0b00000100
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

        #Added for Sprint Challenge
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        ########################

        SP = 7

        running = True

        while running:
            instruction = self.ram[self.pc]

            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            # HLT
            if instruction == HLT:
                running = False
                self.pc += 1
                sys.exit()

            # MUL
            elif instruction == MUL:
                print(self.reg[reg_a] * self.reg[reg_b])
                self.pc += 3

            # PRN
            elif instruction == PRN:
                print(self.reg[reg_a])
                self.pc += 2

            # LDI
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
            
            # CALL
            elif instruction == CALL:
                self.reg[SP] -= 1
                self.ram_write(self.pc + 2, self.reg[SP])
                self.pc = self.reg[reg_a]

            # RET
            elif instruction == RET:
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1

            
            # Added for Sprint Challenge
            
            # CMP
            elif instruction == CMP:
                self.alu("CMP", reg_a, reg_b)
                self.pc += 3

            # JMP
            elif instruction == JMP:
                self.pc == self.reg[reg_a]
                break

            # JEQ
            elif instruction == JEQ:
                if (self.flag & HLT) == 1:
                    self.pc = self.reg[reg_a]

                else:
                    self.pc += 2

            # JNE
            elif instruction == JNE:
                if (self.flag & HLT) == 0:
                    self.pc = self.reg[reg_a]

                else:
                    self.pc += 2
            
            ###############################
                
            else:
                print(f'This instruction is not valid: {hex(instruction)}')
                running = False
                sys.exit()
