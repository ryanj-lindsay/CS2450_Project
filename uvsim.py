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
    pass

  #Execution functions based on line input
  def run(self): 
    pass

  def _execute(self, opcode, operand):
    pass
