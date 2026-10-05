x = 5
x= "hola"
print (x)
print(type(x)) 
print(isinstance(x, int))

# Python
mas_grande = None
if mas_grande is None:
    print("Todavía no hay candidato.")


edad = int(input ("Introduce tu edad: "))
if (edad < 18):
    print("fuera")
else:
    socio = input ("Eres socio? si/no ")
    if socio =="si":
        print ("Entra")
    else:
        print("fuera")

#VAMOS a permitir la entrada a un local solo si los 
#usuarios tienen más de 18 años y son socios.
#El programa pregunta al usuario si tiene 18 años.
#si es menor -> adiós. 
#Si es mayor -> preguntamos si es socio
#Si es socio -> bienvenido sino adios


#Pide (input)una palabra de mínimo 5 letras al usuario
#Si tiene menos de 5 (tamaño se mira con len(palabra)
#se le vuelve a pedir
#EJEMPLO:
x = 5
while x > 0:
    x -=1
    print(x)

palabra=""
while (len(palabra)<5):
    palabra = input("Introduce una palabra de mas de 5 letras: ")

#Muestra las 3 primeras letras
print(palabra[0:3])
#Muestra qué tipo de variable es
print(type(palabra))
#Si la palabra tiene letras pares muestra las pares, sino las impares1
if(palabra%2 ==0):
    posicion=1
else:
    posicion=0
while (posicion<len(palabra)):
    print(palabra[posicion])
    posicion = posicion+2