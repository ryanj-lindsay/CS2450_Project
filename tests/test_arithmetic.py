import pytest
from uvsim import *

def test_add():
  sim = UVSim()
  sim.memory[0] = 10
  sim.memory[1] = 5
  sim.load([2000, 3001, 4300])
  sim.run()

assert sim.accumulator == 15

def test_subtract():
  sim = UVSim()
  sim.memory[0] = 10
  sim.memory[1] = 5
  sim.load([2000, 3101, 4300])
  sim.run()

  assert sim.accumulator == 5

def test_divide():
  sim = UVSim()
  sim.memory[0] = 12
  sim.memory[1] = 4
  sim.load([2000, 3201, 4300])
  sim.run()

  assert sim.accumulator == 3

def test_divide_by_zero():
  sim = UVSim()
  sim.memory[0] = 12
  sim.memory[1] = 0
  sim.load([2000, 3201, 4300])
  
  with pytest.raises(ZeroDivisionError):
    sim.run()

def test_multiply():
  sim = UVSim()
  sim.memory[0] = 3
  sim.memory[1] = 4
  sim.load([2000, 3301, 4300])
  sim.run()
  
  assert sim.accumulator == 12
