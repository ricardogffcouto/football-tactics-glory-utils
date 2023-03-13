import streamlit as st
import utils.streamlit as st_utils
import random

def probs(a, b, c=1):
    prob = 0
    for i in range(500000):
        for j in range(c):
            x = random.randint(1, a)
            y = random.randint(1, b)
            if x >= y:
                prob += 1
                break
    return round(prob / 10000, 1)

st_utils('Probability Calculator')

    print("Calculate probability")
    a = int(input("Your action:"))
    b = int(input("Def. action:"))
    c = input("Times?:")
    if c == "":
        c = 1
    else:
        c = int(c)
    print(probs(a, b, c))
