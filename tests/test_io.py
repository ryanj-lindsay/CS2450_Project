import pytest
from uvsim import *

def load_file(file):
  with open(f"tests/{file}", "r") as f:
    return [line.strip() for line in f if line.strip()]

def test_read_test1():
    inputs = [5, 7]
    outputs = []
    sim = UVSim(input_function = lambda: inputs.pop(0), output_function = lambda x: outputs.append(x))
    program = load_file("Test1.txt")
    sim.load(program)
    sim.run()
  
    assert sim.memory[7] == 5
    assert sim.memory[8] == 7

def test_write_test1():
    inputs = [5, 7]
    outputs = []
    sim = UVSim(input_function = lambda: inputs.pop(0), output_function = lambda x: outputs.append(x))
    program = load_file("Test1.txt")
    sim.load(program)
    sim.run()
  
    assert outputs[-1] == sim.memory[9]

def test_read_test2():
    inputs = [9, 3]
    outputs = []
    sim = UVSim(input_function = lambda: inputs.pop(0), output_function = lambda x: outputs.append(x))
    program = load_file("Test2.txt")
    sim.load(program)
    sim.run()
  
    assert sim.memory[9] == 9
    assert sim.memory[10] == 3

def test_write_test2():
    inputs = [9, 3]
    outputs = []
    sim = UVSim(input_function = lambda: inputs.pop(0), output_function = lambda x: outputs.append(x))
    program = load_file("Test2.txt")
    sim.load(program)
    sim.run()
  
    assert outputs[0] == sim.memory[9]
    assert outputs[1] == sim.memory[10]
