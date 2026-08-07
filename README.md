Aplicación Inventario Python/SQLite3/TTK-TKinter

Esta hecha para WINDOWS!!! En Linux funciona sin problema, pero hay que comentar la linea 14 de "inventario.py" y en "tab_detalle.py" hay que recolocar algunos componentes ya que el ttk no se comporta exactamente igual que en Windows.

Para compilar en Windows:

cd C:\gitub\Inventario  <-- Donde esten todos los archivos

pyinstaller --onefile --windowed --clean --icon=warehouse_storage.ico --name Inventario --add-data "inventario.db;." inventario.py

mover EXE de carpeta dist

Para instalar pyinstaller en Windows:

python -m pip install --upgrade pip

cd "C:\Program Files\Python314\Scripts"
o
cd C:\Users\Mario\AppData\Local\Programs\Python\Python314\scripts

pip install pyinstaller --force-reinstall


En Linux/Debian no se instala Tkinter automaticamente.

Instalar Tkinter en Debian:
sudo apt-get install python3-tk 
