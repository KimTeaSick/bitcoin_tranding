import string
import random

def make_salt():
  digits = string.digits
  alpabat = string.ascii_letters
  letters_set = alpabat + digits
  random_list = random.sample(letters_set,15)
  result = ''.join(random_list)
  print(result)
  return result