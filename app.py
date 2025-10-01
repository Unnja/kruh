import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Body na kružnici")

# Vstupy od uživatele
x0 = st.number_input("Střed X:", value=0.0)
y0 = st.number_input("Střed Y:", value=0.0)
r = st.number_input("Poloměr:", value=5.0, min_value=0.1)
n = st.number_input("Počet bodů:", value=8, min_value=1)
color = st.color_picker("Barva bodů", "#ff0000")

# Výpočet bodů
angles = np.linspace(0, 2*np.pi, int(n), endpoint=False)
x = x0 + r*np.cos(angles)
y = y0 + r*np.sin(angles)

# Vykreslení
fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.plot(x0, y0, "bo", label="Střed")
ax.scatter(x, y, c=color, label="Body")
circle = plt.Circle((x0, y0), r, fill=False, linestyle="--")
ax.add_patch(circle)
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.legend()
st.pyplot(fig)

# Info o autorovi
with st.expander("O autorovi"):
    st.write("Jméno: Filip Vaja")
    st.write("Kontakt: filip.vaja@vut.cz")
    st.write("Použité technologie: Python, Streamlit, GoogleColab")
