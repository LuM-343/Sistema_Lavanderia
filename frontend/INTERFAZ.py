# ============================================================
# SISTEMA DE LAVANDERÍA - JAVE'S LAUNDRY
# Frontend Moderno (Tema Oscuro Elegante)
# Hecho por: WICHO Y ARENZ
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# ---------------------- MÓDULOS BACKEND ----------------------
import backend.modClientes as modClientes
import backend.modServicios as modServicios
import backend.modIngresosEgresos as modIE
import backend.database as database
import backend.utilidades as utilidades

# ------------------------------------------------------------
# CONFIGURACIÓN DE ESTILO GLOBAL Y COLORES
# ------------------------------------------------------------
COLOR_FONDO = "#1E1E1E"
COLOR_PANEL = "#2B2B2B"
COLOR_TEXTO = "#EAEAEA"
COLOR_PRINCIPAL = "#2196F3"
COLOR_BOTON_HOVER = "#1976D2"
COLOR_VOLVER = "#424242"
COLOR_VOLVER_HOVER = "#616161"

FUENTE_TITULO = ("Segoe UI", 20, "bold")
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")

# ============================================================
# VENTANA PRINCIPAL
# ============================================================
ventana = tk.Tk()
ventana.title("Sistema de Lavandería - Jave's Laundry")
ventana.config(bg=COLOR_FONDO)
ventana.state('zoomed')

# --- Contenedor central expandible ---
frame_central = tk.Frame(ventana, bg=COLOR_FONDO)
frame_central.pack(expand=True)

# --- Encabezado con logotipo y título ---
frame_header = tk.Frame(frame_central, bg=COLOR_FONDO)
frame_header.pack(pady=(0, 10))
try:
    ventana.logo = tk.PhotoImage(file="logotipo.png")
    lbl_logo = tk.Label(frame_header, image=ventana.logo, bg=COLOR_FONDO)
    lbl_logo.pack(pady=(0, 5))
except Exception:
    pass

ttk.Separator(frame_central, orient='horizontal').pack(fill='x', pady=(5, 10))

# ------------------------------------------------------------
# CREACIÓN DE TABLAS
# ------------------------------------------------------------
try:
    database.crear_tablas()
    modIE.crear_tabla()
    print("✅ Tablas creadas correctamente")
except Exception as e:
    print("Error al crear tablas:", e)

# ------------------------------------------------------------
# ESTILOS PERSONALIZADOS
# ------------------------------------------------------------
style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background=COLOR_FONDO)
style.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_NORMAL)
style.configure("TEntry", fieldbackground=COLOR_PANEL, foreground="white", insertcolor="white")
style.configure("TButton", background=COLOR_PRINCIPAL, foreground="white", font=FUENTE_BOTON, padding=6)
style.map("TButton", background=[("active", COLOR_BOTON_HOVER)])
style.configure("Volver.TButton", background=COLOR_VOLVER, foreground="white", font=FUENTE_BOTON, padding=6)
style.map("Volver.TButton", background=[("active", COLOR_VOLVER_HOVER)])
style.configure("Treeview", background=COLOR_PANEL, foreground="white", fieldbackground=COLOR_PANEL, rowheight=25)
style.configure("Treeview.Heading", background=COLOR_PRINCIPAL, foreground="white", font=("Segoe UI", 11, "bold"))

# ------------------------------------------------------------
# FUNCIÓN GENERAL PARA VOLVER
# ------------------------------------------------------------
def volver_menu(win):
    win.destroy()
    ventana.deiconify()

