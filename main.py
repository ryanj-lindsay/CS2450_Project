def main():
    
    memory = [0] * 100
    memory[0] = 1009   # read from memory[09]
    memory[1] = 1109   # WRITE memory[09]. This is not techinically needed and is just for visualization
    memory[9] = 20     # DATA = 20
    memory[2] = 1010   # read from input
    memory[3] = 1110   # WRITE to memory[10]. This is not techinically needed and is just for visualization
    memory[10] = 0     # DATA = 30
    memory[4] = 2009    # LOAD from memory[9]
    memory[5] = 3010    # ADD memory[10]
    memory[6] = 2111    # STORE to memory[11]
    memory[7] = 1111    # WRITE memory[11]. This is needed to show the result
    memory[8] = 4300    # HALT
    
    
    pc = 0  # program counter
    accumulator = 0
    running = True

    while running:
        instruction = memory[pc]
        opcode = instruction // 100   # first 2 digits
        address = instruction % 100   # last 2 digits

        if opcode == 10:   # READ
            memory[address] = int(input("Enter a number: "))
        elif opcode == 11: # WRITE
            print(memory[address])
        elif opcode == 20: # LOAD
            accumulator = memory[address]
        elif opcode == 21: # STORE
            memory[address] = accumulator
        elif opcode == 30: # ADD
            accumulator += memory[address]
        elif opcode == 31: # SUBTRACT
            accumulator -= memory[address]
        elif opcode == 43: # HALT
            running = False
        else:
            print("Unknown opcode!")
            running = False

        pc += 1   # move to next instruction (unless changed by BRANCH)
    
    
if __name__ == "__main__":
    main()