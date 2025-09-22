import pytest
from uvsim import *

def load_file(file):
  with open(f"tests/{file}", "r") as f:
    return [line.strip() for line in f if line.strip()]

def test_read():
  inputs = [5, 7]
  outputs = []
  sim = UVSim(input_function = lambda: inputs.pop(0), output_function = lambda x: outputs.append(x))
  program = load_file("Test1.txt")
  sim.load(program)
  sim.run()

  assert sim.memory[7] == 5
  assert sim.memory[8] == 7

def test_write():
  inputs = [5, 7]
  outputs = []
  sim = UVSim(input_function = lambda: inputs.pop(0), output_function = lambda x: outputs.append(x))
  program = load_file("Test1.txt")
  sim.load(program)
  sim.run()

  assert outputs[-1] == sim.memory[9]
