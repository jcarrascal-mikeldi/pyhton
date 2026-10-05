import json

with open("datos.json", encoding="utf-8") as f:
    datos = json.load(f)

por_tipo = {}

for escenario in datos["escenarios"]:
    tipo = escenario["tipo"]
    por_tipo[tipo] = por_tipo.get(tipo, 0) + 1

for genero, cantidad in por_tipo.items():
    print(f"{genero}: {cantidad}")