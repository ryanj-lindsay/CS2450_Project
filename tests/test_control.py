import pytest
from uvsim import *

def test_branch():
  sim = UVSim()
  sim.memory[0] = 77
  sim.load([4002, 4300, 2000, 4300])
  sim.run()

  assert sim.accumulator == 77

def test_branchneg():
  sim = UVSim()
  sim.memory[0] = -5
  sim.memory[1] = 111
  sim.load([2000, 4104, 4300, 2001, 4300])
  sim.run()

  assert sim.accumulator == 111

def test_branchzero():
  sim = UVSim()
  sim.memory[0] = 0 
  sim.memory[1] = 222
  sim.load([2000, 4204, 4300, 2001, 4300])
  sim.run()

  assert sim.accumulator == 222

def test_halt():
  sim = UVSim()
  sim.memory[0] = 9
  sim.load([2000, 4300, 3000])
  sim.run()

  assert sim.accumulator == 9 
