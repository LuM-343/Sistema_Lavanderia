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
    ventana.withdraw()
    ventana_lavadas = tk.Toplevel()
    ventana_lavadas.title("Registro de Lavadas")
    ventana_lavadas.state('zoomed')

    ttk.Label(ventana_lavadas, text="Registro de Lavadas", font=("Arial", 18, "bold")).pack(pady=15)

    marco = ttk.Frame(ventana_lavadas)
    marco.pack(pady=10)

    ttk.Label(marco, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
    cliente = ttk.Entry(marco, width=40)
    cliente.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(marco, text="Tipo de lavada:").grid(row=1, column=0, padx=5, pady=5)
    tipo = ttk.Combobox(marco, values=["Normal", "Rápida", "Especial"], width=37)
    tipo.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(marco, text="Costo (Q):").grid(row=2, column=0, padx=5, pady=5)
    costo = ttk.Entry(marco, width=40)
    costo.grid(row=2, column=1, padx=5, pady=5)

    def registrar():
        if not cliente.get() or not tipo.get() or not costo.get():
            messagebox.showwarning("Atención", "Complete todos los campos.")
            return
        tree.insert("", "end", values=(cliente.get(), tipo.get(), costo.get()))
        messagebox.showinfo("Éxito", "Lavada registrada correctamente.")
        cliente.delete(0, tk.END)
        tipo.set("")
        costo.delete(0, tk.END)

    ttk.Button(marco, text="Registrar", command=registrar).grid(row=3, columnspan=2, pady=10)

    tree = ttk.Treeview(ventana_lavadas, columns=("Cliente", "Tipo", "Costo"), show="headings", height=15)
    tree.heading("Cliente", text="Cliente")
    tree.heading("Tipo", text="Tipo de Lavada")
    tree.heading("Costo", text="Costo (Q)")
    tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    def volver():
        ventana_lavadas.destroy()
        ventana.deiconify()

    ttk.Button(ventana_lavadas, text="⬅ Volver al menú principal", command=volver).pack(pady=15)

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