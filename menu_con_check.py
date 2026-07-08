import tkinter as tk
from tkinter import ttk

def actualizar():
    print("Barra de estado:", estado.get())
    print("Modo oscuro:", oscuro.get())

ventana = tk.Tk()
ventana.title("Menú con Checkbuttons")
ventana.geometry("450x250")

# Variables asociadas a los checks
estado = tk.BooleanVar(value=True)
oscuro = tk.BooleanVar(value=False)

# Widget ttk
ttk.Label(
    ventana,
    text="Ejemplo de menús con opciones marcables"
).pack(pady=30)

# Barra de menús
barra = tk.Menu(ventana)

# Menú Ver
menu_ver = tk.Menu(barra, tearoff=0)

menu_ver.add_checkbutton(
    label="Mostrar barra de estado",
    variable=estado,
    command=actualizar
)

menu_ver.add_checkbutton(
    label="Modo oscuro",
    variable=oscuro,
    command=actualizar
)

barra.add_cascade(label="Ver", menu=menu_ver)

# Menú Archivo
menu_archivo = tk.Menu(barra, tearoff=0)
menu_archivo.add_command(label="Salir", command=ventana.destroy)

barra.add_cascade(label="Archivo", menu=menu_archivo)

tema = tk.StringVar(value="Claro")

menu_ver.add_separator()

#solo una opcion marcada
menu_ver.add_radiobutton(
    label="Tema claro",
    variable=tema,
    value="Claro"
)

menu_ver.add_radiobutton(
    label="Tema oscuro",
    variable=tema,
    value="Oscuro"
)

menu_ver.add_radiobutton(
    label="Tema del sistema",
    variable=tema,
    value="Sistema"
)

ventana.config(menu=barra)

ventana.mainloop()