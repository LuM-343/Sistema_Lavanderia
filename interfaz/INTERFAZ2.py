# ============================================================
# SISTEMA DE LAVANDERÍA - JAVE'S LAUNDRY
# Frontend Moderno (Tema Verde Suave)
# Hecho por: WICHO Y ARENZ
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

import modulos.modClientes as modClientes
import modulos.modServicios as modServicios
import modulos.database as database

# ------------------------------------------------------------
# CONFIGURACIÓN DE ESTILO GLOBAL Y COLORES
# ------------------------------------------------------------
COLOR_FONDO = "#f6f9f6"          # Fondo claro verdoso
COLOR_PANEL = "#ffffff"          # Paneles blancos
COLOR_TEXTO = "#1B5E20"          # Verde oscuro para texto
COLOR_PRINCIPAL = "#4CAF50"      # Verde menta principal
COLOR_BOTON_HOVER = "#43A047"    # Verde más oscuro al pasar
COLOR_VOLVER = "#C8E6C9"         # Verde pálido para botones secundarios
COLOR_VOLVER_HOVER = "#A5D6A7"

FUENTE_TITULO = ("Segoe UI", 20, "bold")
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")

# ------------------------------------------------------------
# VENTANA PRINCIPAL
# ------------------------------------------------------------
ventana = tk.Tk()
ventana.title("Sistema de Lavandería - Jave's Laundry")
ventana.config(bg=COLOR_FONDO)
ventana.state('zoomed')

# Crear tablas al iniciar el sistema
try:
    database.crear_tablas()
except Exception as e:
    print("Error al crear tablas:", e)

# ------------------------------------------------------------
# ESTILOS TTK PERSONALIZADOS
# ------------------------------------------------------------
style = ttk.Style()
style.theme_use("clam")

# Frames y etiquetas
style.configure("TFrame", background=COLOR_FONDO)
style.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_NORMAL)
style.configure("TEntry", fieldbackground="white", foreground=COLOR_TEXTO, insertcolor=COLOR_TEXTO)

# Botones principales
style.configure("TButton", background=COLOR_PRINCIPAL, foreground="white",
                font=FUENTE_BOTON, padding=6, relief="flat")
style.map("TButton", background=[("active", COLOR_BOTON_HOVER)])

# Botón de volver
style.configure("Volver.TButton", background=COLOR_VOLVER, foreground=COLOR_TEXTO,
                font=FUENTE_BOTON, padding=6, relief="flat")
style.map("Volver.TButton", background=[("active", COLOR_VOLVER_HOVER)])

# Tabla
style.configure("Treeview", background=COLOR_PANEL, foreground=COLOR_TEXTO,
                fieldbackground=COLOR_PANEL, rowheight=25, font=FUENTE_NORMAL)
style.configure("Treeview.Heading", background=COLOR_PRINCIPAL, foreground="white",
                font=("Segoe UI", 11, "bold"))

# ------------------------------------------------------------
# MÓDULO CLIENTES
# ------------------------------------------------------------
def abrir_clientes():
    ventana.withdraw()
    modClientes.cargarClientes()

    win = tk.Toplevel()
    win.title("Gestión de Clientes - Jave's Laundry")
    win.config(bg=COLOR_FONDO)
    win.state('zoomed')
    win.protocol("WM_DELETE_WINDOW", lambda: [win.destroy(), ventana.deiconify()])

    ttk.Label(win, text="Gestión de Clientes", font=FUENTE_TITULO,
              foreground=COLOR_PRINCIPAL, background=COLOR_FONDO).pack(pady=15)
    marco = ttk.Frame(win)
    marco.pack(pady=10)

    etiquetas = ["Nombre", "Teléfono", "Dirección", "Extra"]
    entradas = []
    for i, texto in enumerate(etiquetas):
        ttk.Label(marco, text=f"{texto}:").grid(row=i, column=0, padx=5, pady=5)
        e = ttk.Entry(marco, width=40)
        e.grid(row=i, column=1)
        entradas.append(e)

    marco_tabla = ttk.Frame(win)
    marco_tabla.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    columnas = ("ID", "Nombre", "Teléfono", "Dirección", "Extra", "Servicios")
    tree = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    def refrescar():
        for item in tree.get_children():
            tree.delete(item)
        for c in modClientes.cargarClientes():
            tree.insert("", "end", values=(c.idCliente, c.nombre, c.telefono,
                                           c.direccion, c.extra, c.servicios))

    def registrar():
        try:
            now = datetime.now()
            idCliente = f"Cli_{now.strftime('%y%m%d_%H%M%S')}"
            cli = modClientes.Cliente(idCliente, entradas[0].get(),
                                      int(entradas[1].get()), entradas[2].get(), entradas[3].get())
            modClientes.insertarCliente(cli)
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.", parent=win)
            for e in entradas:
                e.delete(0, tk.END)
            refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)

    def eliminar():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Seleccione un cliente.", parent=win)
            return

        idCliente, nombre = tree.item(item, "values")[0], tree.item(item, "values")[1]
        try:
            conn = database.conectar()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM servicios WHERE idCliente=?", (idCliente,))
            tiene_servicios = cur.fetchone()[0]
            conn.close()

            if tiene_servicios > 0:
                messagebox.showwarning("No se puede eliminar",
                                       f"El cliente '{nombre}' tiene {tiene_servicios} servicio(s) registrado(s).",
                                       parent=win)
                return

            if messagebox.askyesno("Confirmar eliminación",
                                   f"¿Eliminar al cliente '{nombre}' definitivamente?", parent=win):
                modClientes.eliminarCliente(idCliente)
                messagebox.showinfo("Eliminado", f"Cliente '{nombre}' eliminado correctamente.", parent=win)
                refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)

    marco_botones = ttk.Frame(win)
    marco_botones.pack(pady=10)
    ttk.Button(marco_botones, text="Registrar", command=registrar).grid(row=0, column=0, padx=10)
    ttk.Button(marco_botones, text="Eliminar", command=eliminar).grid(row=0, column=1, padx=10)
    ttk.Button(marco_botones, text="🔄 Refrescar", command=refrescar).grid(row=0, column=2, padx=10)

    ttk.Button(win, text="🏠 Volver al menú principal", width=30,
               style="Volver.TButton", command=lambda: [win.destroy(), ventana.deiconify()]).pack(pady=20)

    refrescar()

