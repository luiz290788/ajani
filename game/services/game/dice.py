import random

AVAILABLE_DICES = [6, 20, 100]

def throw(size):
  if size not in AVAILABLE_DICES:
    raise ValueError("%d is not an available dice." % size)
  
  return random.randint(1, size)