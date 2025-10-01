import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile

# -----------------------
# Registrace lokálního fontu pro PDF
# -----------------------
pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))  # soubor musí být v repozitáři

# -----------------------
# Nadpis
# -----------------------
st.title("Body na kružnici")

# -----------------------
# Vstupy od uživatele
# -----------------------
x0 = st.number_input("Střed X:", value=0.0)
y0 = st.number_input("Střed Y:", value=0.0)
r = st.number_input("Poloměr:", value=5.0, min_value=0.1)
n = st.number_input("Počet bodů:", value=8, min_value=1)
color = st.color_picker("Barva bodů", "#ff0000")

# -----------------------
# Výpočet bodů
# -----------------------
angles = np.linspace(0, 2*np.pi, int(n), endpoint=False)
x = x0 + r*np.cos(angles)
y = y0 + r*np.sin(angles)

# -----------------------
# Vykreslení
# -----------------------
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

# -----------------------
# Info o autorovi
# -----------------------
with st.expander("O autorovi"):
    st.write("Jméno: Filip Vaja")
    st.write("Kontakt: filip.vaja@vut.cz")
    st.write("Použité technologie: Python, Streamlit, GoogleColab, Matplotlib")

# -----------------------
# Funkce pro export PDF
# -----------------------
def save_pdf(x0, y0, r, n, color, fig):
    # dočasný PNG soubor pro graf
    tmpfile = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig.savefig(tmpfile.name, format='PNG')
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("DejaVu", 12)  # české znaky
    
    # Parametry úlohy
    c.drawString(50, height-50, "Autor: Filip Vaja")
    c.drawString(50, height-70, "Kontakt: filip.vaja@vut.cz")
    c.drawString(50, height-90, f"Střed: ({x0}, {y0})")
    c.drawString(50, height-110, f"Poloměr: {r}")
    c.drawString(50, height-130, f"Počet bodů: {n}")
    c.drawString(50, height-150, f"Barva bodů: {color}")
    
    # vložení obrázku grafu
    img = ImageReader(tmpfile.name)
    c.drawImage(img, 50, height-450, width=500, height=300)
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# -----------------------
# Tlačítko pro stažení PDF
# -----------------------
pdf_buffer = save_pdf(x0, y0, r, n, color, fig)
st.download_button(
    label="Stáhnout PDF",
    data=pdf_buffer,
    file_name="kruh.pdf",
    mime="application/pdf"
)
