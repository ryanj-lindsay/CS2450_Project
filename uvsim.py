memory = [0] * 100
math_memory = 0
instructions_counter = 0
working = False


# this part of the sim is to read what is in the txt file
def read(txtfile):
    global memory
    print(f"Reading program instructions from {txtfile}")
    try:
        with open(txtfile, 'r') as file:
            position = 0
            for line in file:
                line = line.strip()
                if line == "":
                    continue

                try:
                    number = int(line.replace("+", ""))
                    memory[position] = number
                    position += 1
                except ValueError:
                    print("Error: File command written wrong")
                    return False

        print(f"Loaded {position} instructions")
        return True

    except FileNotFoundError:
        print("Could not find file")
        return False


# this section is to clean up the look of the numbers to match what is expected
def clean_numbers(num):
    if num >= 0:
        return f"+{num:04d}"   
    else:
        return f"{num:05d}"   


def user_input(location):
    global memory

    print("Enter number: ", end="")
    input_from_user = input()

    try:
        number = int(input_from_user)
        if -9999 <= number <= 9999:
            memory[location] = number
            print(f"Stored {clean_numbers(number)} in memory[{location:02d}]")
            return True
        else:
            print("Error number must be between limits -9999 and +9999")
            return False
    except ValueError:
        print("Error: enter a valid number")
        return False



def output(location):
    global memory
    number = memory[location]
    print(f"Output: {clean_numbers(number)}")


def load_math_memory(location):
    global math_memory, memory
    math_memory = memory[location]
    print(f"Loaded {math_memory} into math memory")

def store_math_memory(location):
    global math_memory, memory
    memory[location] = math_memory
    print(f"Stored {math_memory} into memory[{location:02d}]")


# Operations that were are going to use for the sim

def math_memory_add(location):
    global math_memory, memory
    original_num = math_memory
    math_memory = math_memory + memory[location]
    print(f"Numbers Added: {original_num} + {memory[location]} = {math_memory}")

def math_memory_compare(location):
    global math_memory, memory
    original_num = math_memory
    math_memory = math_memory - memory[location]
    print(f"The bigger number is: {original_num} - {memory[location]} = {math_memory}")


