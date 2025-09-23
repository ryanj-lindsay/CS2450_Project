import pytest
from uvsim import *

def test_load():
  sim = UVSim()
  sim.memory[0] = 123
  sim.load([2000, 4300])
  sim.run()

  assert sim.accumulator == 123

def test_store():
  sim = UVSim()
  sim.accumulator = 456
  sim.load([2101, 4300])
  sim.run()

  assert sim.memory[1] == 456
