from logging import root
import tkinter as tk
from tkinter import ttk, messagebox
from tab_detalle import TabDetalle
from tab_auxiliares import TabAuxiliares
import configparser
import sqlite3

DB_NAME = "inventario.db"

class InventarioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('warehouse_storage.ico')
        self.title("Inventario")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 1240
        height = 600
        x = (screen_width/2) - (width/2) - 10
        y = (screen_height/2) - (height/2) - 40
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.resizable(False, False)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.seccion = tk.StringVar()
        self.seccion.set(self.leer_config("CONFIGURACION", "seccion_inicial", ""))

        self.id_seccion_actual = self.leer_id_seccion(self.seccion.get())
        self.secciones = []
        self.ids_seccion = {}

        # Pestaña Detalle
        self.tab_detalle = TabDetalle(self.notebook, self)
 
        # Pestaña Auxiliares        
        self.tab_aux = TabAuxiliares(self.notebook,self)
        
        self.notebook.add(self.tab_detalle, text="📝 Detalle")
        self.notebook.add(self.tab_aux, text="⚙️ Auxiliares")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        barra_menus = tk.Menu()
        self.config(menu=barra_menus)
        menu_opciones = tk.Menu(barra_menus, tearoff=False)
        menu_opciones.add_command(
                    label="Cambiar Sección",
                    command=self.modal_configuracion,
                    compound=tk.LEFT
                )
        menu_opciones.add_command(
                    label="Generar CSV",
                    command=self.modal_csv,
                    compound=tk.LEFT
                )
        self.bind_all("<Control-n>", self.modal_configuracion)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Salir", command=self.destroy)

        barra_menus.add_cascade(label="Utilidades", menu=menu_opciones)
        menu_ayuda = tk.Menu(barra_menus, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.modal_acerca_de)
        barra_menus.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.title(f"Inventario ({self.seccion.get()})")

        self.tab_aux.seccion_actual_labelID.set(self.seccion.get())

    def leer_id_seccion(self, seccion_inicial):
        if seccion_inicial:
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("SELECT SeccionID FROM Secciones WHERE Seccion = ?", (seccion_inicial,))
                result = cursor.fetchone()
                conn.close()
                if result:
                    return result[0]
            except Exception as e:
                messagebox.showerror("Error", f"Error al leer el ID de la sección:\n{e}")

        return 0

    def leer_config(self, entrada, clave, valor_por_defecto):
        config = configparser.ConfigParser()
        config.read("config.ini")
        try:
            valor = config.get(entrada, clave, fallback=valor_por_defecto)
        except Exception:
            valor = valor_por_defecto
        return valor

    def modal_acerca_de(self):
        ventana_modal = tk.Toplevel(self)
        ventana_modal.title("Acerca de ...")
        width = 280
        height = 150
        screen_width = ventana_modal.winfo_screenwidth()
        screen_height = ventana_modal.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2) - 60
        ventana_modal.geometry('%dx%d+%d+%d' % (width, height, x, y))
        ventana_modal.resizable(False, False)
        label = tk.Label(ventana_modal, text="Inventario App Versión 1.1.7\n© 2026\n(Flugplatz3D)", font=("Arial", 11), justify="center")
        label.pack(pady=10)
        tk.Button(ventana_modal, text="Cerrar", command=ventana_modal.destroy, width=10).pack(pady=20)
        # Esto bloquea la ventana principal
        ventana_modal.grab_set()
        ventana_modal.focus()

    def modal_configuracion(self, event = None):
        ventana_modal = tk.Toplevel(self)
        ventana_modal.title("Cambiar Sección")
        width = 380
        height = 150
        screen_width = ventana_modal.winfo_screenwidth()
        screen_height = ventana_modal.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2) - 60
        ventana_modal.geometry('%dx%d+%d+%d' % (width, height, x, y))
        ventana_modal.resizable(False, False)

        ventana_modal.columnconfigure(0, weight=1)
        ventana_modal.columnconfigure(1, weight=1)
        ventana_modal.columnconfigure(2, weight=1)
        ventana_modal.rowconfigure(0, weight=1)
        ventana_modal.rowconfigure(1, weight=1)
        ventana_modal.rowconfigure(2, weight=1)
        ventana_modal.rowconfigure(3, weight=1)

        label = ttk.Label(ventana_modal, text="Sección:")
        label.grid(row=0, column=0, sticky="W", padx=12, pady=10)

        self.combo_secciones = ttk.Combobox(ventana_modal, values=[], width=30)
        self.combo_secciones.grid(row=0, column=1, sticky="EW", padx=10, pady=15, columnspan=2)
        self.combo_secciones.config(state="readonly")
        self.combo_secciones.bind("<<ComboboxSelected>>", self.combo_secciones_click)

        # Botón Guardar
        boton_aceptar = ttk.Button(
                                ventana_modal, 
                                text="Aceptar", 
                                command=lambda: self.guardar_configuracion(ventana_modal, self.combo_secciones.get()))
        boton_aceptar.grid(row=3, column=1, sticky="E", padx=10, pady=15)

        # Botón Cancelar
        boton_cancelar = ttk.Button(ventana_modal, text="Cancelar", command=ventana_modal.destroy)
        boton_cancelar.grid(row=3, column=2, sticky="W", padx=10, pady=15)
        
        self.llenar_secciones()
        self.combo_secciones.set(self.seccion.get())  # Establece la sección inicial desde config.ini
        
        # Esto bloquea la ventana principal
        ventana_modal.grab_set()
        ventana_modal.focus()

    def modal_csv(self,event = None):
        messagebox.showinfo("Generar CSV", "Pendiente de desarrollo")

    def combo_secciones_click(self, event):
        selected = self.combo_secciones.get()
        self.id_seccion_actual = self.ids_seccion.get(selected, 0)

    def llenar_secciones(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cadena = "SELECT SeccionID, Seccion FROM Secciones ORDER BY upper(Seccion)"
            cursor.execute(cadena)
            rows = cursor.fetchall()
            conn.close()

            self.secciones = [row[1] for row in rows]
            self.ids_seccion = {row[1]: row[0] for row in rows}

            self.combo_secciones['values'] = self.secciones
            
        except Exception as e:
            messagebox.showerror("Error",f"Error cargando secciones\n{e}")

    def guardar_configuracion(self, ventana_modal, seccion):
        
        config = configparser.ConfigParser()
        config.read("config.ini")
        
        if not config.has_section("CONFIGURACION"):
            config.add_section("CONFIGURACION")
        
        config.set("CONFIGURACION", "seccion_inicial", seccion)
        
        with open("config.ini", "w", encoding="utf-8") as f:
            config.write(f)
        
        self.seccion.set(seccion)   # Actualizamos la variable interna

        self.title(f"Inventario ({self.seccion.get()})")  # Actualizamos el título de la ventana principal

        self.tab_detalle.limpiar()  # Limpia los campos en la pestaña Detalle
        self.tab_detalle.llenarCajas()  # Actualiza las cajas en la pestaña Detalle
        self.tab_detalle.llenarBolsas()  # Actualiza las bolsas en la pestaña Detalle
        self.tab_detalle.llenarClasificacion()  # Actualiza las clasificaciones en la pestaña Detalle

        self.id_seccion_actual = self.ids_seccion.get(seccion, 0)  # Actualiza el ID de la sección actual
        self.tab_aux.llenar_cajas()
        self.tab_aux.llenar_bolsas()
        self.tab_aux.llenar_clasificacion()
        self.tab_aux.nuevo_caja()
        self.tab_aux.nuevo_bolsa()
        self.tab_aux.nuevo_clasificacion()
        self.tab_aux.nuevo_seccion()
        self.tab_aux.seccion_actual_labelID.set(self.seccion.get())

        ventana_modal.destroy()

    def on_tab_changed(self, event):
        if self.notebook.select() == str(self.tab_detalle):
            valor = self.tab_detalle.comboCajas.get()
            self.tab_detalle.llenarCajas()
            if valor:
                self.tab_detalle.comboCajas.set(valor)
            valor = self.tab_detalle.comboBolsas.get()
            self.tab_detalle.llenarBolsas()
            if valor:
                self.tab_detalle.comboBolsas.set(valor)
            valor = self.tab_detalle.comboClasificaciones.get()
            self.tab_detalle.llenarClasificacion()
            if valor:
                self.tab_detalle.comboClasificaciones.set(valor)

            if len(self.tab_detalle.tree.get_children()) > 0:
                self.tab_detalle.buscar()

        # if self.notebook.select() == str(self.tab_aux):
        #     print("En tab_aux")
    
if __name__ == "__main__":
    app = InventarioApp()
    app.mainloop()