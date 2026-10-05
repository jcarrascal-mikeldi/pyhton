grupoMusical="La oreja de van gogh"
print("Longitud: ",len(grupoMusical))
print(grupoMusical[0:3])
print(grupoMusical[-3:])

horaInicio = input("Introduce la hora de inicio: ")
horaFin = input("Introduce la hora de fin: ")
horasInicio=int(horaInicio[0:2])
minutosInicio=int(horaInicio[3:5])
horasFin=int(horaFin[0:2])
minutosFin=int(horaFin[3:5])
horas=horasFin-horasInicio
minutos=minutosFin-minutosInicio
print("Horas: ", horas)
print("Minutos: ", minutos)

#Crea una lista llamada nombres con nombres random de alumnos
nombres = ["Ana", "Juan", "Pedro", "Maria", "Luis", "Sofia", "Carlos", "Lucia"]

#De esa lista, crea otra lista llamada nombresCortos que contenga 
# los nombres de menos de 5 letras
for nombre in nombres:
    if len(nombre) < 5:
        print(nombre)

#Muestra las 3 primeras letras de cada nombre
for nombre in nombres:
    print(nombre[0:3])

#Crea otra lista con los apellidos
apellidos = ["Garcia", "Lopez", "Rodriguez", "Martinez", "Sanchez", "Perez", "Gonzalez", "Rodriguez"]

#Muestra en cada linea cada nombre con su apellido 
# (compartiran posicion) en arrays diferentes
for i in range(len(nombres)):
    print(nombres[i], apellidos[i])