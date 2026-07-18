Aplicación Inventario Python/SQLite3/TTK-TKinter
Mucha ayuda de xAI mediante GROK.

Para compilar:

cd C:\gitub\Inventario

pyinstaller --onefile --windowed --clean --icon=warehouse_storage.ico --name Inventario --add-data "inventario.db;." inventario.py

mover EXE de carpeta dist

Para instalar pyinstaller:

cd "C:\Program Files\Python314\Scripts"
o
cd C:\Users\Mario\AppData\Local\Programs\Python\Python314\scripts

pip install pyinstaller --force-reinstall