# ============================================================
# MÓDULO CLIENTES
# ============================================================
def abrir_clientes():
    ventana.withdraw()
    modClientes.cargarClientes()

    win = tk.Toplevel()
    win.title("Gestión de Clientes - Jave's Laundry")
    win.config(bg=COLOR_FONDO)
    win.state('zoomed')
    win.protocol("WM_DELETE_WINDOW", lambda: volver_menu(win))

    ttk.Label(win, text="Gestión de Clientes", font=FUENTE_TITULO, foreground=COLOR_PRINCIPAL).pack(pady=15)

    marco = ttk.Frame(win)
    marco.pack(pady=10)
    etiquetas = ["Nombre", "Teléfono", "Dirección", "Extra"]
    entradas = []
    for i, texto in enumerate(etiquetas):
        ttk.Label(marco, text=f"{texto}:").grid(row=i, column=0, padx=5, pady=5, sticky="e")
        e = ttk.Entry(marco, width=40)
        e.grid(row=i, column=1, padx=5, pady=5, sticky="w")
        entradas.append(e)

    marco_busqueda = ttk.Frame(win)
    marco_busqueda.pack(pady=10)
    ttk.Label(marco_busqueda, text="🔎 Buscar cliente:").grid(row=0, column=0, padx=5)
    entrada_buscar = ttk.Entry(marco_busqueda, width=40)
    entrada_buscar.grid(row=0, column=1, padx=5)
    ttk.Button(marco_busqueda, text="Buscar", command=lambda: buscar_cliente()).grid(row=0, column=2, padx=5)
    ttk.Button(marco_busqueda, text="📋 Mostrar todos", command=lambda: [entrada_buscar.delete(0, tk.END), refrescar()]).grid(row=0, column=3, padx=5)

    marco_tabla = ttk.Frame(win)
    marco_tabla.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    columnas = ("ID", "Nombre", "Teléfono", "Dirección", "Extra", "Servicios")
    tree = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    def refrescar():
        for item in tree.get_children():
            tree.delete(item)
        clientes = modClientes.cargarClientes()
        for c in clientes:
            try:
                total_servicios = modServicios.contarServiciosPorCliente(c.idCliente)
            except Exception:
                total_servicios = c.servicios
            tree.insert("", "end", values=(c.idCliente, c.nombre, c.telefono, c.direccion, c.extra, total_servicios))

    # --- FUNCIÓN PARA BUSCAR CLIENTE POR NOMBRE ---
    def buscar_cliente():
        texto = entrada_buscar.get().strip().lower()
        if not texto:
            messagebox.showwarning("Atención", "Ingrese un nombre para buscar.", parent=win)
            return
        coincidencias = utilidades.busquedaSecuencialPorNombre(modClientes.clientes, texto)
        for item in tree.get_children():
            tree.delete(item)
        if coincidencias:
            for c in coincidencias:
                total_servicios = modServicios.contarServiciosPorCliente(c.idCliente)
                tree.insert("", "end", values=(c.idCliente, c.nombre, c.telefono, c.direccion, c.extra, total_servicios))
    
    # --- FUNCIÓN PARA REGISTRAR CLIENTE ---
    def registrar():
        try:
            nombre, telefono, direccion, extra = [e.get().strip() for e in entradas]
            nuevo = modClientes.crearCliente(nombre, telefono, direccion, extra)
            messagebox.showinfo("Éxito", f"Cliente '{nuevo.nombre}' registrado correctamente.", parent=win)
            for e in entradas: e.delete(0, tk.END)
            refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)
    
    # --- FUNCIÓN PARA ELIMINAR CLIENTE ---
    def eliminar():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Seleccione un cliente.", parent=win)
            return

        idCliente = tree.item(item, "values")[0]
        resultado = modClientes.eliminarCliente(idCliente)

        if resultado["estado"] == "no_existe":
            messagebox.showerror("Error", "El cliente no existe en la base de datos.", parent=win)
        elif resultado["estado"] == "bloqueado":
            messagebox.showwarning("No se puede eliminar",
                                f"El cliente '{resultado['nombre']}' tiene servicios registrados.",
                                parent=win)
        elif resultado["estado"] == "ok":
            messagebox.showinfo("Eliminado",
                                f"Cliente '{resultado['nombre']}' eliminado correctamente.",
                                parent=win)
            refrescar()
        else:
            messagebox.showerror("Error", "Ocurrió un error inesperado al eliminar el cliente.", parent=win)

    # --- FUNCIÓN PARA EDITAR CLIENTE ---
    def editar_cliente():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Seleccione un cliente para editar.", parent=win)
            return

        valores = tree.item(item, "values")
        idCliente, nombre, telefono, direccion, extra = valores[:5]

        # Crear ventana emergente
        edit_win = tk.Toplevel(win)
        edit_win.title(f"Editar Cliente - {nombre}")
        edit_win.config(bg=COLOR_FONDO)
        edit_win.geometry("450x350")
        edit_win.resizable(False, False)
        edit_win.grab_set()  # Bloquea la ventana principal mientras se edita

        ttk.Label(edit_win, text="Editar Cliente", font=("Segoe UI", 16, "bold"), foreground=COLOR_PRINCIPAL).pack(pady=10)

        marco_edit = ttk.Frame(edit_win)
        marco_edit.pack(pady=10)

        # Campos editables
        etiquetas = ["Nombre", "Teléfono", "Dirección", "Extra"]
        valores_campos = [nombre, telefono, direccion, extra]
        entradas_edit = []

        for i, texto in enumerate(etiquetas):
            ttk.Label(marco_edit, text=f"{texto}:").grid(row=i, column=0, padx=5, pady=5, sticky="e")
            e = ttk.Entry(marco_edit, width=40)
            e.insert(0, valores_campos[i])
            e.grid(row=i, column=1, padx=5, pady=5)
            entradas_edit.append(e)

        # --- FUNCIÓN DE GUARDADO ---
        def guardar_edicion():
            try:
                nuevo_nombre = entradas_edit[0].get().strip()
                nuevo_tel = entradas_edit[1].get().strip()
                nueva_dir = entradas_edit[2].get().strip()
                nuevo_extra = entradas_edit[3].get().strip()

                if not nuevo_nombre:
                    messagebox.showwarning("Atención", "El nombre no puede estar vacío.", parent=edit_win)
                    return

                # --- Actualizar en BD ---
                modClientes.actualizarCliente(idCliente, nuevo_nombre, nuevo_tel, nueva_dir, nuevo_extra)

                # --- Refrescar listas en memoria ---
                modClientes.cargarClientes()
                modServicios.cargarServicios()

                # --- Refrescar tabla visible ---
                refrescar()

                # --- Confirmación ---
                messagebox.showinfo("Éxito", f"Cliente '{nuevo_nombre}' actualizado correctamente.", parent=edit_win)

                edit_win.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el cliente.\n{e}", parent=edit_win)

        # --- BOTONES DE ACCIÓN ---
        ttk.Button(edit_win, text="💾 Guardar cambios", command=guardar_edicion).pack(pady=10)
        ttk.Button(edit_win, text="❌ Cancelar", style="Volver.TButton", command=edit_win.destroy).pack()

    marco_botones = ttk.Frame(win)
    marco_botones.pack(pady=10)
    ttk.Button(marco_botones, text="Registrar", command=registrar).grid(row=0, column=0, padx=10)
    ttk.Button(marco_botones, text="Editar", command=editar_cliente).grid(row=0, column=1, padx=10)
    ttk.Button(marco_botones, text="Eliminar", command=eliminar).grid(row=0, column=2, padx=10)

    ttk.Button(win, text="🏠 Volver al menú principal", width=30, style="Volver.TButton", command=lambda: volver_menu(win)).pack(pady=20)
    refrescar()

