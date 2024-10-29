# mi_paquete/main.py
import os
from runstep.simpath import simpath
import argparse

def mkdirsimln(target="simulations"):
    sp = simpath()
    # Crear el enlace simbólico con `os.symlink`
    os.symlink(sp, target)
    print(f"Enlace simbólico creado: {sp} -> {target}")

def main():
    parser = argparse.ArgumentParser(description="Crear un enlace simbólico al directorio de simulaciones.")

    # Argumento para el directorio de destino
    parser.add_argument('-t', '--target', type=str, default="simulations",
                        help="Directorio de destino para el enlace simbólico (por defecto: 'simulations')")

    # Parsear los argumentos
    args = parser.parse_args()

    # Llamar a mkdirsimln con el argumento proporcionado
    mkdirsimln(args.target)
