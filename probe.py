from collections import Counter
from pprint import pprint
from pickle import load


with open('area.pkl', mode='rb') as f:
    ar = load(f)
pprint(ar)
