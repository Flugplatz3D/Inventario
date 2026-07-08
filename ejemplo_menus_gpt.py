import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def nuevo():
    messagebox.showinfo("Nuevo", "Crear un nuevo archivo")

def abrir():
    messagebox.showinfo("Abrir", "Abrir un archivo")

def salir():
    ventana.quit()

def acerca_de():
    messagebox.showinfo("Acerca de", "Ejemplo de menú con Tkinter y ttk")

# Ventana principal
ventana = tk.Tk()
ventana.title("Ejemplo de Menús")
ventana.geometry("500x300")

# Widget ttk
frame = ttk.Frame(ventana, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Ejemplo de barra de menús con ttk").pack(pady=10)

ttk.Button(frame, text="Botón ttk").pack()

# Barra de menú
barra_menu = tk.Menu(ventana)

# Menú Archivo
menu_archivo = tk.Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Nuevo", command=nuevo)
menu_archivo.add_command(label="Abrir", command=abrir)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=salir)

barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

menu_editar = tk.Menu(barra_menu, tearoff=0)

submenu_formato = tk.Menu(menu_editar, tearoff=0)
submenu_formato.add_command(label="Negrita")
submenu_formato.add_command(label="Cursiva")

menu_editar.add_cascade(label="Formato", menu=submenu_formato)
barra_menu.add_cascade(label="Editar", menu=menu_editar)

menu_contextual = tk.Menu(ventana, tearoff=0)
menu_contextual.add_command(label="Copiar")
menu_contextual.add_command(label="Pegar")

def mostrar_menu(event):
    menu_contextual.post(event.x_root, event.y_root)

ventana.bind("<Button-3>", mostrar_menu)  # Windows/Linux
# En macOS suele utilizarse <Button-2>

# Menú Ayuda
menu_ayuda = tk.Menu(barra_menu, tearoff=0)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)

barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

# Asignar la barra de menú
ventana.config(menu=barra_menu)

ventana.mainloop()