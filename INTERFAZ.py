# ============================================================
# Hecho por: 
# - LUIS VELÁSQUEZ - 1502325
# - ARENZ PELÁEZ - 1556425
# ============================================================

# Importación de módulo de librería de TKINTER
import tkinter as tk
from tkinter import ttk, messagebox # ttk = widgets modernos, messagebox = alertas y confirmaciones

# ============================================================
# FUNCIONES GENERALES
# ============================================================

# ---------- Ventana: Clientes ----------
def abrir_clientes():
    ventana.withdraw() # Oculta la ventana principal mientras se abre la nueva
    ventana_clientes = tk.Toplevel() # Crea una nueva ventana secundaria (hija)
    ventana_clientes.title("Gestión de Clientes")
    ventana_clientes.state('zoomed') # Maximiza automáticamente la ventana

    # ---------- Título principal ----------
    ttk.Label(ventana_clientes, text="Registro de Clientes", font=("Arial", 18, "bold")).pack(pady=15)

    # ---------- Marco para agrupar campos ----------
    marco = ttk.Frame(ventana_clientes)
    marco.pack(pady=10)

    # ---------- Campos de formulario ----------
    ttk.Label(marco, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    nombre = ttk.Entry(marco, width=40)
    nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(marco, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5)
    telefono = ttk.Entry(marco, width=40)
    telefono.grid(row=1, column=1, padx=5, pady=5)

    # ---------- Función interna para registrar cliente ----------
    def registrar():
        # Validación: los campos no deben estar vacíos
        if not nombre.get() or not telefono.get():
            messagebox.showwarning("Atención", "Complete todos los campos.")
            return
        
        # Inserta los datos en la tabla Treeview
        tree.insert("", "end", values=(nombre.get(), telefono.get()))
        messagebox.showinfo("Éxito", "Cliente registrado correctamente.")

        # Limpia los campos después del registro
        nombre.delete(0, tk.END)
        telefono.delete(0, tk.END)

    # ---------- Botón de registro ----------
    ttk.Button(marco, text="Registrar", command=registrar).grid(row=2, columnspan=2, pady=10)

    # ---------- Tabla (Treeview) para mostrar los clientes ----------
    tree = ttk.Treeview(ventana_clientes, columns=("Nombre", "Teléfono"), show="headings", height=15)
    tree.heading("Nombre", text="Nombre")
    tree.heading("Teléfono", text="Teléfono")
    tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # ---------- Botón para volver al menú principal ----------
    def volver():
        ventana_clientes.destroy() # Cierra esta ventana
        ventana.deiconify() # Muestra nuevamente la ventana principal

    ttk.Button(ventana_clientes, text="⬅ Volver al menú principal", command=volver).pack(pady=15)

# ---------- Ventana: Lavadas ----------
def abrir_lavadas():
    ventana.withdraw() # Oculta el menú principal
    ventana_lavadas = tk.Toplevel()
    ventana_lavadas.title("Registro de Lavadas")
    ventana_lavadas.state('zoomed') # Se maximiza automáticamente

    # ---------- Título principal ----------
    ttk.Label(ventana_lavadas, text="Registro de Lavadas", font=("Arial", 18, "bold")).pack(pady=15)

    # ---------- Marco principal ----------
    marco = ttk.Frame(ventana_lavadas)
    marco.pack(pady=10)

    # ---------- Campos de formulario ----------
    ttk.Label(marco, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
    cliente = ttk.Entry(marco, width=40)
    cliente.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(marco, text="Tipo de lavada:").grid(row=1, column=0, padx=5, pady=5)
    tipo = ttk.Combobox(marco, values=["Normal", "Rápida", "Especial"], width=37)
    tipo.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(marco, text="Costo (Q):").grid(row=2, column=0, padx=5, pady=5)
    costo = ttk.Entry(marco, width=40)
    costo.grid(row=2, column=1, padx=5, pady=5)

    # ---------- Función para registrar lavada ----------
    def registrar():
        # Verifica que todos los campos estén llenos
        if not cliente.get() or not tipo.get() or not costo.get():
            messagebox.showwarning("Atención", "Complete todos los campos.")
            return
        
        # Inserta los datos en la tabla Treeview
        tree.insert("", "end", values=(cliente.get(), tipo.get(), costo.get()))
        messagebox.showinfo("Éxito", "Lavada registrada correctamente.")

        # Limpia los campos después de registrar
        cliente.delete(0, tk.END)
        tipo.set("")
        costo.delete(0, tk.END)

    # ---------- Botón de registro ----------
    ttk.Button(marco, text="Registrar", command=registrar).grid(row=3, columnspan=2, pady=10)

    # ---------- Tabla (Treeview) ----------
    tree = ttk.Treeview(ventana_lavadas, columns=("Cliente", "Tipo", "Costo"), show="headings", height=15)
    tree.heading("Cliente", text="Cliente")
    tree.heading("Tipo", text="Tipo de Lavada")
    tree.heading("Costo", text="Costo (Q)")
    tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

     # ---------- Botón para volver al menú principal ----------
    def volver():
        ventana_lavadas.destroy()
        ventana.deiconify()

    ttk.Button(ventana_lavadas, text="⬅ Volver al menú principal", command=volver).pack(pady=15)

# ============================================================
# VENTANA PRINCIPAL DEL SISTEMA
# ============================================================

ventana = tk.Tk() # Crea la ventana principal del sistema
ventana.title("Sistema de Lavandería")
ventana.state('zoomed') # Se abre maximizada automáticamente

# ---------- Título principal ----------
ttk.Label(ventana, text="Sistema de Lavandería", font=("Arial", 22, "bold")).pack(pady=30)

# ---------- Marco para los botones del menú ----------
marco_botones = ttk.Frame(ventana)
marco_botones.pack(pady=40)

# Cada tupla contiene el texto del botón y la función asociada
botones = [
    ("👤 Clientes", abrir_clientes),
    ("🧺 Lavadas", abrir_lavadas),
    ("💰 Ingresos", lambda: messagebox.showinfo("Ingresos", "Módulo en construcción.")),
    ("📉 Egresos", lambda: messagebox.showinfo("Egresos", "Módulo en construcción.")),
    ("📊 Reportes", lambda: messagebox.showinfo("Reportes", "Módulo en construcción.")),
]

# ---------- Creación dinámica de botones ----------
for texto, comando in botones:
    ttk.Button(marco_botones, text=texto, command=comando, width=25).pack(pady=10)

# ---------- Pie de página ----------
ttk.Label(
    ventana,
    text="© 2025 - Jave's Laundry\nHecho por: Wicho y Arenz",
    font=("Arial", 10, "italic"),
    anchor='center', # Centra el texto dentro del Label
    justify='center' # Centra si hay saltos de línea
).pack(side=tk.BOTTOM, pady=20, expand=True, fill='x')

# ---------- Bucle principal (mantiene la ventana abierta) ----------
ventana.mainloop()