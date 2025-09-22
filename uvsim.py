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
      raise ValueError("Value out of range (-9999..9999)")
      
    self.memory[address] = value

  def get_memory(self, address):
    if not (0 <= address < 100):
      raise IndexError(f"Invalid memory address: {address}")
      
    return self.memory[address]

  #Default input/output functions
  def _default_input(self):
    while True:
      value = int(input("Enter a word (-9999..9999): "))
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

    for i, line in enumerate(lines):
      if i >= 100:
        raise IndexError("Input too large for memory.")
      if isinstance(line, str):
        line = int(line)
      self.set_memory(i, line)

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
      pass
    #LOAD
    elif opcode == 20:
      pass
    #STORE
    elif opcode == 21:
      pass
    #ADD
    elif opcode == 30:
      pass
    #SUBTRACT
    elif opcode == 31:
      pass
    #DIVIDE
    elif opcode == 32:
      pass
    #MULTIPLY
    elif opcode == 33:
      pass
    #BRANCH
    elif opcode == 40:
      pass
    #BRANCHNEG
    elif opcode == 41:
      pass
    #BRANCHZERO
    elif opcode == 42:
      pass
    #HALT
    elif opcode == 43:
      pass
    #Every other opcode not listed
    else:
      raise RuntimeError(f"Invalid opcode: {opcode}")

    self.instruction_pointer += 1
