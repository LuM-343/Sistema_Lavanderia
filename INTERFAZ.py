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
    ventana.withdraw()
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Gestión de Clientes")
    ventana_clientes.state('zoomed')

    ttk.Label(ventana_clientes, text="Registro de Clientes", font=("Arial", 18, "bold")).pack(pady=15)

    marco = ttk.Frame(ventana_clientes)
    marco.pack(pady=10)

    ttk.Label(marco, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    nombre = ttk.Entry(marco, width=40)
    nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(marco, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5)
    telefono = ttk.Entry(marco, width=40)
    telefono.grid(row=1, column=1, padx=5, pady=5)

    def registrar():
        if not nombre.get() or not telefono.get():
            messagebox.showwarning("Atención", "Complete todos los campos.")
            return
        tree.insert("", "end", values=(nombre.get(), telefono.get()))
        messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
        nombre.delete(0, tk.END)
        telefono.delete(0, tk.END)

    ttk.Button(marco, text="Registrar", command=registrar).grid(row=2, columnspan=2, pady=10)

    tree = ttk.Treeview(ventana_clientes, columns=("Nombre", "Teléfono"), show="headings", height=15)
    tree.heading("Nombre", text="Nombre")
    tree.heading("Teléfono", text="Teléfono")
    tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    def volver():
        ventana_clientes.destroy()
        ventana.deiconify()

    ttk.Button(ventana_clientes, text="⬅ Volver al menú principal", command=volver).pack(pady=15)

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