# ============================================================
# MÓDULO LAVADAS
# ============================================================
def abrir_lavadas():
    ventana.withdraw()
    modServicios.cargarServicios()
    modClientes.cargarClientes()

    win = tk.Toplevel()
    win.title("Gestión de Lavadas - Jave's Laundry")
    win.config(bg=COLOR_FONDO)
    win.state('zoomed')
    win.protocol("WM_DELETE_WINDOW", lambda: volver_menu(win))

    ttk.Label(win, text="Gestión de Lavadas", font=FUENTE_TITULO, foreground=COLOR_PRINCIPAL).pack(pady=15)

    # --- FORMULARIO PRINCIPAL ---
    marco = ttk.Frame(win)
    marco.pack(pady=10)

    ttk.Label(marco, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
    entrada_cliente = ttk.Entry(marco, width=40)
    entrada_cliente.grid(row=0, column=1)

    # --- SUGERENCIAS AUTOMÁTICAS (TABLA HASH) ---
    tabla_hash = utilidades.crearTablaHash(modClientes.clientes)
    sugerencias = tk.Listbox(marco, height=2, width=40)
    sugerencias.grid(row=1, column=1, padx=5, sticky="w")

    def actualizar_sugerencias(event):
        texto = entrada_cliente.get().strip()
        sugerencias.delete(0, tk.END)
        if texto:
            resultados = utilidades.buscarHash(tabla_hash, texto)
            for c in resultados:
                sugerencias.insert(tk.END, c.nombre)

    def seleccionar_sugerencia(event):
        seleccion = sugerencias.get(tk.ACTIVE)
        entrada_cliente.delete(0, tk.END)
        entrada_cliente.insert(0, seleccion)
        sugerencias.delete(0, tk.END)

    entrada_cliente.bind("<KeyRelease>", actualizar_sugerencias)
    sugerencias.bind("<Double-Button-1>", seleccionar_sugerencia)

    # --- CAMPOS ADICIONALES ---
    ttk.Label(marco, text="Precio (Q):").grid(row=2, column=0, padx=5, pady=5)
    entrada_precio = ttk.Entry(marco, width=40)
    entrada_precio.grid(row=2, column=1)

    ttk.Label(marco, text="Observaciones:").grid(row=3, column=0, padx=5, pady=5)
    entrada_obs = ttk.Entry(marco, width=40)
    entrada_obs.grid(row=3, column=1)

    ttk.Label(marco, text="Pago:").grid(row=4, column=0, padx=5, pady=5)
    pago_var = tk.StringVar(value="Pendiente")
    combo_pago = ttk.Combobox(marco, textvariable=pago_var, values=["Pendiente", "Pagado"], width=37, state="readonly")
    combo_pago.grid(row=4, column=1)

    marco_busqueda = ttk.Frame(win)
    marco_busqueda.pack(pady=10)
    ttk.Label(marco_busqueda, text="🔎 Buscar cliente:").grid(row=0, column=0, padx=5)
    entrada_buscar = ttk.Entry(marco_busqueda, width=40)
    entrada_buscar.grid(row=0, column=1, padx=5)
    ttk.Button(marco_busqueda, text="Buscar", command=lambda: buscar_cliente()).grid(row=0, column=2, padx=5)
    ttk.Button(marco_busqueda, text="📋 Mostrar todos", command=lambda: [entrada_buscar.delete(0, tk.END), refrescar()]).grid(row=0, column=3, padx=5)

    # --- TABLA DE SERVICIOS ---
    columnas = ("ID Servicio", "Cliente", "Fecha", "Precio", "Observaciones", "Estado", "Pago")
    marco_tabla = ttk.Frame(win)
    marco_tabla.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    def refrescar():
        for item in tree.get_children():
            tree.delete(item)
        for s in modServicios.cargarServicios():
            cliente = next((c.nombre for c in modClientes.clientes if c.idCliente == s.idCliente), "Desconocido")
            tree.insert("", "end", values=(s.idServicio, cliente, s.fecha.strftime("%Y-%m-%d"), s.precio, s.obs, s.estado, s.pago))
    
    # --- FUNCIÓN PARA BUSCAR CLIENTE ---
    def buscar_cliente():
        texto = entrada_buscar.get().strip().lower()
        if not texto:
            messagebox.showwarning("Atención", "Ingrese un nombre para buscar.", parent=win)
            return

        # Sincronizar listas antes de buscar
        modClientes.cargarClientes()
        modServicios.cargarServicios()

        # Buscar servicios con nombre actualizado
        coincidencias = utilidades.busquedaBinariaPorNombreServicio(modServicios.servicios, texto)

        # Refrescar tabla
        for item in tree.get_children():
            tree.delete(item)

        if coincidencias:
            for s in coincidencias:
                cliente = next(
                    (c.nombre for c in modClientes.clientes if c.idCliente == s.idCliente),
                    "Desconocido"
                )
                tree.insert(
                    "",
                    "end",
                    values=(
                        s.idServicio,
                        cliente,
                        s.fecha.strftime("%Y-%m-%d"),
                        s.precio,
                        s.obs,
                        s.estado,
                        s.pago
                    ),
                )
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron lavadas para ese cliente.", parent=win)
    
    # --- FUNCIÓN PARA REGISTRAR LAVADA ---
    def registrar():
        try:
            nombre = entrada_cliente.get().strip()
            if not nombre:
                messagebox.showwarning("Atención", "Ingrese o seleccione un cliente.", parent=win)
                return
            cliente = next((c for c in modClientes.clientes if c.nombre.lower() == nombre.lower()), None)
            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado.", parent=win)
                return
            now = datetime.now()
            idServicio = f"Ser_{now.strftime('%y%m%d_%H%M%S')}"
            s = modServicios.Servicio(idServicio, cliente.idCliente, now, float(entrada_precio.get()), entrada_obs.get())
            s.pago = combo_pago.get()
            modServicios.insertarServicio(s)
            messagebox.showinfo("Éxito", "Lavada registrada correctamente.", parent=win)
            entrada_cliente.delete(0, tk.END)
            entrada_precio.delete(0, tk.END)
            entrada_obs.delete(0, tk.END)
            combo_pago.set("Pendiente")
            refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)

    # --- FUNCIÓN PARA ELIMINAR LAVADA ---
    def eliminar():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Seleccione una lavada.", parent=win)
            return
        idServicio = tree.item(item, "values")[0]
        modServicios.eliminarServicioConPila(idServicio)
        messagebox.showinfo("Eliminado", "Lavada eliminada correctamente.", parent=win)
        refrescar()

    # --- FUNCIÓN PARA RESTAURAR CLIENTE ---
    def restaurar():
        # Confirmación del usuario
        if not messagebox.askyesno("Confirmar restauración", "¿Desea restaurar la última lavada eliminada?", parent=win):
            messagebox.showinfo("Cancelado", "Restauración cancelada por el usuario.", parent=win)
            return

        # Ejecutar restauración
        resultado = modServicios.deshacerEliminacionServicio()

        if resultado == "ok":
            messagebox.showinfo("Restaurado", "Última lavada restaurada correctamente.", parent=win)
            refrescar()
        elif resultado == "vacio":
            messagebox.showwarning("Sin lavadas", "No hay lavadas por restaurar.", parent=win)
        else:
            messagebox.showerror("Error", "Ocurrió un error al intentar restaurar la lavada.", parent=win)


    # --- CAMBIO DE ESTADO Y PAGO ---
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
        messagebox.showinfo("Actualizado", f"Estado cambiado a '{nuevo_estado}'.", parent=win)
        refrescar()

    def cambiar_pago():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atención", "Seleccione una lavada.", parent=win)
            return
        idServicio = tree.item(item, "values")[0]
        nuevo_pago = combo_pago_estado.get()
        if not nuevo_pago:
            messagebox.showwarning("Atención", "Seleccione el estado de pago.", parent=win)
            return
        modServicios.actualizarServicio(idServicio, pago=nuevo_pago)
        messagebox.showinfo("Actualizado", f"Pago cambiado a '{nuevo_pago}'.", parent=win)
        refrescar()

    # --- DOBLE CLIC PARA CAMBIAR PAGO ---
    def alternar_pago(event):
        item = tree.focus()
        if not item:
            return
        valores = tree.item(item, "values")
        idServicio, pago_actual = valores[0], valores[6]
        nuevo_pago = "Pagado" if pago_actual == "Pendiente" else "Pendiente"
        modServicios.actualizarServicio(idServicio, pago=nuevo_pago)
        refrescar()

    tree.bind("<Double-1>", alternar_pago)

    # --- BOTONES PRINCIPALES ---
    marco_botones = ttk.Frame(win)
    marco_botones.pack(pady=10)
    ttk.Button(marco_botones, text="Registrar", command=registrar).grid(row=0, column=0, padx=5)
    ttk.Button(marco_botones, text="Eliminar", command=eliminar).grid(row=0, column=1, padx=5)
    ttk.Button(marco_botones, text="Restaurar Última", command=restaurar).grid(row=0, column=2, padx=5)

    # --- CAMBIO DE ESTADO Y PAGO (SECCIÓN INFERIOR) ---
    frame_estado = ttk.Frame(win)
    frame_estado.pack(pady=8)
    ttk.Label(frame_estado, text="Nuevo Estado:").grid(row=0, column=0, padx=5)
    combo_estado = ttk.Combobox(frame_estado, values=["Pendiente", "Lavado", "Entregado", "Olvidado"], width=20, state="readonly")
    combo_estado.grid(row=0, column=1, padx=5)
    ttk.Button(frame_estado, text="Cambiar Estado", command=cambiar_estado).grid(row=0, column=2, padx=5)
    ttk.Label(frame_estado, text="Nuevo Pago:").grid(row=0, column=3, padx=5)
    combo_pago_estado = ttk.Combobox(frame_estado, values=["Pendiente", "Pagado"], width=15, state="readonly")
    combo_pago_estado.grid(row=0, column=4, padx=5)
    ttk.Button(frame_estado, text="Cambiar Pago", command=cambiar_pago).grid(row=0, column=5, padx=5)

    ttk.Button(win, text="🏠 Volver al menú principal", width=30, style="Volver.TButton", command=lambda: volver_menu(win)).pack(pady=20)

    refrescar()

