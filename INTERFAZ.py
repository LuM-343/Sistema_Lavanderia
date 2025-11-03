# ============================================================
# Hecho por: 
# - LUIS VELÁSQUEZ - 1502325
# - ARENZ PELÁEZ - 1556425
# ============================================================

# Importación de módulo de librería de TKINTER
import tkinter as tk
from tkinter import ttk, messagebox  # ttk = widgets modernos, messagebox = alertas y confirmaciones

# ============================================================
# VENTANA PRINCIPAL DEL SISTEMA
# ============================================================

ventana = tk.Tk()
ventana.title("Sistema de Lavandería")
ventana.state('zoomed')
ventana.resizable(True, True)

ttk.Label(ventana, text="Sistema de Lavandería", font=("Arial", 22, "bold")).pack(pady=30)

ventana.mainloop()