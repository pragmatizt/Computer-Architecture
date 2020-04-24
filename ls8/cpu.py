"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # create 8 registers
        self.reg = [0] * 8
        # Set the program counter to 0
        self.pc = 0
        # Create 256 bits of RAM
        self.ram = [0] * 255

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, # registrar 0
            0b00001000, # value 8
            0b01000111, # PRN R0
            0b00000000, # print value in first registrar
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        """
        Reads the value at the designated address of RAM
        """
        return self.ram[address]
    
    def ram_write(self, address, value):
        """
        Writes a value to RAM at the designated address
        """
        self.ram[address] = value

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
        """Run the CPU."""
        running = True
        while running == True:
            instruction = self.ram[self.pc]

            if instruction == 0b00000001:
                running = False
                self.pc += 1

            elif instruction == 0b10000010:
                reg_slot = self.ram_read(self.pc + 1)

                int_value = self.ram_read(self.pc + 2)

                self.reg[reg_slot] = int_value

                self.pc += 3

            elif instruction == 0b01000111:
                reg_slot = self.ram_read(self.pc + 1)
                print(self.reg[reg_slot])

                self.pc += 2

            else:
                print("Command not recognized")
                print(f"You are currently at Program Counter value: {self.pc}")
                print(f"The command issued was: {self.ram_read(self.pc)}")
                sys.exit(1)