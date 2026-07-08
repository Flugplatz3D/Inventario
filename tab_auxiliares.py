
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "inventario.db"

class TabAuxiliares(ttk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        print(f"aux.. Literal: {app.seccion.get()} | ID: {app.id_seccion_actual}") 

        # Clasificaciones
        self.id_clasificacion_actual = 0
        self.clasificacion = []
        self.idsClasificacion = {}
        self.clasificacion_labelID = tk.StringVar(value="0")

        # Cajas
        self.id_caja_actual = 0
        self.caja = []
        self.idsCaja = {}
        self.caja_labelID = tk.StringVar(value="0")
        self.seccion_caja_labelID = tk.StringVar(value="Prueba2")

        # Tipos de Caja en cajas
        self.id_tipo_caja_cajas_actual = 0
        self.tipos_caja_cajas = []
        self.ids_tipo_caja_cajas = {}

        # Bolsas
        self.id_bolsa_actual = 0
        self.bolsa = []
        self.idsbolsa = {}
        self.bolsa_labelID = tk.StringVar(value="0")

        # Tipos de Bolsa en bolsas
        self.id_tipo_bolsa_bolsas_actual = 0
        self.tipos_bolsa_bolsas = []
        self.ids_tipo_bolsa_bolsas = {}

        # Tipos de Caja
        self.id_tipo_caja_actual = 0
        self.tipos_caja = []
        self.ids_tipo_caja = {}
        self.tipos_caja_labelID = tk.StringVar(value="0")

        # Tipos de Bolsa
        self.id_tipo_bolsa_actual = 0
        self.tipos_bolsa = []
        self.ids_tipo_bolsa = {}
        self.tipos_bolsa_labelID = tk.StringVar(value="0")

        # Secciones
        self.id_seccion_actual = 0
        self.secciones = []
        self.ids_seccion = {}
        self.seccion_labelID = tk.StringVar(value="0")

        self.crear_layout()
        self.crear_frame_secciones()
        self.crear_frame_cajas()
        self.crear_frame_bolsas()
        self.crear_frame_clasificaciones()
        self.crear_frame_tipos_caja()
        self.crear_frame_tipos_bolsa()
        self.llenar_secciones()
        self.llenar_clasificacion()
        self.llenar_cajas()
        self.llenar_tipos_caja_cajas()
        self.llenar_bolsas()
        self.llenar_tipos_bolsa_bolsas()
        self.llenar_tipos_caja()
        self.llenar_tipos_bolsa()

    def crear_layout(self):
        # 3 columnas
        self.columnconfigure(0, weight=1, minsize=350)
        self.columnconfigure(1, weight=1, minsize=350)
        self.columnconfigure(2, weight=1, minsize=350)
        # 2 filas
        self.rowconfigure(0, weight=1, minsize=260)
        self.rowconfigure(1, weight=1, minsize=260)

    def crear_frame_secciones(self):
        
        self.frm_secciones = ttk.LabelFrame(self, text="Secciones")
        self.frm_secciones.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.frm_secciones.columnconfigure(0, weight=0)
        self.frm_secciones.columnconfigure(1, weight=1)

        tk.Label(self.frm_secciones, text="Sección").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.entrada_seccion = tk.Entry(self.frm_secciones, width=35)
        self.entrada_seccion.grid(row=0, column=1, sticky="ew", padx=10, pady=15)

        tk.Label(self.frm_secciones, text="ID").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.labelID_seccion = tk.Label(self.frm_secciones, text="0", textvariable=self.seccion_labelID, font=("Segoe UI", 9))
        self.labelID_seccion.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(self.frm_secciones, text="Secciones").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.combo_secciones = ttk.Combobox(self.frm_secciones, state="readonly", width=32)
        self.combo_secciones.grid(row=2, column=1, sticky="ew", padx=10, pady=8)
        self.combo_secciones.bind("<<ComboboxSelected>>", self.combo_secciones_click)

        btn_frame = ttk.Frame(self.frm_secciones)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text="Nuevo", command=self.nuevo_seccion, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Guardar", command=self.guardar_seccion, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_seccion, width=10).pack(side="left", padx=5)
 
    def crear_frame_cajas(self):

        self.frm_cajas = ttk.LabelFrame(self, text="Cajas")
        self.frm_cajas.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.frm_cajas.columnconfigure(0, weight=0)
        self.frm_cajas.columnconfigure(1, weight=1)

        tk.Label(self.frm_cajas, text="Caja").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.entrada_cajas = tk.Entry(self.frm_cajas, width=35)
        self.entrada_cajas.grid(row=0, column=1, sticky="ew", padx=10, pady=15)

        tk.Label(self.frm_cajas, text="ID").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.labelID_cajas = tk.Label(self.frm_cajas, text="0", textvariable=self.caja_labelID, font=("Segoe UI", 9))
        self.labelID_cajas.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(self.frm_cajas, text="Cajas").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.combo_cajas = ttk.Combobox(self.frm_cajas, state="readonly", width=32)
        self.combo_cajas.grid(row=2, column=1, sticky="ew", padx=10, pady=8)
        self.combo_cajas.bind("<<ComboboxSelected>>", self.combo_cajas_click)

        tk.Label(self.frm_cajas, text="Tipo de Caja").grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.combo_tipo_caja_cajas = ttk.Combobox(self.frm_cajas, state="readonly", width=32)
        self.combo_tipo_caja_cajas.grid(row=3, column=1, sticky="ew", padx=10, pady=8)
        self.combo_tipo_caja_cajas.bind("<<ComboboxSelected>>", self.combo_tipo_caja_cajas_click)

        tk.Label(self.frm_cajas, text="Sección").grid(row=4, column=0, sticky="e", padx=10, pady=8)
        self.labelID_seccion_cajas = tk.Label(self.frm_cajas, text="0", textvariable=self.seccion_caja_labelID, font=("Segoe UI", 9, "italic"))
        self.labelID_seccion_cajas.grid(row=4, column=1, sticky="w", padx=10, pady=8)

        btn_frame = ttk.Frame(self.frm_cajas)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Nuevo", command=self.nuevo_caja, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Guardar", command=self.guardar_caja, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_caja, width=10).pack(side="left", padx=5)

    def crear_frame_bolsas(self):

        self.frm_bolsas = ttk.LabelFrame(self, text="Bolsas")
        self.frm_bolsas.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.frm_bolsas.columnconfigure(0, weight=0)
        self.frm_bolsas.columnconfigure(1, weight=1)

        tk.Label(self.frm_bolsas, text="Bolsa").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.entrada_bolsa = tk.Entry(self.frm_bolsas, width=35)
        self.entrada_bolsa.grid(row=0, column=1, sticky="ew", padx=10, pady=15)

        tk.Label(self.frm_bolsas, text="ID").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.labelID_bolsa = tk.Label(self.frm_bolsas, text="0", textvariable=self.bolsa_labelID, font=("Segoe UI", 9))
        self.labelID_bolsa.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(self.frm_bolsas, text="Bolsas").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.combo_bolsas = ttk.Combobox(self.frm_bolsas, state="readonly", width=32)
        self.combo_bolsas.grid(row=2, column=1, sticky="ew", padx=10, pady=8)
        self.combo_bolsas.bind("<<ComboboxSelected>>", self.combo_bolsas_click)

        tk.Label(self.frm_bolsas, text="Tipo de Bolsa").grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.combo_tipo_bolsa_bolsas = ttk.Combobox(self.frm_bolsas, state="readonly", width=32)
        self.combo_tipo_bolsa_bolsas.grid(row=3, column=1, sticky="ew", padx=10, pady=8)
        self.combo_tipo_bolsa_bolsas.bind("<<ComboboxSelected>>", self.combo_tipo_bolsa_bolsas_click)

        # tk.Label(self.frm_bolsas, text="Sección").grid(row=4, column=0, sticky="e", padx=10, pady=8)
        # self.combo_seccion_bolsas = ttk.Combobox(self.frm_bolsas, state="readonly", width=32)
        # self.combo_seccion_bolsas.grid(row=4, column=1, sticky="ew", padx=10, pady=8)
        # self.combo_seccion_bolsas.bind("<<ComboboxSelected>>", self.combo_seccion_bolsas_click)

        tk.Label(self.frm_bolsas, text="Sección").grid(row=4, column=0, sticky="e", padx=10, pady=8)
        self.labelID_seccion_cajas = tk.Label(self.frm_bolsas, text= self.app.seccion.get(), font=("Segoe UI", 9, "italic"))
        self.labelID_seccion_cajas.grid(row=4, column=1, sticky="w", padx=10, pady=8)

        btn_frame = ttk.Frame(self.frm_bolsas)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Nuevo", command=self.nuevo_bolsa, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Guardar", command=self.guardar_bolsa, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_bolsa, width=10).pack(side="left", padx=5)

    def crear_frame_clasificaciones(self):

        self.frm_datos = ttk.LabelFrame(self, text="Clasificaciones")
        self.frm_datos.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        tk.Label(self.frm_datos, text="Clasificación").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.entrada_clasificacion = tk.Entry(self.frm_datos, width=35)
        self.entrada_clasificacion.grid(row=0, column=1, sticky="ew", padx=10, pady=15)

        tk.Label(self.frm_datos, text="ID").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.labelID_clasificacion = tk.Label(self.frm_datos, textvariable=self.clasificacion_labelID, 
                                font=("Segoe UI", 9))
        self.labelID_clasificacion.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(self.frm_datos, text="Clasificaciones").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.comboClasificaciones = ttk.Combobox(self.frm_datos, state="readonly", width=32)
        self.comboClasificaciones.grid(row=2, column=1, sticky="ew", padx=10, pady=8)
        self.comboClasificaciones.bind("<<ComboboxSelected>>", self.combo_clasificaciones_click)

        btn_frame = ttk.Frame(self.frm_datos)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text="Nuevo", command=self.nuevo_clasificacion, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Guardar", command=self.guardar_clasificacion, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_clasificacion, width=10).pack(side="left", padx=5)

    def crear_frame_tipos_caja(self):

        self.frm_tipos_caja = ttk.LabelFrame(self, text="Tipos de Caja")
        self.frm_tipos_caja.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.frm_tipos_caja.columnconfigure(0, weight=0)
        self.frm_tipos_caja.columnconfigure(1, weight=1)

        tk.Label(self.frm_tipos_caja, text="Tipo de Caja").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.entrada_tipo_caja = tk.Entry(self.frm_tipos_caja, width=35)
        self.entrada_tipo_caja.grid(row=0, column=1, sticky="ew", padx=10, pady=15)

        tk.Label(self.frm_tipos_caja, text="ID").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.labelID_tipo_caja = tk.Label(self.frm_tipos_caja, text="0", textvariable=self.tipos_caja_labelID, font=("Segoe UI", 9))
        self.labelID_tipo_caja.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(self.frm_tipos_caja, text="Tipos de Caja").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.combo_tipo_caja = ttk.Combobox(self.frm_tipos_caja, state="readonly", width=32)
        self.combo_tipo_caja.grid(row=2, column=1, sticky="ew", padx=10, pady=8)
        self.combo_tipo_caja.bind("<<ComboboxSelected>>", self.combo_tipo_caja_click)

        btn_frame = ttk.Frame(self.frm_tipos_caja)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text="Nuevo", command=self.nuevo_tipo_caja, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Guardar", command=self.guardar_tipo_caja, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_tipo_caja, width=10).pack(side="left", padx=5)

    def crear_frame_tipos_bolsa(self):
        self.frm_tipos_bolsa = ttk.LabelFrame(self, text="Tipos Bolsa")
        self.frm_tipos_bolsa.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        self.frm_tipos_bolsa.columnconfigure(0, weight=0)
        self.frm_tipos_bolsa.columnconfigure(1, weight=1)

        tk.Label(self.frm_tipos_bolsa, text="Tipo de Bolsa").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.entrada_tipo_bolsa = tk.Entry(self.frm_tipos_bolsa, width=35)
        self.entrada_tipo_bolsa.grid(row=0, column=1, sticky="ew", padx=10, pady=15)

        tk.Label(self.frm_tipos_bolsa, text="ID").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.labelID_tipo_bolsa = tk.Label(self.frm_tipos_bolsa, text="0", textvariable=self.tipos_bolsa_labelID, font=("Segoe UI", 9))
        self.labelID_tipo_bolsa.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(self.frm_tipos_bolsa, text="Tipos de Bolsa").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.combo_tipo_bolsa = ttk.Combobox(self.frm_tipos_bolsa, state="readonly", width=32)
        self.combo_tipo_bolsa.grid(row=2, column=1, sticky="ew", padx=10, pady=8)
        self.combo_tipo_bolsa.bind("<<ComboboxSelected>>", self.combo_tipo_bolsa_click)

        btn_frame = ttk.Frame(self.frm_tipos_bolsa)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text="Nuevo", command=self.nuevo_tipo_bolsa, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Guardar", command=self.guardar_tipo_bolsa, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_tipo_bolsa, width=10).pack(side="left", padx=5)

    def llenar_clasificacion(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT ClasificacionID, Clasificacion FROM Clasificaciones ORDER BY upper(Clasificacion)")
            rows = cursor.fetchall()
            conn.close()

            self.clasificacion = [""]
            self.idsClasificacion = {"": 0}
            for row in rows:
                self.clasificacion.append(row[1])
                self.idsClasificacion[row[1]] = row[0]

            self.comboClasificaciones['values'] = self.clasificacion
            self.comboClasificaciones.set("")
        except Exception as e:
            print("Error cargando Clasificacion:", e)

    def llenar_cajas(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT CajaID, Caja FROM cajas ORDER BY upper(Caja)")
            rows = cursor.fetchall()
            conn.close()

            self.caja = [""]
            self.idsCaja = {"": 0}
            for row in rows:
                self.caja.append(row[1])
                self.idsCaja[row[1]] = row[0]

            self.combo_cajas['values'] = self.caja
            self.combo_cajas.set("")
        except Exception as e:
            print("Error cargando Cajas:", e)

    def llenar_tipos_caja_cajas(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT TipoCajaID, TipoCaja FROM TiposCaja ORDER BY upper(TipoCaja)")
            rows = cursor.fetchall()
            conn.close()
            self.tipos_caja_cajas = [""]
            self.ids_tipo_caja_cajas = {"": 0}
            for row in rows:
                self.tipos_caja_cajas.append(row[1])
                self.ids_tipo_caja_cajas[row[1]] = row[0]
            self.combo_tipo_caja_cajas['values'] = self.tipos_caja_cajas
            self.combo_tipo_caja_cajas.set("")
        except Exception as e:
            print("Error cargando Tipos de Caja:", e)

    def llenar_bolsas(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT BolsaID, Bolsa FROM bolsas ORDER BY upper(Bolsa)")
            rows = cursor.fetchall()
            conn.close()

            self.bolsas = [""]
            self.idsBolsa = {"": 0}
            for row in rows:
                self.bolsas.append(row[1])
                self.idsBolsa[row[1]] = row[0]

            self.combo_bolsas['values'] = self.bolsas
            self.combo_bolsas.set("")
        except Exception as e:
            print("Error cargando Bolsas:", e)

    def llenar_tipos_bolsa_bolsas(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT TipoBolsaID, TipoBolsa FROM TiposBolsa ORDER BY upper(TipoBolsa)")
            rows = cursor.fetchall()
            conn.close()

            self.tipos_bolsa_bolsas = [""]
            self.idsTipoBolsa_bolsas = {"": 0}
            for row in rows:
                self.tipos_bolsa_bolsas.append(row[1])
                self.idsTipoBolsa_bolsas[row[1]] = row[0]

            self.combo_tipo_bolsa_bolsas['values'] = self.tipos_bolsa_bolsas
            self.combo_tipo_bolsa_bolsas.set("")
        except Exception as e:
            print("Error cargando Tipos de Bolsa:", e)

    def llenar_tipos_caja(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT TipoCajaID, TipoCaja FROM TiposCaja ORDER BY upper(TipoCaja)")
            rows = cursor.fetchall()
            conn.close()
            self.tipos_caja = [""]
            self.idsTipoCaja = {"": 0}
            for row in rows:
                self.tipos_caja.append(row[1])
                self.idsTipoCaja[row[1]] = row[0]
            self.combo_tipo_caja['values'] = self.tipos_caja
            self.combo_tipo_caja.set("")
        except Exception as e:
            print("Error cargando Tipos de Caja:", e)

    def llenar_tipos_bolsa(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT TipoBolsaID, TipoBolsa FROM TiposBolsa ORDER BY upper(TipoBolsa)")
            rows = cursor.fetchall()
            conn.close()

            self.tipos_bolsa = [""]
            self.idsTipoBolsa = {"": 0}
            for row in rows:
                self.tipos_bolsa.append(row[1])
                self.idsTipoBolsa[row[1]] = row[0]

            self.combo_tipo_bolsa['values'] = self.tipos_bolsa
            self.combo_tipo_bolsa.set("")
        except Exception as e:
            print("Error cargando Tipos de Bolsa:", e)

    def llenar_secciones(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT SeccionID, Seccion FROM Secciones ORDER BY upper(Seccion)")
            rows = cursor.fetchall()
            conn.close()

            self.secciones = [""]
            self.ids_seccion = {"": 0}
            for row in rows:
                self.secciones.append(row[1])
                self.ids_seccion[row[1]] = row[0]

            self.combo_secciones['values'] = self.secciones
            self.combo_secciones.set("")
        except Exception as e:
            print("Error cargando Secciones:", e)

    def llenar_secciones_cajas(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT SeccionID, Seccion FROM Secciones ORDER BY upper(Seccion)")
            rows = cursor.fetchall()
            conn.close()

            self.secciones_cajas = [""]
            self.ids_seccion_cajas = {"": 0}
            for row in rows:
                self.secciones_cajas.append(row[1])
                self.ids_seccion_cajas[row[1]] = row[0]

            self.combo_seccion_cajas['values'] = self.secciones_cajas
            self.combo_seccion_cajas.set("")
            # print(self.ids_seccion_cajas)
            # print(self.secciones_cajas)
        except Exception as e:
            print("Error cargando Secciones para Cajas:", e)

    def llenar_secciones_bolsas(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT SeccionID, Seccion FROM Secciones ORDER BY upper(Seccion)")
            rows = cursor.fetchall()
            conn.close()

            self.secciones_bolsas = [""]
            self.ids_seccion_bolsas = {"": 0}
            for row in rows:
                self.secciones_bolsas.append(row[1])
                self.ids_seccion_bolsas[row[1]] = row[0]

            self.combo_seccion_bolsas['values'] = self.secciones_bolsas
            self.combo_seccion_bolsas.set("")
            # print(self.ids_seccion_bolsas)
            # print(self.secciones_bolsas)

        except Exception as e:
            print("Error cargando Secciones para Bolsas:", e)

    def nuevo_clasificacion(self):
        self.entrada_clasificacion.delete(0, tk.END) #self.entrada_clasificacion.insert(0, '')
        self.clasificacion_labelID.set('0')
        self.comboClasificaciones.set('')
        self.entrada_clasificacion.focus_set()

    def nuevo_caja(self):
        self.entrada_cajas.delete(0, tk.END)
        self.caja_labelID.set('0')
        self.combo_cajas.set('')
        self.entrada_cajas.insert(0, '')
        self.combo_tipo_caja_cajas.set('')
        self.combo_seccion_cajas.set('')
        self.entrada_cajas.focus_set()
        
    def nuevo_bolsa(self):
        self.entrada_bolsa.delete(0, tk.END)
        self.bolsa_labelID.set('0')
        self.combo_bolsas.set('')
        self.entrada_bolsa.insert(0, '')
        self.combo_tipo_bolsa_bolsas.set('')
        self.combo_seccion_bolsas.set('')
        self.entrada_bolsa.focus_set()

    def nuevo_tipo_caja(self):
        self.entrada_tipo_caja.delete(0, tk.END)
        self.tipos_caja_labelID.set('0')
        self.combo_tipo_caja.set('')
        self.entrada_tipo_caja.focus_set()

    def nuevo_tipo_bolsa(self):
        self.entrada_tipo_bolsa.delete(0, tk.END)
        self.tipos_bolsa_labelID.set('0')
        self.combo_tipo_bolsa.set('')
        self.entrada_tipo_bolsa.focus_set()

    def nuevo_seccion(self):
        self.entrada_seccion.delete(0, tk.END)
        self.seccion_labelID.set('0')
        self.combo_secciones.set('')
        self.entrada_seccion.focus_set()
        
    def guardar_clasificacion(self):     
        selected = self.comboClasificaciones.get()
        self.id_clasificacion_actual = self.idsClasificacion.get(selected, 0)
        valor = self.entrada_clasificacion.get().strip()
        if valor == '':
            messagebox.showwarning("Error", "Se debe rellenar la Clasificación")
            return
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if selected != '' and self.id_clasificacion_actual != 0:
                cadena = f"UPDATE Clasificaciones SET Clasificacion = '{valor}' WHERE ClasificacionID = {self.id_clasificacion_actual}"
            else:
                cadena = f"INSERT INTO Clasificaciones (Clasificacion) VALUES ('{valor}')"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.llenar_clasificacion()
            self.comboClasificaciones.set(valor)
            self.entrada_clasificacion.focus_set()
            messagebox.showinfo("Éxito", "Operación realizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def guardar_caja(self):
        selected = self.combo_cajas.get()
        self.id_caja_actual = self.idsCaja.get(selected, 0)
        valor_caja = self.entrada_cajas.get().strip()
        if valor_caja == '':
            messagebox.showwarning("Error", "Se debe rellenar la Caja")
            return
        if self.combo_tipo_caja_cajas.get() == '':
            messagebox.showwarning("Error", "Se debe seleccionar un Tipo de Caja")
            return
        valor_tipo_caja = self.combo_tipo_caja_cajas.get()
        self.id_tipo_caja_cajas_actual = self.ids_tipo_caja_cajas.get(valor_tipo_caja, 0)
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            # print(f"Guardar Caja: {valor_caja}\nID actual: {self.id_caja_actual}\nTipo Caja: {valor_tipo_caja}\nID Tipo Caja: {self.id_tipo_caja_cajas_actual}\nSeccion: {self.id_seccion_cajas_actual}")
            if selected != '' and self.id_caja_actual != 0:
                cadena = f"UPDATE Cajas SET Caja = '{valor_caja}', TipoCajaID = {self.id_tipo_caja_cajas_actual}, SeccionID = {self.id_seccion_cajas_actual} WHERE CajaID = {self.id_caja_actual}"
            else:
                cadena = f"INSERT INTO Cajas (Caja, TipoCajaID, SeccionID) VALUES ('{valor_caja}', {self.id_tipo_caja_cajas_actual}, {self.id_seccion_cajas_actual})"
            print(cadena)
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.llenar_cajas()
            self.combo_cajas.set(valor_caja)
            self.llenar_tipos_caja_cajas()
            self.combo_tipo_caja_cajas.set(valor_tipo_caja)
            self.entrada_cajas.focus_set()
            messagebox.showinfo("Éxito", "Operación realizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def guardar_bolsa(self):
        # self.combo_tipo_bolsa_bolsas.config(state="disabled")
        selected = self.combo_bolsas.get()
        self.id_bolsa_actual = self.idsBolsa.get(selected, 0)
        valor_bolsa = self.entrada_bolsa.get().strip()
        if valor_bolsa == '':
            messagebox.showwarning("Error", "Se debe rellenar la Bolsa")
            return
        if self.combo_tipo_bolsa_bolsas.get() == '':
            messagebox.showwarning("Error", "Se debe seleccionar un Tipo de Bolsa")
            return
        valor_tipo_bolsa = self.combo_tipo_bolsa_bolsas.get()
        self.id_tipo_bolsa_bolsas_actual = self.idsTipoBolsa_bolsas.get(valor_tipo_bolsa, 0)
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            print(f"Guardar Bolsa: {valor_bolsa}, ID actual: {self.id_bolsa_actual}")
            if selected != '' and self.id_bolsa_actual != 0:
                cadena = f"UPDATE Bolsas SET Bolsa = '{valor_bolsa}', TipoBolsaID = {self.id_tipo_bolsa_bolsas_actual}, SeccionID = {self.id_seccion_bolsas_actual} WHERE BolsaID = {self.id_bolsa_actual}"
            else:
                cadena = f"INSERT INTO Bolsas (Bolsa, TipoBolsaID) VALUES ('{valor_bolsa}', {self.id_tipo_bolsa_bolsas_actual})"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.llenar_bolsas()
            self.combo_bolsas.set(valor_bolsa)
            self.llenar_tipos_bolsa_bolsas()
            self.combo_tipo_bolsa_bolsas.set(valor_tipo_bolsa)
            self.entrada_bolsa.focus_set()
            messagebox.showinfo("Éxito", "Operación realizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def guardar_tipo_caja(self):
        selected = self.combo_tipo_caja.get()
        self.id_tipo_caja_actual = self.idsTipoCaja.get(selected, 0)
        valor = self.entrada_tipo_caja.get().strip()
        if valor == '': 
            messagebox.showwarning("Error", "Se debe rellenar el Tipo de Caja")
            return
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            print(f"Guardar Tipo de Caja: {valor}, ID actual: {self.id_tipo_caja_actual}")
            if selected != '' and self.id_tipo_caja_actual != 0:
                cadena = f"UPDATE TiposCaja SET TipoCaja = '{valor}' WHERE TipoCajaID = {self.id_tipo_caja_actual}"
            else:
                cadena = f"INSERT INTO TiposCaja (TipoCaja) VALUES ('{valor}')"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.llenar_tipos_caja()
            self.llenar_tipos_caja_cajas()
            self.combo_tipo_caja.set(valor) 
            self.entrada_tipo_caja.focus_set()
            messagebox.showinfo("Éxito", "Operación realizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")  

    def guardar_tipo_bolsa(self):
        selected = self.combo_tipo_bolsa.get()
        self.id_tipo_bolsa_actual = self.idsTipoBolsa.get(selected, 0)
        valor = self.entrada_tipo_bolsa.get().strip()
        if valor == '':
            messagebox.showwarning("Error", "Se debe rellenar el Tipo de Bolsa")
            return
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            print(f"Guardar Tipo de Bolsa: {valor}, ID actual: {self.id_tipo_bolsa_actual}")
            if selected != '' and self.id_tipo_bolsa_actual != 0:
                cadena = f"UPDATE TiposBolsa SET TipoBolsa = '{valor}' WHERE TipoBolsaID = {self.id_tipo_bolsa_actual}"
            else:
                cadena = f"INSERT INTO TiposBolsa (TipoBolsa) VALUES ('{valor}')"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.llenar_tipos_bolsa()
            self.llenar_tipos_bolsa_bolsas()
            self.combo_tipo_bolsa.set(valor)
            self.entrada_tipo_bolsa.focus_set()
            messagebox.showinfo("Éxito", "Operación realizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def guardar_seccion(self):
        selected = self.combo_secciones.get()
        self.id_seccion_actual = self.ids_seccion.get(selected, 0)
        valor = self.entrada_seccion.get().strip()
        if valor == '':
            messagebox.showwarning("Error", "Se debe rellenar la Sección")
            return
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            print(f"Guardar Sección: {valor}, ID actual: {self.id_seccion_actual}")
            if selected != '' and self.id_seccion_actual != 0:
                cadena = f"UPDATE Secciones SET Seccion = '{valor}' WHERE SeccionID = {self.id_seccion_actual}"
            else:
                cadena = f"INSERT INTO Secciones (Seccion) VALUES ('{valor}')"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.llenar_secciones()
            self.combo_secciones.set(valor)
            self.entrada_seccion.focus_set()
            messagebox.showinfo("Éxito", "Operación realizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def eliminar_clasificacion(self):
        selected = self.comboClasificaciones.get()
        self.id_clasificacion_actual = self.idsClasificacion.get(selected, 0)
        if selected == '':
            return
        total = self.contar_registros_asociados(self.id_clasificacion_actual, "ClasificacionID", "detalles")
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if total > 0:
                messagebox.showerror("Eliminar", f"No se puede borrar:\nHay {total} registros asociados")
                conn.close()
                return
            cadena = f"DELETE FROM Clasificaciones WHERE ClasificacionID = {self.id_clasificacion_actual}"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.nuevo_clasificacion()
            self.llenar_clasificacion()
            self.entrada_clasificacion.focus_set()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    def eliminar_caja(self):
        # messagebox.showinfo("Eliminar", "Función de eliminar Caja en desarrollo")
        selected = self.combo_cajas.get()
        self.id_caja_actual = self.idsCaja.get(selected, 0)
        if selected == '':
            return
        total = self.contar_registros_asociados(self.id_caja_actual, "CajaID", "detalles")
        try:    
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if total > 0:
                messagebox.showerror("Eliminar", f"No se puede borrar:\nHay {total} registros asociados")
                conn.close()
                return
            cadena = f"DELETE FROM Cajas WHERE CajaID = {self.id_caja_actual}"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.nuevo_caja()
            self.llenar_cajas()
            self.llenar_tipos_caja_cajas()
            self.entrada_cajas.focus_set()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    def eliminar_bolsa(self):
        selected = self.combo_bolsas.get()
        self.id_bolsa_actual = self.idsBolsa.get(selected, 0)
        if selected == '':
            return
        total = self.contar_registros_asociados(self.id_bolsa_actual, "BolsaID", "detalles")
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if total > 0:
                messagebox.showerror("Eliminar", f"No se puede borrar:\nHay {total} registros asociados")
                conn.close()
                return
            cadena = f"DELETE FROM Bolsas WHERE BolsaID = {self.id_bolsa_actual}"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.nuevo_bolsa()
            self.llenar_bolsas()
            self.llenar_tipos_bolsa_bolsas()
            self.entrada_bolsa.focus_set()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    def eliminar_tipo_caja(self):
        selected = self.combo_tipo_caja.get()
        self.id_tipo_caja_actual = self.idsTipoCaja.get(selected, 0)
        if selected == '':
            return
        total = self.contar_registros_asociados(self.id_tipo_caja_actual, "TipoCajaID", "cajas")
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if total > 0:
                messagebox.showerror("Eliminar", f"No se puede borrar:\nHay {total} registros asociados")
                conn.close()
                return
            cadena = f"DELETE FROM TiposCaja WHERE TipoCajaID = {self.id_tipo_caja_actual}"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.nuevo_tipo_caja()
            self.llenar_tipos_caja()
            self.llenar_tipos_caja_cajas()
            self.entrada_tipo_caja.focus_set()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    def eliminar_tipo_bolsa(self):
        selected = self.combo_tipo_bolsa.get()
        self.id_tipo_bolsa_actual = self.idsTipoBolsa.get(selected, 0)
        if selected == '':
            return
        total = self.contar_registros_asociados(self.id_tipo_bolsa_actual, "TipoBolsaID", "bolsas")
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if total > 0:
                messagebox.showerror("Eliminar", f"No se puede borrar:\nHay {total} registros asociados")
                conn.close()
                return
            cadena = f"DELETE FROM TiposBolsa WHERE TipoBolsaID = {self.id_tipo_bolsa_actual}"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.nuevo_tipo_bolsa()
            self.llenar_tipos_bolsa()
            self.llenar_tipos_bolsa_bolsas()
            self.entrada_tipo_bolsa.focus_set()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    def eliminar_seccion(self):
        selected = self.combo_secciones.get()
        self.id_seccion_actual = self.ids_seccion.get(selected, 0)
        if selected == '':
            return
        total = self.contar_registros_asociados(self.id_seccion_actual, "SeccionID", "detalles")
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if total > 0:
                messagebox.showerror("Eliminar", f"No se puede borrar:\nHay {total} registros asociados")
                conn.close()
                return
            cadena = f"DELETE FROM Secciones WHERE SeccionID = {self.id_seccion_actual}"
            cursor.execute(cadena)
            conn.commit()
            conn.close()
            self.nuevo_seccion()
            self.llenar_secciones()
            self.entrada_seccion.focus_set()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
            
    def combo_clasificaciones_click(self, event):
        selected = self.comboClasificaciones.get()
        self.id_clasificacion_actual = self.idsClasificacion.get(selected, 0)
        self.entrada_clasificacion.delete(0, tk.END)
        self.entrada_clasificacion.insert(0, selected)
        self.clasificacion_labelID.set(self.id_clasificacion_actual)

    def combo_cajas_click(self, event):
        selected = self.combo_cajas.get()
        self.id_caja_actual = self.idsCaja.get(selected, 0)
        self.caja_labelID.set(str(self.id_caja_actual))
        self.entrada_cajas.delete(0, tk.END)
        self.entrada_cajas.insert(0, selected)
        self.seccion_caja_labelID.set(self.app.seccion.get())
        if selected == '':
            self.combo_tipo_caja_cajas.set('')
            return  
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cadena = f"select t.TipoCaja from tiposCaja t, cajas c where c.CajaID =  {self.id_caja_actual}"
            cadena += " and t.TipoCajaID = c.TipoCajaID"
            cursor.execute(cadena)
            row = cursor.fetchone()
            tipo_caja = row[0]
            self.combo_tipo_caja_cajas.set(tipo_caja)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer tipo caja:\n{e}")

    def combo_bolsas_click(self, event):
        selected = self.combo_bolsas.get()
        self.id_bolsa_actual = self.idsBolsa.get(selected, 0)
        self.bolsa_labelID.set(str(self.id_bolsa_actual))
        self.entrada_bolsa.delete(0, tk.END)
        self.entrada_bolsa.insert(0, selected)
        if selected == '':
            self.combo_tipo_bolsa_bolsas.set('')
            return
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            # cadena = f"select TipoBolsa from tiposBolsa t, bolsas b where b.BolsaID = {self.id_bolsa_actual} and t.TipoBolsaID = b.TipoBolsaID"
            cadena = f"select t.TipoBolsa, s.seccion from tiposBolsa t, bolsas c, secciones s where c.BolsaID =  {self.id_bolsa_actual}"
            cadena += " and t.TipoBolsaID = c.TipoBolsaID and c.SeccionID = s.SeccionID"
            cursor.execute(cadena)
            row = cursor.fetchone()
            tipo_bolsa = row[0]
            seccion_bolsa = row[1]
            self.combo_tipo_bolsa_bolsas.set(tipo_bolsa)
            self.combo_seccion_bolsas.set(seccion_bolsa)
            selected = self.combo_seccion_bolsas.get()
            self.id_seccion_bolsas_actual = self.ids_seccion_bolsas.get(selected, 0)
            print(self.id_seccion_bolsas_actual)
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer tipo bolsa:\n{e}")
        
    def combo_tipo_caja_click(self, event):
        selected = self.combo_tipo_caja.get()
        self.id_tipo_caja_actual = self.idsTipoCaja.get(selected, 0)
        self.entrada_tipo_caja.delete(0, tk.END)
        self.entrada_tipo_caja.insert(0, selected)
        self.tipos_caja_labelID.set(str(self.id_tipo_caja_actual))

    def combo_tipo_caja_cajas_click(self, event):
        selected = self.combo_tipo_caja_cajas.get()
        self.id_tipo_caja_cajas_actual = self.ids_tipo_caja_cajas.get(selected, 0)

    def combo_tipo_bolsa_click(self, event):
        selected = self.combo_tipo_bolsa.get()
        self.id_tipo_bolsa_actual = self.idsTipoBolsa.get(selected, 0)
        self.entrada_tipo_bolsa.delete(0, tk.END)
        self.entrada_tipo_bolsa.insert(0, selected)
        self.tipos_bolsa_labelID.set(str(self.id_tipo_bolsa_actual))

    def combo_tipo_bolsa_bolsas_click(self, event):
        selected = self.combo_tipo_bolsa_bolsas.get()
        self.id_tipo_bolsa_bolsas_actual = self.idsTipoBolsa_bolsas.get(selected, 0)
    
    def combo_secciones_click(self, event):
        selected = self.combo_secciones.get()
        self.id_seccion_actual = self.ids_seccion.get(selected, 0)
        self.entrada_seccion.delete(0, tk.END)
        self.entrada_seccion.insert(0, selected)
        self.seccion_labelID.set(str(self.id_seccion_actual))
        print(f"Sección seleccionada: {selected}, ID: {self.id_seccion_actual}")

    def combo_seccion_cajas_click(self, event):
        selected = self.combo_seccion_cajas.get()
        self.id_seccion_cajas_actual = self.ids_seccion_cajas.get(selected, 0)

        # print(f"Sección para Cajas seleccionada: {selected}, ID: {self.id_seccion_cajas_actual}")

    def combo_seccion_bolsas_click(self, event):
        selected = self.combo_seccion_bolsas.get()
        self.id_seccion_bolsas_actual = self.ids_seccion_bolsas.get(selected, 0)

    def contar_registros_asociados(self, valor_id, campo, tabla):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cadena = f"SELECT count(*) FROM {tabla} WHERE {campo} = {valor_id}"
            # print(f"Registros asociados:\n {cadena}")
            cursor.execute(cadena)
            total = cursor.fetchone()[0]
            conn.close()
            return total
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo contar los registros asociados:\n{e}")
            return -1
