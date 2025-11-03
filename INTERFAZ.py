# ============================================================
# Hecho por: 
# - LUIS VELÁSQUEZ - 1502325
# - ARENZ PELÁEZ - 1556425
# ============================================================

# Importación de módulo de librería de TKINTER
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Funciones vacías de ejemplo ----------
def abrir_clientes():
    messagebox.showinfo("Clientes", "Módulo en construcción.")

def abrir_lavadas():
    messagebox.showinfo("Lavadas", "Módulo en construcción.")

# ---------- Ventana principal ----------
ventana = tk.Tk()
ventana.title("Sistema de Lavandería")
ventana.state('zoomed')

ttk.Label(ventana, text="Sistema de Lavandería", font=("Arial", 22, "bold")).pack(pady=30)

marco_botones = ttk.Frame(ventana)
marco_botones.pack(pady=40)

botones = [
    ("👤 Clientes", abrir_clientes),
    ("🧺 Lavadas", abrir_lavadas),
    ("💰 Ingresos", lambda: messagebox.showinfo("Ingresos", "Módulo en construcción.")),
    ("📉 Egresos", lambda: messagebox.showinfo("Egresos", "Módulo en construcción.")),
    ("📊 Reportes", lambda: messagebox.showinfo("Reportes", "Módulo en construcción.")),
]

for texto, comando in botones:
    ttk.Button(marco_botones, text=texto, command=comando, width=25).pack(pady=10)

ventana.mainloop()
