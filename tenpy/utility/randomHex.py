import random as rand

def random_hex():
    string = "#"
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
    for i in range(6):
        string += str(rand.choice(digits))
    return string