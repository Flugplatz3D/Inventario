import configparser

config = configparser.ConfigParser()

# 1. Agregar secciones y claves usando diccionarios
config['DATABASE'] = {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': 'mi_password_seguro'
}

# 2. También puedes agregar secciones y claves una por una
config['LOGGING'] = {}
config['LOGGING']['level'] = 'gusano'
config['LOGGING']['file'] = 'patata.log'

# # 3. Guardar los datos en un archivo
# with open('nuevo_config.ini', 'w') as configfile:
#     config.write(configfile)

config.write(open('config.ini', 'w'))  # 'a' para agregar al final del archivo existente

print("Archivo 'config.ini' creado con éxito.")