# ------------------------------------------------------------
# MÓDULO LAVADAS
# ------------------------------------------------------------
def abrir_lavadas():
    ventana.withdraw()
    modServicios.cargarServicios()
    modClientes.cargarClientes()

    win = tk.Toplevel()
    win.title("Gestión de Lavadas - Jave's Laundry")
    win.config(bg=COLOR_FONDO)
    win.state('zoomed')
    win.protocol("WM_DELETE_WINDOW", lambda: [win.destroy(), ventana.deiconify()])

    ttk.Label(win, text="Gestión de Lavadas", font=FUENTE_TITULO,
              foreground=COLOR_PRINCIPAL, background=COLOR_FONDO).pack(pady=15)

    marco = ttk.Frame(win)
    marco.pack(pady=10)

    ttk.Label(marco, text="Cliente (ID):").grid(row=0, column=0, padx=5, pady=5)
    combo = ttk.Combobox(marco, values=[c.idCliente for c in modClientes.clientes], width=37)
    combo.grid(row=0, column=1)

    ttk.Label(marco, text="Precio (Q):").grid(row=1, column=0, padx=5, pady=5)
    precio = ttk.Entry(marco, width=40)
    precio.grid(row=1, column=1)

    ttk.Label(marco, text="Observaciones:").grid(row=2, column=0, padx=5, pady=5)
    obs = ttk.Entry(marco, width=40)
    obs.grid(row=2, column=1)

    ttk.Label(marco, text="Pago:").grid(row=3, column=0, padx=5, pady=5)
    pago_var = tk.StringVar(value="pendiente")
    combo_pago = ttk.Combobox(marco, textvariable=pago_var,
                              values=["pendiente", "pagado"], width=37, state="readonly")
    combo_pago.grid(row=3, column=1)

    marco_tabla = ttk.Frame(win)
    marco_tabla.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    columnas = ("ID Servicio", "Cliente", "Fecha", "Precio", "Observaciones", "Estado", "Pago")
    tree = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    def refrescar():
        for item in tree.get_children():
            tree.delete(item)
        for s in modServicios.cargarServicios():
            tree.insert("", "end", values=(s.idServicio, s.idCliente,
                                           s.fecha.strftime("%Y-%m-%d"),
                                           s.precio, s.obs, s.estado, s.pago))
        combo["values"] = [c.idCliente for c in modClientes.cargarClientes()]

    def registrar():
        try:
            now = datetime.now()
            idServicio = f"Ser_{now.strftime('%y%m%d_%H%M%S')}"
            if not combo.get():
                messagebox.showwarning("Atención", "Seleccione un cliente.", parent=win)
                return
            s = modServicios.Servicio(idServicio, combo.get(), now,
                                      float(precio.get() or 0), obs.get())
            s.pago = combo_pago.get()
            modServicios.insertarServicio(s)
            messagebox.showinfo("Éxito", "Lavada registrada correctamente.", parent=win)
            precio.delete(0, tk.END)
            obs.delete(0, tk.END)
            combo_pago.set("pendiente")
            refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)

    def eliminar():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Seleccione una lavada.", parent=win)
            return
        idServicio = tree.item(item, "values")[0]
        modServicios.eliminarServicioConPila(idServicio)
        messagebox.showinfo("Eliminado", "Lavada eliminada correctamente.", parent=win)
        refrescar()

    def restaurar():
        modServicios.deshacerEliminacionServicio()
        messagebox.showinfo("Restaurado", "Última lavada restaurada correctamente.", parent=win)
        refrescar()

    def cambiar_estado():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Seleccione una lavada.", parent=win)
            return
        idServicio = tree.item(item, "values")[0]
        nuevo_estado = combo_estado.get()
        if not nuevo_estado:
            messagebox.showwarning("Atención", "Seleccione un nuevo estado.", parent=win)
            return
        modServicios.actualizarServicio(idServicio, estado=nuevo_estado)
        messagebox.showinfo("Estado actualizado", f"El servicio cambió a '{nuevo_estado}'.", parent=win)
        refrescar()

    def cambiar_pago():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Seleccione una lavada.", parent=win)
            return
        idServicio = tree.item(item, "values")[0]
        nuevo_pago = combo_pago_estado.get()
        if not nuevo_pago:
            messagebox.showwarning("Atención", "Seleccione un estado de pago.", parent=win)
            return
        modServicios.actualizarServicio(idServicio, pago=nuevo_pago)
        messagebox.showinfo("Pago actualizado", f"El pago se cambió a '{nuevo_pago}'.", parent=win)
        refrescar()

    def alternar_pago(event):
        item = tree.focus()
        if not item:
            return
        valores = tree.item(item, "values")
        idServicio, pago_actual = valores[0], valores[6]
        nuevo_pago = "pagado" if pago_actual == "pendiente" else "pendiente"
        modServicios.actualizarServicio(idServicio, pago=nuevo_pago)
        refrescar()

    tree.bind("<Double-1>", alternar_pago)

    marco_botones = ttk.Frame(win)
    marco_botones.pack(pady=10)
    ttk.Button(marco_botones, text="Registrar Lavada", command=registrar).grid(row=0, column=0, padx=5)
    ttk.Button(marco_botones, text="🗑 Eliminar", command=eliminar).grid(row=0, column=1, padx=5)
    ttk.Button(marco_botones, text="↩ Restaurar Última", command=restaurar).grid(row=0, column=2, padx=5)
    ttk.Button(marco_botones, text="🔄 Refrescar", command=refrescar).grid(row=0, column=3, padx=5)

    frame_estado = ttk.Frame(win)
    frame_estado.pack(pady=8)
    ttk.Label(frame_estado, text="Nuevo Estado:").grid(row=0, column=0, padx=5)
    combo_estado = ttk.Combobox(frame_estado, values=["Pendiente", "Lavado", "Entregado", "Olvidado"],
                                width=20, state="readonly")
    combo_estado.grid(row=0, column=1, padx=5)
    ttk.Button(frame_estado, text="Cambiar Estado", command=cambiar_estado).grid(row=0, column=2, padx=5)
    ttk.Label(frame_estado, text="Nuevo Pago:").grid(row=0, column=3, padx=5)
    combo_pago_estado = ttk.Combobox(frame_estado, values=["pendiente", "pagado"], width=15, state="readonly")
    combo_pago_estado.grid(row=0, column=4, padx=5)
    ttk.Button(frame_estado, text="Cambiar Pago", command=cambiar_pago).grid(row=0, column=5, padx=5)

    frame_volver = ttk.Frame(win)
    frame_volver.pack(pady=20)
    ttk.Button(frame_volver, text="🏠 Volver al menú principal",
               width=30, style="Volver.TButton",
               command=lambda: [win.destroy(), ventana.deiconify()]).pack()

    refrescar()

# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------
ttk.Label(ventana, text="🌿 Sistema de Lavandería", font=("Segoe UI", 26, "bold"),
          foreground=COLOR_PRINCIPAL, background=COLOR_FONDO).pack(pady=40)

frame_botones = ttk.Frame(ventana)
frame_botones.pack(pady=40)
ttk.Button(frame_botones, text="👤 Clientes", width=25, command=abrir_clientes).grid(row=0, column=0, pady=10, padx=20)
ttk.Button(frame_botones, text="🧴 Lavadas", width=25, command=abrir_lavadas).grid(row=1, column=0, pady=10, padx=20)

ttk.Label(ventana, text="© 2025 - Jave’s Laundry\nHecho por: Wicho y Arenz",
          font=("Segoe UI", 10, "italic"),
          background=COLOR_FONDO, foreground="#2E7D32").pack(side=tk.BOTTOM, pady=20)

ventana.mainloop()