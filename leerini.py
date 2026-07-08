import configparser

# 1. Inicializar el parser
config = configparser.ConfigParser()

# 2. Leer el archivo
# (Nota: read() no lanza error si el archivo no existe, simplemente no carga nada)
config.read('config.ini')

# 3. Acceder a los valores (siempre se devuelven como cadenas de texto por defecto)
db_host = config['DATABASE']['host']
print(f"Host de la base de datos: {db_host}")

# 4. Usar métodos para convertir tipos de datos automáticamente
db_port = config.getint('DATABASE', 'port')       # Convierte a entero (int)
api_timeout = config.getint('API', 'timeout')     # Convierte a entero (int)
api_debug = config.getboolean('API', 'debug')     # Convierte a booleano (True/False)

print(f"Puerto: {db_port} (tipo: {type(db_port)})")
print(f"Debug API: {api_debug} (tipo: {type(api_debug)})")

# 5. Usar valores por defecto (fallback) por si la clave o sección no existe
max_retries = config.getint('API', 'max_retries', fallback=5)
print(f"Reintentos máximos: {max_retries}")