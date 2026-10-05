"""
Tests de la actividad 1.1 · Python 2º DAM · Mikeldi

Cómo se usan:
    python -m pytest -v            (en Windows también vale: py -m pytest -v)

Cada ejercicio tiene dos tests:
  - datos_reales: el programa con el datos.json del festival.
  - otros_datos:  el programa con un datos.json modificado. Si los
                  resultados están escritos de forma literal, este test falla.

No es necesario entender este fichero para hacer la actividad.
No debe modificarse: es el que se utiliza en la corrección.
"""

import copy
import json
import os
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest

CARPETA = Path(__file__).parent
DATOS = json.loads((CARPETA / "datos.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- utilidades

def normaliza(texto):
    """Minúsculas, guiones unificados y espacios simples (las tildes se respetan)."""
    texto = unicodedata.normalize("NFC", texto).casefold()
    for guion in ("—", "–", "−"):
        texto = texto.replace(guion, "-")
    return " ".join(texto.split())


def ejecuta(nombre, tmp_path, datos=None):
    """Copia ejN.py a una carpeta temporal con su datos.json y devuelve las líneas que imprime."""
    script = CARPETA / nombre
    if not script.exists():
        pytest.fail(f"Todavía no existe {nombre} en la carpeta {CARPETA}")
    shutil.copy(script, tmp_path / nombre)
    (tmp_path / "datos.json").write_text(
        json.dumps(datos if datos is not None else DATOS, ensure_ascii=False),
        encoding="utf-8",
    )
    r = subprocess.run(
        [sys.executable, nombre],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=20,
        env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
    )
    if r.returncode != 0:
        ultima = (r.stderr.strip().splitlines() or ["(sin mensaje)"])[-1]
        pytest.fail(f"{nombre} termina con un error: {ultima}")
    lineas = [normaliza(l) for l in r.stdout.splitlines() if l.strip()]
    if not lineas:
        pytest.fail(f"{nombre} no imprime nada")
    return lineas


def hay_linea(lineas, *trozos):
    trozos = [normaliza(str(t)) for t in trozos]
    return any(all(t in l for t in trozos) for l in lineas)


def linea_con_numero(lineas, clave, numero):
    """Hay una línea que contiene la clave y el número como palabra suelta."""
    clave = normaliza(clave)
    for l in lineas:
        if clave in l:
            palabras = l.replace(":", " ").replace(",", " ").replace("(", " ").replace(")", " ").split()
            if str(numero) in palabras:
                return True
    return False


# ------------------------------------------------------------- ejercicio 1

def _cuenta_tipos(datos):
    cuenta = {}
    for e in datos["escenarios"]:
        cuenta[e["tipo"]] = cuenta.get(e["tipo"], 0) + 1
    return cuenta


def test_ej1_datos_reales(tmp_path):
    lineas = ejecuta("ej1.py", tmp_path)
    for tipo, n in _cuenta_tipos(DATOS).items():
        assert linea_con_numero(lineas, tipo, n), f"Falta una línea con «{tipo}» y {n}"


def test_ej1_otros_datos(tmp_path):
    datos = copy.deepcopy(DATOS)
    datos["escenarios"] += [
        {"nombre": "Ría", "capacidad": 5000, "tipo": "principal"},
        {"nombre": "Txoko", "capacidad": 300, "tipo": "acústico"},
        {"nombre": "Dársena", "capacidad": 900, "tipo": "acústico"},
    ]
    lineas = ejecuta("ej1.py", tmp_path, datos)
    for tipo, n in _cuenta_tipos(datos).items():
        assert linea_con_numero(lineas, tipo, n), (
            f"Con otros datos debería salir «{tipo}» con {n}: ¿están escritos los números de forma literal?"
        )


# ------------------------------------------------------------- ejercicio 2

def _lineas_ej2(datos):
    esperadas = []
    for a in datos["actuaciones"]:
        momento = "tarde" if a["hora_inicio"] < "20:00" else "noche"
        esperadas.append(normaliza(f'{a["artista"]} en {a["escenario"]} ({a["dia"]}) — {momento}'))
    return esperadas


def test_ej2_datos_reales(tmp_path):
    lineas = ejecuta("ej2.py", tmp_path)
    for esperada in _lineas_ej2(DATOS):
        assert esperada in lineas, f"Falta la línea: {esperada}"


def test_ej2_otros_datos(tmp_path):
    datos = copy.deepcopy(DATOS)
    datos["actuaciones"] += [
        {"artista": "Lasai", "escenario": "Faro", "dia": "domingo", "hora_inicio": "19:59", "hora_fin": "20:40"},
        {"artista": "Errimuxu", "escenario": "Muelle", "dia": "viernes", "hora_inicio": "20:00", "hora_fin": "20:45"},
    ]
    lineas = ejecuta("ej2.py", tmp_path, datos)
    for esperada in _lineas_ej2(datos):
        assert esperada in lineas, f"Con otros datos falta la línea: {esperada}"


# ------------------------------------------------------------- ejercicio 3

def _cuenta_escenarios(datos):
    cuenta = {}
    for a in datos["actuaciones"]:
        cuenta[a["escenario"]] = cuenta.get(a["escenario"], 0) + 1
    return cuenta


def _linea_maximo(lineas):
    candidatas = [l for l in lineas if "más" in l or "mas " in l or "max" in l]
    return candidatas[-1] if candidatas else lineas[-1]


def test_ej3_datos_reales(tmp_path):
    lineas = ejecuta("ej3.py", tmp_path)
    for escenario, n in _cuenta_escenarios(DATOS).items():
        assert linea_con_numero(lineas, escenario, n), f"Falta una línea con «{escenario}» y {n}"
    maximo = max(_cuenta_escenarios(DATOS).values())
    ganadores = [e for e, n in _cuenta_escenarios(DATOS).items() if n == maximo]
    ultima = _linea_maximo(lineas)
    assert any(normaliza(g) in ultima for g in ganadores), (
        f"La línea del escenario con más actuaciones debería nombrar a {' o '.join(ganadores)}"
    )


def test_ej3_otros_datos(tmp_path):
    datos = copy.deepcopy(DATOS)
    for hora in ("16:00", "17:00", "18:00"):
        datos["actuaciones"].append(
            {"artista": "Nordika", "escenario": "Muelle", "dia": "sábado", "hora_inicio": hora, "hora_fin": hora[:2] + ":45"}
        )
    lineas = ejecuta("ej3.py", tmp_path, datos)
    for escenario, n in _cuenta_escenarios(datos).items():
        assert linea_con_numero(lineas, escenario, n), f"Con otros datos falta «{escenario}» con {n}"
    assert "muelle" in _linea_maximo(lineas), (
        "Con otros datos el escenario con más actuaciones es Muelle: ¿está escrito de forma literal?"
    )


# ------------------------------------------------------------- ejercicio 4

ARTISTA = "Mar de Fondo"


def test_ej4_datos_reales(tmp_path):
    lineas = ejecuta("ej4.py", tmp_path)
    suyas = [a for a in DATOS["actuaciones"] if a["artista"] == ARTISTA]
    for a in suyas:
        assert hay_linea(lineas, a["dia"], a["escenario"], a["hora_inicio"]), (
            f"Falta la actuación de {ARTISTA} del {a['dia']} ({a['escenario']}, {a['hora_inicio']}). "
            f"Comprobar que ARTISTA = \"{ARTISTA}\"."
        )
    assert not hay_linea(lineas, "no actúa"), f"{ARTISTA} sí actúa: no debería salir «no actúa»"


def test_ej4_otros_datos(tmp_path):
    datos = copy.deepcopy(DATOS)
    datos["actuaciones"] = [a for a in datos["actuaciones"] if a["artista"] != ARTISTA]
    lineas = ejecuta("ej4.py", tmp_path, datos)
    assert hay_linea(lineas, ARTISTA, "no actúa este año"), (
        f"Si {ARTISTA} no tiene actuaciones, debe aparecer «{ARTISTA} no actúa este año»"
    )


# ------------------------------------------------------------- ejercicio 5

def test_ej5_datos_reales(tmp_path):
    lineas = ejecuta("ej5.py", tmp_path)
    texto = " ".join(lineas)
    assert "sin solape" in texto or "no hay solape" in texto, (
        "Con los datos reales no hay solapes en Bahía: debe aparecer «sin solapes» o «no hay solapes»"
    )
    assert not any("solape entre" in l for l in lineas), "Se detecta un solape que no existe"


def test_ej5_otros_datos(tmp_path):
    datos = copy.deepcopy(DATOS)
    datos["actuaciones"] += [
        # solapa con Kortatu Berri (19:30-20:30) y con Vertigo Norte (21:00-22:00)
        {"artista": "Proba Taldea", "escenario": "Bahía", "dia": "viernes", "hora_inicio": "20:15", "hora_fin": "21:15"},
        # mismo día y hora pero en otro escenario: NO cuenta
        {"artista": "Otro Escenario", "escenario": "Muelle", "dia": "sábado", "hora_inicio": "20:10", "hora_fin": "20:40"},
    ]
    lineas = ejecuta("ej5.py", tmp_path, datos)
    for otra in ("Kortatu Berri", "Vertigo Norte"):
        assert hay_linea(lineas, "solape entre", "proba taldea", otra), (
            f"Falta «Solape entre Proba Taldea y {otra}» (o en orden inverso)"
        )
    assert not hay_linea(lineas, "otro escenario"), "Solo cuenta Bahía: se ha incluido otro escenario"
    assert not hay_linea(lineas, "solape entre", "kortatu berri", "vertigo norte"), (
        "Kortatu Berri y Vertigo Norte no se solapan"
    )
