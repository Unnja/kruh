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

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

# Funkce pro uložení grafu do PDF
def save_pdf(x0, y0, r, n, color, fig):
    buffer = BytesIO()
    
    # nejdříve uložíme matplotlib figuru jako obrázek
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # vytvoření PDF
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica", 12)
    
    # Parametry úlohy
    c.drawString(50, height-50, f"Autor: Jan Novák")
    c.drawString(50, height-70, f"Kontakt: jan.novak@univerzita.cz")
    c.drawString(50, height-90, f"Střed: ({x0}, {y0})")
    c.drawString(50, height-110, f"Poloměr: {r}")
    c.drawString(50, height-130, f"Počet bodů: {n}")
    c.drawString(50, height-150, f"Barva bodů: {color}")
    
    # Vložíme obrázek grafu
    c.drawImage(img_buffer, 50, height-450, width=500, height=300)  
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer

# Tlačítko pro stažení PDF
pdf_buffer = save_pdf(x0, y0, r, n, color, fig)
st.download_button(
    label="Stáhnout PDF",
    data=pdf_buffer,
    file_name="kruh.pdf",
    mime="application/pdf"
)
