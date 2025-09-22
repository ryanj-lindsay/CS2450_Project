import sys
from uvsim import *

def main():
    if len(sys.argv) < 2:
        print("Too few arguments. Usage: python uvsim.py textfile.txt")
        sys.exit(1)

    file = sys.argv[1]
    with open(file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    sim = UVSim()
    sim.load(lines)

    try: 
        sim.run()
    except (ValueError, IndexError, ZeroDivisionError, RuntimeError) as e:
        print(f"Runtime error: {e}")
        sys.exit(1)
        
    
if __name__ == "__main__":
    main()
