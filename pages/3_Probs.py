import streamlit as st
import utils.streamlit as st_utils
import random

def probs(a, b, c=1):
    prob = 0
    times_run = 100000
    for i in range(times_run):
        for j in range(c):
            x = random.randint(1, a)
            y = random.randint(1, b)
            if x >= y:
                prob += 1
                break
    st.write(f"### {round(prob * 100 / times_run, 1)} % success")

class RNGType:
    NORMAL: str = "Normal"
    REALISTIC: str = "Realistic (30%)"

st_utils.header('Probability Calculator')
st.selectbox("RNG Type", [RNGType.NORMAL, RNGType.REALISTIC])
active = st.number_input("Active action", min_value=1, max_value=None)
passive = st.number_input("Passive action", min_value=1, max_value=None)
times = st.selectbox("Times", [1, 2, 3])
st.button("Calculate probability", on_click=probs, args=(active, passive, times))