# ============================================================
# MÓDULOS INGRESOS
# ============================================================
def abrir_ingresos():
    ventana.withdraw()
    modIE.crear_tabla()
    win = tk.Toplevel()
    win.title("Gestión de Ingresos - Jave's Laundry")
    win.config(bg=COLOR_FONDO)
    win.state('zoomed')
    win.protocol("WM_DELETE_WINDOW", lambda: volver_menu(win))

    ttk.Label(win, text="Gestión de Ingresos", font=FUENTE_TITULO, foreground=COLOR_PRINCIPAL).pack(pady=15)

    marco = ttk.Frame(win)
    marco.pack(pady=10)
    ttk.Label(marco, text="Concepto:").grid(row=0, column=0, padx=5, pady=5)
    entrada_c = ttk.Entry(marco, width=40)
    entrada_c.grid(row=0, column=1)
    ttk.Label(marco, text="Total (Q):").grid(row=1, column=0, padx=5, pady=5)
    entrada_t = ttk.Entry(marco, width=40)
    entrada_t.grid(row=1, column=1)

    columnas = ("Concepto", "Ingreso (Q)", "Fecha")
    marco_tabla = ttk.Frame(win)
    marco_tabla.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    tree = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=200)
    tree.pack(fill=tk.BOTH, expand=True)

    def refrescar():
        for i in tree.get_children(): tree.delete(i)
        for r in modIE.cargarRegistros():
            if r[2] > 0:
                fecha = r[4] if len(r) > 4 else datetime.now().strftime("%Y-%m-%d %H:%M")
                tree.insert("", "end", values=(r[1], r[2], fecha))

    def registrar():
        try:
            modIE.registrarIngreso(entrada_c.get(), float(entrada_t.get()))
            messagebox.showinfo("Éxito", "Ingreso registrado correctamente.", parent=win)
            entrada_c.delete(0, tk.END); entrada_t.delete(0, tk.END)
            refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)

    marco_botones = ttk.Frame(win)
    marco_botones.pack(pady=10)
    ttk.Button(marco_botones, text="Registrar", command=registrar).grid(row=0, column=0, padx=5)
    ttk.Button(marco_botones, text="Refrescar", command=refrescar).grid(row=0, column=1, padx=5)

    ttk.Button(win, text="🏠 Volver al menú principal", width=30, style="Volver.TButton", command=lambda: volver_menu(win)).pack(pady=20)
    refrescar()

