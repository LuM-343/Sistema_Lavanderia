import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os

DB_PATH = "lavanderia.db"

#Ingresar a la base de datos
def conectar():
    return sqlite3.connect(DB_PATH)

#Generar reportes escritos del ultimo mes

def reporteLavadas(periodo="mes"):
    conn = conectar()
    cur = conn.cursor()
    fecha_limite = datetime.now() - timedelta(days=7 if periodo == "semana" else 30)
    cur.execute("""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN estado='Pendiente' THEN 1 ELSE 0 END),
            SUM(CASE WHEN estado='Lavado' THEN 1 ELSE 0 END),
            SUM(CASE WHEN estado='Entregado' THEN 1 ELSE 0 END),
            SUM(CASE WHEN estado='Olvidado' THEN 1 ELSE 0 END)
        FROM servicios
        WHERE fecha >= ?
    """, (fecha_limite.strftime("%Y-%m-%d %H:%M:%S"),))
    data = cur.fetchone()
    conn.close()
    total, pend, lav, ent, olv = data
    return f"""
Reporte de Lavadas ({'última semana' if periodo == 'semana' else 'último mes'}):
- Total registradas: {total or 0}
- Pendientes: {pend or 0}
- En Lavado: {lav or 0}
- Entregadas: {ent or 0}
- Olvidadas: {olv or 0}
"""

def reporteClientes(periodo="mes"):
    conn = conectar()
    cur = conn.cursor()
    fecha_limite = datetime.now() - timedelta(days=7 if periodo == "semana" else 30)
    cur.execute("""
        SELECT COUNT(DISTINCT idCliente),
               SUM(precio)
        FROM servicios
        WHERE fecha >= ? AND pago='pagado'
    """, (fecha_limite.strftime("%Y-%m-%d %H:%M:%S"),))
    data = cur.fetchone()
    conn.close()
    clientes, total = data
    return f"""
👤 Reporte de Clientes ({'última semana' if periodo == 'semana' else 'último mes'}):
- Clientes atendidos: {clientes or 0}
- Total facturado: Q{total or 0:.2f}
"""

def reporteIngresos(periodo="mes"):
    conn = conectar()
    cur = conn.cursor()
    fecha_limite = datetime.now() - timedelta(days=7 if periodo == "semana" else 30)
    try:
        cur.execute("""
            SELECT 
                SUM(ingreso),
                SUM(egreso),
                SUM(ingreso) - SUM(egreso)
            FROM ingresosYegresos
            WHERE fecha >= ?
        """, (fecha_limite.strftime("%Y-%m-%d %H:%M:%S"),))
        data = cur.fetchone()
        conn.close()
        ingresos, egresos, balance = data
    except Exception:
        ingresos, egresos, balance = (0, 0, 0)
    return f"""
💰 Reporte Financiero ({'última semana' if periodo == 'semana' else 'último mes'}):
- Ingresos: Q{ingresos or 0:.2f}
- Egresos: Q{egresos or 0:.2f}
- Balance: Q{balance or 0:.2f}
"""

#Graficos bisuales
def graficoLavadas(win, periodo="mes"):
    conn = conectar()
    cur = conn.cursor()
    fecha_limite = datetime.now() - timedelta(days=7 if periodo == "semana" else 30)
    cur.execute("""
        SELECT estado, COUNT(*) 
        FROM servicios 
        WHERE fecha >= ?
        GROUP BY estado
    """, (fecha_limite.strftime("%Y-%m-%d %H:%M:%S"),))
    data = cur.fetchall()
    conn.close()

    if not data:
        tk.Label(win, text="Sin datos para graficar.", bg="#1E1E1E", fg="white").pack()
        return

    estados = [d[0] for d in data]
    totales = [d[1] for d in data]

    fig, ax = plt.subplots(figsize=(5, 4), facecolor="#2B2B2B")
    ax.bar(estados, totales, color=["#2196F3", "#4CAF50", "#FFC107", "#E91E63"])
    ax.set_title(f"Lavadas por Estado ({'semana' if periodo == 'semana' else 'mes'})", color="white")
    ax.set_facecolor("#2B2B2B")
    ax.tick_params(colors="white")

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)


def graficoClientes(win, periodo="mes"):
    conn = conectar()
    cur = conn.cursor()
    fecha_limite = datetime.now() - timedelta(days=7 if periodo == "semana" else 30)
    cur.execute("""
        SELECT c.nombre, SUM(s.precio) 
        FROM clientes c
        JOIN servicios s ON c.idCliente = s.idCliente
        WHERE s.pago='pagado' AND s.fecha >= ?
        GROUP BY c.idCliente
        ORDER BY SUM(s.precio) DESC LIMIT 5
    """, (fecha_limite.strftime("%Y-%m-%d %H:%M:%S"),))
    data = cur.fetchall()
    conn.close()

    if not data:
        tk.Label(win, text="Sin datos de clientes recientes.", bg="#1E1E1E", fg="white").pack()
        return

    nombres = [d[0] for d in data]
    totales = [d[1] for d in data]

    fig, ax = plt.subplots(figsize=(5, 4), facecolor="#2B2B2B")
    ax.pie(totales, labels=nombres, autopct="%1.1f%%", startangle=90)
    ax.set_title(f"Top 5 Clientes ({'semana' if periodo == 'semana' else 'mes'})", color="white")
    fig.patch.set_facecolor("#2B2B2B")

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

def exportarExcel():
    conn = sqlite3.connect(DB_PATH)

    # Se crea un diccionario con las tablas a exportar
    tablas = {
        "Clientes": "SELECT * FROM clientes",
        "Servicios": "SELECT * FROM servicios",
        "Ingresos_Egresos": "SELECT * FROM ingresosYegresos"
    }

    nombreArchivo = f"Reporte_Lavanderia_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx" #El nombre del archivo condicionado por fecha
    with pd.ExcelWriter(nombreArchivo, engine="openpyxl") as writer:   #Coon openpyxl abrimos excel y creamos el documento
        for nombre, consulta in tablas.items():
            df = pd.read_sql_query(consulta, conn)
            df.to_excel(writer, sheet_name=nombre, index=False)

    conn.close()
    print(f"✅ Reporte generado exitosamente: {nombreArchivo}")
    os.startfile(nombreArchivo) 

    return nombreArchivo