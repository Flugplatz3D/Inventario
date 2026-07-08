import sqlite3

conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

i=0
cursor.execute("select * from detalles")
# rows = cursor.fetchall()
# rows = cursor.fetchone()[0]
# for row in rows:
#     i+=1
#     print(f"columna1:{row[0]} - columna2:{row[4]} - columna3:{row[5]} -- Recuento:{i}")
#     # print(row)

row = cursor.fetchone()

print(f"columna1:{row[0]} || columna2:{row[4]} || columna3:{row[5]} || Recuento:{i}")

#print(f"Número de registros: {len(rows)}")

# print(row)

conn.close()
print("Fin\n")