# ============================================================
# MÓDULOS EGRESOS
# ============================================================
def abrir_egresos():
    ventana.withdraw()
    win = tk.Toplevel()
    win.title("Gestión de Egresos - Jave's Laundry")
    win.config(bg=COLOR_FONDO)
    win.state('zoomed')
    win.protocol("WM_DELETE_WINDOW", lambda: volver_menu(win))

    ttk.Label(win, text="Gestión de Egresos", font=FUENTE_TITULO, foreground="#E53935").pack(pady=15)

    marco = ttk.Frame(win)
    marco.pack(pady=10)
    ttk.Label(marco, text="Concepto:").grid(row=0, column=0, padx=5, pady=5)
    entrada_c = ttk.Entry(marco, width=40)
    entrada_c.grid(row=0, column=1)
    ttk.Label(marco, text="Total (Q):").grid(row=1, column=0, padx=5, pady=5)
    entrada_t = ttk.Entry(marco, width=40)
    entrada_t.grid(row=1, column=1)

    columnas = ("Concepto", "Egreso (Q)", "Fecha")
    marco_tabla = ttk.Frame(win)
    marco_tabla.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    tree = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=200)
    tree.pack(fill=tk.BOTH, expand=True)

    def refrescar():
        for i in tree.get_children(): tree.delete(i)
        for r in modIE.cargarRegistros():
            if r[3] > 0:
                fecha = r[4] if len(r) > 4 else datetime.now().strftime("%Y-%m-%d %H:%M")
                tree.insert("", "end", values=(r[1], r[3], fecha))

    def registrar():
        try:
            modIE.registrarEgreso(entrada_c.get(), float(entrada_t.get()))
            messagebox.showinfo("Éxito", "Egreso registrado correctamente.", parent=win)
            entrada_c.delete(0, tk.END); entrada_t.delete(0, tk.END)
            refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=win)

    marco_botones = ttk.Frame(win)
    marco_botones.pack(pady=10)
    ttk.Button(marco_botones, text="Registrar", command=registrar).grid(row=0, column=0, padx=5)
    ttk.Button(marco_botones, text="Refrescar", command=refrescar).grid(row=0, column=1, padx=5)

    ttk.Button(win, text="🏠 Volver al menú principal", width=30, style="Volver.TButton", command=lambda: volver_menu(win)).pack(pady=20)
    refrescar()

