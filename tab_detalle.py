import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

DB_NAME = "inventario.db"

class TabDetalle(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        # print(f"Literal: {app.seccion.get()} | ID: {app.id_seccion_actual}") 
       
        # Variables
        self.intOrden = tk.IntVar(value=1)
        self.intSentido = tk.IntVar(value=1)
        self.id_caja_actual = 0
        self.id_bolsa_actual = 0
        self.id_clasificacion_actual = 0

        self.texto_labelID = tk.StringVar()
        self.texto_labelCaja = tk.StringVar(value="labelcaja")
        self.texto_labelBolsa = tk.StringVar(value="labelBolsa")
        self.texto_label_recuento = tk.StringVar(value="")

        self.cajas = []
        self.idsCajas = {}
        self.bolsas = []
        self.idsBolsas = {}
        self.clasificacion = []
        self.idsClasificacion = {}

        self.setup_ui()
        self.llenarCajas()
        self.llenarBolsas()
        self.llenarClasificacion()

        # Dato de prueba
        # self.entrada1.insert(0, "ESP32")

    def setup_ui(self):
        tk.Label(self, text="Descripción1").place(x=10, y=15)
        self.entrada1 = tk.Entry(self, width=22)
        self.entrada1.place(x=95, y=15)

        tk.Label(self, text="Descripción2").place(x=300, y=15)
        self.entrada2 = tk.Entry(self, width=22)
        self.entrada2.place(x=385, y=15)

        tk.Label(self, text="Detalle").place(x=580, y=15)
        self.entrada3 = tk.Entry(self, width=22)
        self.entrada3.place(x=665, y=15)

        tk.Label(self, text="Cajas").place(x=10, y=45)
        tk.Label(self, text="Bolsas").place(x=10, y=75)
        tk.Label(self, text="Clasificación").place(x=10, y=105)

        # Combos
        self.comboCajas = ttk.Combobox(self, state="readonly", width=27)
        self.comboCajas.place(x=95, y=45)
        
        self.comboBolsas = ttk.Combobox(self, state="readonly", width=27)
        self.comboBolsas.place(x=95, y=75)

        self.comboClasificaciones = ttk.Combobox(self, state="readonly", width=27)
        self.comboClasificaciones.place(x=95, y=105)

        self.comboCajas.bind("<<ComboboxSelected>>", self.comboCajasClick)
        self.comboBolsas.bind("<<ComboboxSelected>>", self.comboBolsasClick)
        self.comboClasificaciones.bind("<<ComboboxSelected>>", self.comboClasificacionClick)

        # Botones de búsqueda
        tk.Button(self, text="Buscar", command=self.buscar, width=10).place(x=890, y=10)
        tk.Button(self, text="Limpiar", command=self.limpiar, width=10).place(x=980, y=10)

        self.botonDetalle = tk.Button(self, text="Detalle", 
                                    command=self.mostrar_editar_detalle_modal,
                                    width=10, state=tk.DISABLED)
        self.botonDetalle.place(x=10, y=510)

        self.botonEliminar = tk.Button(self, text="Eliminar", command=self.eliminar_seleccionado, 
                  width=10, state=tk.DISABLED)
        self.botonEliminar.place(x=100, y=510)
        
        self.botonNuevo = tk.Button(self, text="Nuevo", command=self.nuevo_registro, 
                                    width=10, state=tk.ACTIVE)
        self.botonNuevo.place(x=190, y=510)

        self.labelRecuento = tk.Label(self, text="", textvariable=self.texto_label_recuento, font=("Segoe UI", 9))
        self.labelRecuento.place(x=880,y=510)

        # Radiobuttons para orden
        rb1_1 = ttk.Radiobutton(self, text="Descripción", variable=self.intOrden, 
                        value=1, command=self.buscar).place(x=660, y=70)
        rb1_2 = ttk.Radiobutton(self, text="Clasificación", variable=self.intOrden, 
                        value=2, command=self.buscar).place(x=750, y=70)
        rb1_3 = ttk.Radiobutton(self, text="Detalle", variable=self.intOrden, 
                        value=3, command=self.buscar).place(x=847, y=70)
        rb1_4 = ttk.Radiobutton(self, text="Caja", variable=self.intOrden, 
                        value=4, command=self.buscar).place(x=910, y=70)
        rb1_5 = ttk.Radiobutton(self, text="Bolsa", variable=self.intOrden, 
                        value=5, command=self.buscar).place(x=963, y=70)
        rb1_6 = ttk.Radiobutton(self, text="ID", variable=self.intOrden, 
                        value=6, command=self.buscar).place(x=1020, y=70)
        # Radiobuttons para sentido
        rb2_1 = ttk.Radiobutton(self, text="ASC", variable=self.intSentido, 
                        value=1, command=self.buscar).place(x=660, y=110)
        rb2_2 = ttk.Radiobutton(self, text="DESC", variable=self.intSentido, 
                        value=2, command=self.buscar).place(x=720, y=110)

        # ==================== TREEVIEW ====================
        self.tree = ttk.Treeview(self, columns=("Descripcion", "Clasificacion", "Detalle", 
                                                "Caja", "TipoCaja", "Bolsa", "TipoBolsa", "Cantidad", "id"), 
                                 show="headings", height=15, selectmode="extended")

        columnas = {
            "Descripcion":   ("Descripción", 170),
            "Clasificacion": ("Clasificación", 145),
            "Detalle":       ("Detalle", 160),
            "Caja":          ("Caja", 155),
            "TipoCaja":      ("TipoCaja", 90),
            "Bolsa":         ("Bolsa", 120),
            "TipoBolsa":     ("TipoBolsa", 115),
            "Cantidad":      ("Cantidad", 56),
            "id":            ("ID", 35)
        }

        for col, (texto, ancho) in columnas.items():
            self.tree.heading(col, text=texto, anchor=tk.W,
                              command=lambda c=col: self.ordenar_por_columna(c))
            self.tree.column(col, width=ancho, anchor=tk.W, stretch=False)

        self.tree.column('#0', width=0, stretch=False)
        self.tree.place(x=10, y=160, width=1048, height=328)

        # Scrollbars
        scroll_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.place(x=10, y=490, width=1048)
        scroll_y.place(x=1060, y=160, height=328)

        # Bindings
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.on_right_click)

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def buscar(self, *args):
        
        id_seccion = self.app.id_seccion_actual

        texto1 = self.entrada1.get().strip()
        texto2 = self.entrada2.get().strip()
        texto3 = self.entrada3.get().strip()

        cadena = "select d.Descripcion, f.Clasificacion, d.Detalle, c.Caja, tc.TipoCaja, "
        cadena += "b.Bolsa, tb.TipoBolsa, d.Cantidad, d.DetalleID "
        cadena += "from detalles d, cajas c, bolsas b, clasificaciones f, TiposCaja tc, tiposBolsa tb "
        cadena += "where d.CajaID = c.CajaID "
        cadena += "and d.BolsaID = b.BolsaID "
        cadena += "and d.ClasificacionID = f.ClasificacionID "
        cadena += f"and c.SeccionID = {id_seccion} and b.SeccionID = {id_seccion} and f.SeccionID = {id_seccion} "
        cadena += "and c.TipoCajaID = tc.TipoCajaID "
        cadena += "and b.TipoBolsaID = tb.TipoBolsaID "
        # print(cadena)
        if texto1:
            cadena += f" AND d.Descripcion LIKE '%{texto1}%'"
        if texto2:
            cadena += f" AND d.Descripcion LIKE '%{texto2}%'"
        if texto3:
            cadena += f" AND d.Detalle LIKE '%{texto3}%'"
        if self.id_caja_actual > 0:
            cadena += f" AND d.CajaID = {self.id_caja_actual}"        
        if self.id_bolsa_actual > 0:
            cadena += f" AND d.BolsaID = {self.id_bolsa_actual}"
        if self.id_clasificacion_actual > 0:
            cadena += f" AND d.ClasificacionID = {self.id_clasificacion_actual}"
        match self.intOrden.get():
            case 1:
                cadena += " ORDER BY upper(d.Descripcion)"
            case 2:
                cadena += " ORDER BY upper(f.Clasificacion)"
            case 3:
                cadena += " ORDER BY upper(d.Detalle)"
            case 4:
                cadena += " ORDER BY upper(c.Caja)"
            case 5:
                cadena += " ORDER BY upper(b.Bolsa)"
            case 6:
                cadena += " ORDER BY d.DetalleID"

        match self.intSentido.get():
            case 1:
                cadena += " ASC"
            case 2:
                cadena += " DESC"

        # print(cadena)

        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            self.botonDetalle.config(state=tk.ACTIVE)
            self.botonEliminar.config(state=tk.ACTIVE)
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(cadena)
            rows = cursor.fetchall()
            recuento = len(rows)
            if recuento == 0:
                self.texto_label_recuento.set("No se han encontrado registros")
            elif recuento == 1:
                self.texto_label_recuento.set("Se ha encontrado 1 registro")
            else:
                self.texto_label_recuento.set(f"Se han encontrado {recuento} registros")
            conn.close()

            for row in rows:
                self.tree.insert('', 'end', values=row)

            if not rows:
                self.botonDetalle.config(state=tk.DISABLED)
                self.botonEliminar.config(state=tk.DISABLED)
                messagebox.showinfo("Búsqueda", "No se encontraron resultados.")

        except Exception as e:
            messagebox.showerror("Error", f"Error en la consulta:\n{e}")

    def limpiar(self):
        self.entrada1.delete(0, tk.END)
        self.entrada2.delete(0, tk.END)
        self.entrada3.delete(0, tk.END)
        
        self.comboCajas.set('')
        self.comboBolsas.set('')
        self.comboClasificaciones.set('')
        
        self.id_caja_actual = 0
        self.id_bolsa_actual = 0
        self.id_clasificacion_actual = 0
        self.intOrden.set(6)
        self.intSentido.set(2)
        self.texto_label_recuento.set("")

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.botonDetalle.config(state=tk.DISABLED)

    def llenarCajas(self):
        try:
            id_seccion = self.app.id_seccion_actual
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cadena = f"SELECT CajaID, Caja FROM cajas WHERE SeccionID = {id_seccion} ORDER BY upper(Caja)"
            cursor.execute(cadena)
            rows = cursor.fetchall()
            conn.close()
            self.cajas = [""]
            self.idsCajas = {"": 0}
            for row in rows:
                self.cajas.append(row[1])
                self.idsCajas[row[1]] = row[0]
            self.comboCajas['values'] = self.cajas
            self.comboCajas.set("")
        except Exception as e:
            print("Error cargando cajas:", e)

    def llenarBolsas(self):
        try:
            id_seccion = self.app.id_seccion_actual
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cadena = f"SELECT BolsaID, Bolsa FROM bolsas WHERE SeccionID = {id_seccion} ORDER BY upper(Bolsa)"
            cursor.execute(cadena)
            rows = cursor.fetchall()
            conn.close()
            self.bolsas = [""]
            self.idsBolsas = {"": 0}
            for row in rows:
                self.bolsas.append(row[1])
                self.idsBolsas[row[1]] = row[0]
            self.comboBolsas['values'] = self.bolsas
            self.comboBolsas.set("")
        except Exception as e:
            print("Error cargando bolsas:", e)
    
    def llenarClasificacion(self):
        try:
            id_seccion = self.app.id_seccion_actual
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cadena = "SELECT ClasificacionID, Clasificacion FROM clasificaciones"
            cadena +=f" WHERE SeccionID = {id_seccion} ORDER BY upper(Clasificacion)"
            cursor.execute(cadena)
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

    def comboCajasClick(self, event):
        selected = self.comboCajas.get()
        self.id_caja_actual = self.idsCajas.get(selected, 0)
        self.buscar()

    def comboBolsasClick(self, event):
        selected = self.comboBolsas.get()
        self.id_bolsa_actual = self.idsBolsas.get(selected, 0)
        self.buscar()

    def comboClasificacionClick(self, event):
        selected = self.comboClasificaciones.get()
        self.id_clasificacion_actual = self.idsClasificacion.get(selected, 0)
        self.buscar()

    def on_double_click(self, event):
        self.editar_detalle_click()

    def on_right_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Editar", command=self.editar_item)
            menu.add_separator()
            menu.add_command(label="Eliminar", command=self.eliminar_item)
            menu.tk_popup(event.x_root, event.y_root)

    def editar_item(self):
        self.mostrar_editar_detalle_modal()

    def eliminar_item(self):
        self.eliminar_seleccionado()
    
    def editar_detalle_click(self):
        self.mostrar_editar_detalle_modal()

    def eliminar_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un registro primero")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar este registro?\n{self.tree.item(seleccion[0])['values']}"):
            valores = self.tree.item(seleccion[0])['values']
            desc, clasif, detalle, caja_actual, tipocaja, bolsa_actual, tipobolsa, cantidad, detalle_id = valores
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cadena = "delete from detalles "
                cadena += " where DetalleID = " + str(detalle_id)                
                # print(cadena)
                cursor.execute(cadena)
                conn.commit()
                conn.close()
                self.tree.delete(seleccion)
                messagebox.showinfo("Eliminar", "Registro eliminado correctamente")
                self.buscar()   # Refrescar lista

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def nuevo_registro(self):
        self.mostrar_nuevo_detalle_modal()

    def mostrar_editar_detalle_modal(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un registro primero")
            return

        valores = self.tree.item(seleccion[0])['values']

        if not valores or len(valores) < 8:
            return

        desc, clasif, detalle, caja_actual, tipocaja, bolsa_actual, tipobolsa, cantidad, detalle_id = valores

        # Crear ventana modal
        modal = tk.Toplevel(self)
        modal.title("Editar Detalle")
        modal.geometry("580x430")
        modal.resizable(False, False)
        modal.transient(self)
        modal.grab_set()

        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (580 // 2)
        y = (modal.winfo_screenheight() // 2) - (430 // 2)
        modal.geometry(f"580x430+{x}+{y}")

        frame = ttk.Frame(modal, padding=20)
        frame.pack(fill="both", expand=True)

        # Variables
        var_desc = tk.StringVar(value=desc)
        var_clasif = tk.StringVar(value=clasif)
        var_detalle = tk.StringVar(value=detalle)
        var_caja = tk.StringVar(value=caja_actual)
        var_bolsa = tk.StringVar(value=bolsa_actual)
        var_cantidad = tk.StringVar(value=cantidad)
        self.var_tipo_caja = tk.StringVar(value=tipocaja)
        self.var_tipo_bolsa = tk.StringVar(value=tipobolsa)

        # print(self.var_tipo_bolsa.get())

        # Descripción
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Descripción", width=13, anchor="e").pack(side="left")
        entry_desc = ttk.Entry(row, textvariable=var_desc, width=45)
        entry_desc.pack(side="left", padx=10, fill="x", expand=True)

        # Detalle
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Detalle", width=13, anchor="e").pack(side="left")
        entry_detalle = ttk.Entry(row, textvariable=var_detalle, width=55)
        entry_detalle.pack(side="left", padx=10, fill="x", expand=True)

        # Clasificacion (Combobox)
        row_clasificacion = ttk.Frame(frame)
        row_clasificacion.pack(fill="x", pady=7)
        ttk.Label(row_clasificacion, text="Clasificación", width=13, anchor="e").pack(side="left")
        self.combo_clasificacion_modal = ttk.Combobox(row_clasificacion, textvariable=var_clasif, 
                                              values=self.clasificacion, state="readonly", width=42)
        self.combo_clasificacion_modal.pack(side="left", padx=10)

        # Caja (Combobox)
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Caja", width=13, anchor="e").pack(side="left")
        self.combo_caja_modal = ttk.Combobox(row, textvariable=var_caja, 
                                             values=self.cajas, state="readonly", width=42)
        self.combo_caja_modal.pack(side="left", padx=10)
        
        # ← Evento al cambiar selección de Caja
        self.combo_caja_modal.bind("<<ComboboxSelected>>", 
                                   lambda e: self.on_caja_changed_modal(var_bolsa, modal))
        
        # TipoCaja
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Tipo Caja", width=13, anchor="e").pack(side="left")
        ttk.Label(row, textvariable=self.texto_labelCaja).pack(side="left", padx=10)
        self.texto_labelCaja.set(value=self.var_tipo_caja.get())

        # Bolsa (Combobox)
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Bolsa", width=13, anchor="e").pack(side="left")
        self.combo_bolsa_modal = ttk.Combobox(row, textvariable=var_bolsa, 
                                   values=self.bolsas, state="readonly", width=42)
        self.combo_bolsa_modal.pack(side="left", padx=10)

        # ← Evento al cambiar selección de Bolsa
        self.combo_bolsa_modal.bind("<<ComboboxSelected>>", 
                                   lambda e: self.on_bolsa_changed_modal(var_caja, modal))

        # TipoBolsa
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Tipo Bolsa", width=13, anchor="e").pack(side="left")
        ttk.Label(row, textvariable=self.texto_labelBolsa).pack(side="left", padx=10)
        self.texto_labelBolsa.set(value=self.var_tipo_bolsa.get())

        # Cantidad
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Cantidad", width=13, anchor="e").pack(side="left")
        entry_cantidad = ttk.Entry(row, textvariable=var_cantidad, width=55)
        entry_cantidad.pack(side="left", padx=10, fill="x", expand=False)

        # ID (solo lectura)
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="ID", width=13, anchor="e").pack(side="left")
        ttk.Label(row, text=str(detalle_id), foreground="gray").pack(side="left", padx=10)

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=15)

        # ==================== BOTONES ====================
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        def guardar_cambios():
            nuevo_desc = var_desc.get().strip()
            nuevo_clasif = var_clasif.get().strip()
            nuevo_detalle = var_detalle.get().strip()
            nueva_caja = var_caja.get()
            nueva_bolsa = var_bolsa.get()
            nueva_cantidad = var_cantidad.get()

            if not nuevo_desc or not nuevo_detalle or not nueva_cantidad:
                messagebox.showwarning("Error", "Descripción, Detalle y Cantidad son obligatorios")
                return

            if not nueva_caja or not nueva_bolsa or not nuevo_clasif:
                messagebox.showwarning("Error", "Se debe seleccionar Caja, Bolsa y Clasificación")
                return

            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cadena = "update detalles "
                cadena += "set Descripcion = '" + nuevo_desc + "', " 
                cadena += "ClasificacionID = " + str(self.idsClasificacion.get(nuevo_clasif, 0)) + ", "
                cadena += "Detalle = '" + nuevo_detalle + "', "
                cadena += "CajaID = " + str(self.idsCajas.get(nueva_caja, 0)) + ", "
                cadena += "Cantidad = " + str(nueva_cantidad)  + ", "
                cadena += "BolsaID = " + str(self.idsBolsas.get(nueva_bolsa, 0))
                cadena += " where DetalleID = " + str(detalle_id)                
                cursor.execute(cadena)
                conn.commit()
                conn.close()

                messagebox.showinfo("Guardar", "Registro actualizado correctamente")
                modal.destroy()
                self.buscar()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        ttk.Button(btn_frame, text="Guardar", command=guardar_cambios, 
                   width=15).pack(side="left", padx=8)
        
        ttk.Button(btn_frame, text="Cancelar", command=modal.destroy, 
                   width=15).pack(side="left", padx=8)

        # Atajos de teclado
        modal.bind("<Escape>", lambda e: modal.destroy())
        modal.bind("<Control-s>", lambda e: guardar_cambios())

        # Enfocar primer campo
        entry_desc.focus_set()

    def mostrar_nuevo_detalle_modal(self):
        """Ventana modal para crear un Nuevo Detalle"""
        modal = tk.Toplevel(self)
        modal.title("Nuevo Detalle")
        modal.geometry("580x445")
        modal.resizable(False, False)
        modal.transient(self)
        modal.grab_set()

        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (580 // 2)
        y = (modal.winfo_screenheight() // 2) - (445 // 2) - 40
        modal.geometry(f"580x445+{x}+{y}")

        frame = ttk.Frame(modal, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nuevo Registro", 
                  font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))

        var_desc = tk.StringVar()
        var_clasif = tk.StringVar()
        var_detalle = tk.StringVar()
        var_caja = tk.StringVar()
        var_bolsa = tk.StringVar()
        var_cantidad = tk.StringVar()
        self.var_tipo_caja = tk.StringVar(value="0")
        self.var_tipo_bolsa = tk.StringVar(value="0")

        # Descripción
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Descripción", width=13, anchor="e").pack(side="left")
        entry_desc = ttk.Entry(row, textvariable=var_desc, width=45)
        entry_desc.pack(side="left", padx=10, fill="x", expand=True)

        # Detalle
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Detalle", width=13, anchor="e").pack(side="left")
        entry_detalle = ttk.Entry(row, textvariable=var_detalle, width=55)
        entry_detalle.pack(side="left", padx=10, fill="x", expand=True)

        # Clasificación (Combobox)
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Clasificación", width=13, anchor="e").pack(side="left")
        combo_clasif = ttk.Combobox(row, textvariable=var_clasif, 
                                    values=self.clasificacion, state="readonly", width=42)
        combo_clasif.pack(side="left", padx=10)

        # Caja (Combobox)
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Caja", width=13, anchor="e").pack(side="left")
        self.combo_caja_modal = ttk.Combobox(row, textvariable=var_caja, 
                                             values=self.cajas, state="readonly", width=42)
        self.combo_caja_modal.pack(side="left", padx=10)
        
        # ← Evento al cambiar selección de Caja
        self.combo_caja_modal.bind("<<ComboboxSelected>>", 
                                   lambda e: self.on_caja_changed_modal(var_bolsa, modal))
        
        # TipoCaja
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Tipo Caja", width=13, anchor="e").pack(side="left")
        ttk.Label(row, textvariable=self.texto_labelCaja).pack(side="left", padx=10)
        self.texto_labelCaja.set(value=self.var_tipo_caja.get())

        # Bolsa (Combobox)
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Bolsa", width=13, anchor="e").pack(side="left")
        self.combo_bolsa_modal = ttk.Combobox(row, textvariable=var_bolsa, 
                                   values=self.bolsas, state="readonly", width=42)
        self.combo_bolsa_modal.pack(side="left", padx=10)

        # ← Evento al cambiar selección de Bolsa
        self.combo_bolsa_modal.bind("<<ComboboxSelected>>", 
                                   lambda e: self.on_bolsa_changed_modal(var_caja, modal))

        # TipoBolsa
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Tipo Bolsa", width=13, anchor="e").pack(side="left")
        ttk.Label(row, textvariable=self.texto_labelBolsa).pack(side="left", padx=10)
        self.texto_labelBolsa.set(value=self.var_tipo_bolsa.get())

        # Cantidad
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text="Cantidad", width=13, anchor="e").pack(side="left")
        entry_cantidad = ttk.Entry(row, textvariable=var_cantidad, width=15)
        entry_cantidad.pack(side="left", padx=10)

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=15)

        # ==================== BOTONES ====================
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        def guardar_nuevo():
            nuevo_desc = var_desc.get().strip()
            nuevo_detalle = var_detalle.get().strip()
            nuevo_clasif = var_clasif.get()
            nueva_caja = var_caja.get()
            nueva_bolsa = var_bolsa.get()
            nueva_cantidad = var_cantidad.get().strip()

            if not nuevo_desc or not nuevo_detalle:
                messagebox.showwarning("Error", "Descripción y Detalle son obligatorios")
                return

            if not nueva_caja or not nueva_bolsa or not nuevo_clasif:
                messagebox.showwarning("Error", "Debe seleccionar Clasificación, Caja y Bolsa")
                return

            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO detalles 
                    (Descripcion, ClasificacionID, Detalle, CajaID, BolsaID, Cantidad)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    nuevo_desc,
                    self.idsClasificacion.get(nuevo_clasif, 0),
                    nuevo_detalle,
                    self.idsCajas.get(nueva_caja, 0),
                    self.idsBolsas.get(nueva_bolsa, 0),
                    int(nueva_cantidad) if nueva_cantidad.isdigit() else 1
                ))
                
                conn.commit()
                conn.close()

                messagebox.showinfo("Éxito", "Registro creado correctamente")
                modal.destroy()
                self.buscar()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

        ttk.Button(btn_frame, text="Guardar", command=guardar_nuevo, 
                   width=15).pack(side="left", padx=8)
        
        ttk.Button(btn_frame, text="Cancelar", command=modal.destroy, 
                   width=15).pack(side="left", padx=8)

        # Atajos
        modal.bind("<Escape>", lambda e: modal.destroy())
        modal.bind("<Control-s>", lambda e: guardar_nuevo())

        # Enfocar primer campo
        entry_desc.focus_set()

    def on_caja_changed_modal(self, var_bolsa, modal):
        caja_seleccionada = self.combo_caja_modal.get()
        caja_seleccionada_id = self.idsCajas.get(caja_seleccionada, 0)
        
        if not caja_seleccionada:
            self.texto_labelCaja.set("")
            return
        
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cadena = f"select t.TipoCaja from cajas c, tiposCaja t "
            cadena += f"where c.TipoCajaID = t.TipoCajaID and c.CajaID = {caja_seleccionada_id}"
            cursor.execute(cadena)
            tipo_caja = cursor.fetchone()[0]
            self.texto_labelCaja.set(tipo_caja)
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar cajas: {e}")

    def on_bolsa_changed_modal(self, var_bolsa, modal):
        """Se ejecuta cuando el usuario selecciona una Bolsa en la modal"""
        bolsa_seleccionada = self.combo_bolsa_modal.get()
        bolsa_seleccionada_id = self.idsBolsas.get(bolsa_seleccionada, 0)
        
        if not bolsa_seleccionada:
            self.texto_labelBolsa.set("")
            return
        
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cadena = f"select t.TipoBolsa from bolsas c, tiposBolsa t "
            cadena += f"where c.TipoBolsaID = t.TipoBolsaID and c.BolsaID = {bolsa_seleccionada_id}"
            cursor.execute(cadena)
            tipo_bolsa = cursor.fetchone()[0]
            self.texto_labelBolsa.set(tipo_bolsa)
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar bolsas: {e}")