import re

class UVSim:
    
    #Class initialization
    def __init__(self, input_function = None, output_function = None):
        self.memory = [0] * 100
        self.accumulator = 0
        self.instruction_pointer = 0
        self.running = False
        self.input_function = input_function or self._default_input
        self.output_function = output_function or self._default_output

    #Memory helper functions
    def set_memory(self, address, value):
        if not (0 <= address < 100):
            raise IndexError(f"Invalid memory address: {address}")
        if not (-9999 <= value <= 9999):
            raise ValueError("Value out of range (-9999 - 9999)")
      
        self.memory[address] = value

    def get_memory(self, address):
        if not (0 <= address < 100):
            raise IndexError(f"Invalid memory address: {address}")
      
        return self.memory[address]
        
    #Method for truncating
    @staticmethod
    def _truncate_to_word(value):
        sign = -1 if value < 0 else 1
        low4 = abs(int(value)) % 10000
        return sign * low4

    #Default input/output functions
    def _default_input(self):
        while True:
            try:
                value = int(input("Enter a word (-9999 - 9999): "))
                if -9999 <= value <= 9999:
                    return value
                print("Out of range. Please try again.")

            except ValueError:
                print("Invalid input. Input must be an integer.")

    def _default_output(self, value):
        print(value)

    #Program loading function    
    def load(self, lines):
        self.memory = [0] * 100
        self.accumulator = 0
        self.instruction_pointer = 0
        for i, raw in enumerate(lines):
            if i >= 100:
                raise IndexError("Input too large.")
            if isinstance(raw, str):
                s = raw.strip()
                if s == "":
                    value = 0
                else:
                    m = re.fullmatch(r'([+-])?(\d{1,4})', s)
                    if not m:
                        raise ValueError(
                            f"Malformed word at input line {i+1}: '{raw.strip()}'. "
                            "Expected optional sign and 1–4 digits (e.g. +1234 or 0123)."
                        )
                    sign, digits = m.groups()
                    num = int(digits)
                    if sign == '-':
                        num = -num
                    value = num
            elif isinstance(raw, int):
                value = raw
            else:
                raise TypeError(f"Unsupported line type at index {i}: {type(raw).__name__}")
            self.set_memory(i, value)

    #Execution functions based on line input
    def run(self): 
        self.running = True
        while self.running:
            instruction = self.get_memory(self.instruction_pointer)
            opcode, operand = divmod(instruction, 100)
            self._execute(opcode, operand)

    def _execute(self, opcode, operand):
        #READ
        if opcode == 10:
            value = self.input_function()
            self.set_memory(operand, value)
        #WRITE
        elif opcode == 11:
            value = self.get_memory(operand)
            self.output_function(value)
        #LOAD
        elif opcode == 20:
            if not (0 <= operand < 100):
                raise IndexError(f"Invalid memory access: {operand}")
            self.accumulator = self.get_memory(operand)
            self.instruction_pointer += 1
        #STORE
        elif opcode == 21:
            self.set_memory(operand, self.accumulator)
            self.instruction_pointer += 1
        #ADD
        elif opcode == 30:
            self.accumulator = self._truncate_to_word(self.accumulator + self.get_memory(operand))
            self.instruction_pointer += 1
        #SUBTRACT
        elif opcode == 31:
            self.accumulator = self._truncate_to_word(self.accumulator - self.get_memory(operand))
            self.instruction_pointer += 1
        #DIVIDE
        elif opcode == 32:
            if self.get_memory(operand) == 0:
                raise ZeroDivisionError("Division by zero.")
            self.accumulator = self._truncate_to_word(self.accumulator // self.get_memory(operand))
            self.instruction_pointer += 1
        #MULTIPLY
        elif opcode == 33:
            self.accumulator = self._truncate_to_word(self.accumulator * self.get_memory(operand))
            self.instruction_pointer += 1
        #BRANCH
        elif opcode == 40:
            self.instruction_pointer = operand
            return
        #BRANCHNEG
        elif opcode == 41:
            if self.accumulator < 0:
                self.instruction_pointer = operand
                return
        #BRANCHZERO
        elif opcode == 42:
            if self.accumulator == 0:
                self.instruction_pointer = operand
                return
        #HALT
        elif opcode == 43:
            self.running = False
            return
        #Every other opcode not listed
        else:
            raise RuntimeError(f"Invalid opcode: {opcode}")