# ============================================================
# MENÚ PRINCIPAL
# ============================================================
lbl_titulo = tk.Label(frame_header, text="🧺  Sistema de Lavandería", font=("Segoe UI", 26, "bold"), fg=COLOR_PRINCIPAL, bg=COLOR_FONDO)
lbl_titulo.pack()

frame_botones = ttk.Frame(frame_central)
frame_botones.pack(pady=30)
ttk.Button(frame_botones, text="👤 Clientes", width=25, command=abrir_clientes).grid(row=0, column=0, pady=10, padx=20)
ttk.Button(frame_botones, text="🧴 Lavadas", width=25, command=abrir_lavadas).grid(row=1, column=0, pady=10, padx=20)
ttk.Button(frame_botones, text="💰 Ingresos", width=25, command=abrir_ingresos).grid(row=2, column=0, pady=10, padx=20)
ttk.Button(frame_botones, text="💸 Egresos", width=25, command=abrir_egresos).grid(row=3, column=0, pady=10, padx=20)

ttk.Label(ventana, text="© 2025 - Jave’s Laundry\nHecho por: Wicho y Arenz", font=("Segoe UI", 10, "italic"), background=COLOR_FONDO, foreground="#9E9E9E").pack(side=tk.BOTTOM, pady=15)

ventana.mainloop()