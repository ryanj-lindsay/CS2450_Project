import re

class UVSim:
    def __init__(self, input_function=None, output_function=None):
        self.MAX_MEM = 250
        self.memory = [0] * self.MAX_MEM
        self.accumulator = 0
        self.instruction_pointer = 0
        self.running = False
        self.input_function = input_function or self._default_input
        self.output_function = output_function or self._default_output
        self.format = None  # 4 or 6 (digits)

    def _max_word(self):
        return 9999 if self.format == 4 else 999999

    def _truncate_to_word(self, value):
        sign = -1 if value < 0 else 1
        mag = abs(int(value))
        if self.format == 4:
            low = mag % 10000
        else:
            low = mag % 1000000
        return sign * low

    def set_memory(self, address, value):
        if not (0 <= address < self.MAX_MEM):
            raise IndexError(f"Invalid memory address: {address}")
        limit = self._max_word()
        if not (-limit <= value <= limit):
            raise ValueError(f"Value out of range (-{limit} - {limit})")
        self.memory[address] = int(value)

    def get_memory(self, address):
        if not (0 <= address < self.MAX_MEM):
            raise IndexError(f"Invalid memory address: {address}")
        return self.memory[address]

    def _default_input(self):
        while True:
            try:
                raw = int(input("Enter a word: "))
                limit = self._max_word()
                if -limit <= raw <= limit:
                    return raw
                print(f"Out of range. Enter between {-limit} and {limit}.")
            except ValueError:
                print("Invalid input. Integer required.")

    def _default_output(self, value):
        print(value)

    def load(self, lines):
        self.memory = [0] * self.MAX_MEM
        self.accumulator = 0
        self.instruction_pointer = 0
        fmt = None
        for i, raw in enumerate(lines):
            if i >= self.MAX_MEM:
                raise IndexError(f"Input too large. Max {self.MAX_MEM} lines allowed.")
            if isinstance(raw, str):
                s = raw.strip()
                if s == "":
                    value = 0
                    # leave fmt unchanged by blank lines
                else:
                    if re.fullmatch(r'[+-]?\d{6}', s):
                        f = 6
                    elif re.fullmatch(r'[+-]?\d{1,4}', s):
                        f = 4
                    else:
                        raise ValueError(f"Malformed word at input line {i+1}: '{s}'")
                    if fmt is None:
                        fmt = f
                    elif fmt != f:
                        raise ValueError("Mixed 4-digit and 6-digit words in same file.")
                    value = int(s)
            elif isinstance(raw, int):
                value = raw
            else:
                raise TypeError(f"Unsupported line type at index {i}: {type(raw).__name__}")

            # set detected format before enforcing per-line limits
            if fmt is not None:
                self.format = fmt

            # enforce per-format bounds when loading numeric instruction/values
            if self.format == 4:
                if not (-9999 <= value <= 9999):
                    raise ValueError(f"Value out of 4-digit range at line {i+1}: {value}")
            elif self.format == 6:
                if not (-999999 <= value <= 999999):
                    raise ValueError(f"Value out of 6-digit range at line {i+1}: {value}")

            self.set_memory(i, value)

        if self.format is None:
            # empty file default to new (6-digit) format for behavior consistency
            self.format = 6

    def run(self):
        self.running = True
        while self.running:
            instruction = self.get_memory(self.instruction_pointer)
            instr_abs = abs(int(instruction))
            if self.format == 4:
                opcode = instr_abs // 100
                operand = instr_abs % 100
                if not (0 <= operand <= 99):
                    raise IndexError(f"Invalid operand address {operand} for 4-digit program.")
            else:
                opcode = instr_abs // 1000
                operand = instr_abs % 1000
                if not (0 <= operand <= 249):
                    raise IndexError(f"Invalid operand address {operand} for 6-digit program (must be 000-249).")

            self._execute(opcode, operand)

    def _execute(self, opcode, operand):
        if opcode == 10:  # READ
            value = self.input_function()
            self.set_memory(operand, int(value))
            self.instruction_pointer += 1
        elif opcode == 11:  # WRITE
            value = self.get_memory(operand)
            self.output_function(value)
            self.instruction_pointer += 1
        elif opcode == 20:  # LOAD
            if not (0 <= operand < self.MAX_MEM):
                raise IndexError(f"Invalid memory access: {operand}")
            self.accumulator = self.get_memory(operand)
            self.instruction_pointer += 1
        elif opcode == 21:  # STORE
            self.set_memory(operand, self.accumulator)
            self.instruction_pointer += 1
        elif opcode == 30:  # ADD
            res = self.accumulator + self.get_memory(operand)
            self.accumulator = self._truncate_to_word(res)
            self.instruction_pointer += 1
        elif opcode == 31:  # SUBTRACT
            res = self.accumulator - self.get_memory(operand)
            self.accumulator = self._truncate_to_word(res)
            self.instruction_pointer += 1
        elif opcode == 32:  # DIVIDE
            denom = self.get_memory(operand)
            if denom == 0:
                raise ZeroDivisionError("Division by zero.")
            res = self.accumulator // denom
            self.accumulator = self._truncate_to_word(res)
            self.instruction_pointer += 1
        elif opcode == 33:  # MULTIPLY
            res = self.accumulator * self.get_memory(operand)
            self.accumulator = self._truncate_to_word(res)
            self.instruction_pointer += 1
        elif opcode == 40:  # BRANCH
            self.instruction_pointer = operand
            return
        elif opcode == 41:  # BRANCHNEG
            if self.accumulator < 0:
                self.instruction_pointer = operand
            else:
                self.instruction_pointer += 1
            return
        elif opcode == 42:  # BRANCHZERO
            if self.accumulator == 0:
                self.instruction_pointer = operand
            else:
                self.instruction_pointer += 1
            return
        elif opcode == 43:  # HALT
            self.running = False
            return
        else:
            raise RuntimeError(f"Invalid opcode: {opcode}")

def convert_4_to_6(lines):
    valid_opcodes = set(range(10, 44))
    out = []
    for raw in lines:
        s = str(raw).strip()
        if s == "":
            out.append("000000")
            continue
        sign = "-" if s.startswith("-") else ""
        core = s.lstrip("+-")
        if not core.isdigit() or not (1 <= len(core) <= 4):
            raise ValueError(f"Not a valid 4-digit token: '{s}'")
        core4 = core.zfill(4)
        first_two = int(core4[:2])
        if first_two in valid_opcodes:
            opcode = f"{first_two:03d}"
            operand = int(core4[2:])
            out.append(f"{sign}{opcode}{operand:03d}")
        else:
            num = int(core)
            out.append(f"{sign}{num:06d}")
    return out