#!/usr/bin/env python3
"""
actualizar.py — Script de mantenimiento para josepcosta.es

Uso: python3 actualizar.py

Qué hace:
  1. Escanea cada carpeta de proyecto dentro de img/
  2. Renumera los .jpg secuencialmente (01.jpg, 02.jpg, 03.jpg...)
  3. Actualiza index.html con los nuevos conteos

Así solo tienes que:
  - Meter fotos nuevas en la carpeta (con cualquier nombre)
  - Borrar fotos que no quieras
  - Ejecutar: python3 actualizar.py
"""

import os
import re
import glob
import shutil

# Carpetas de proyecto (key debe coincidir con genPhotos en el HTML)
SERIES_FOLDERS = [
    'gigantes',
    'paisajesenfuga',
    'matances',
    'nyc',
    'light',
    'trigo',
    'mirades',
    'carrusel',
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(SCRIPT_DIR, 'img')
HTML_FILE = os.path.join(SCRIPT_DIR, 'index.html')


def renumber_folder(folder_path):
    """Renumera todos los .jpg de una carpeta a 01.jpg, 02.jpg, etc."""
    files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')],
        key=lambda f: f.lower()
    )

    if not files:
        print(f"  ⚠ Carpeta vacía")
        return 0

    # Primero renombrar a temporales para evitar colisiones
    temp_names = []
    for i, f in enumerate(files):
        temp = f"_tmp_{i:04d}.jpg"
        os.rename(
            os.path.join(folder_path, f),
            os.path.join(folder_path, temp)
        )
        temp_names.append(temp)

    # Luego renombrar a nombres finales
    for i, temp in enumerate(temp_names):
        final = f"{i+1:02d}.jpg"
        os.rename(
            os.path.join(folder_path, temp),
            os.path.join(folder_path, final)
        )

    return len(temp_names)


def update_html(counts):
    """Actualiza genPhotos('carpeta', N) en index.html con los nuevos conteos."""
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    for folder, count in counts.items():
        # Busca genPhotos('carpeta', NUMERO) y actualiza el número
        pattern = rf"genPhotos\('{folder}',\s*\d+\)"
        replacement = f"genPhotos('{folder}', {count})"
        html, n = re.subn(pattern, replacement, html)
        if n == 0:
            print(f"  ⚠ No se encontró genPhotos('{folder}', ...) en el HTML")

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    print("═" * 50)
    print("  Actualizando josepcosta.es")
    print("═" * 50)
    print()

    counts = {}

    for folder in SERIES_FOLDERS:
        folder_path = os.path.join(IMG_DIR, folder)
        if not os.path.isdir(folder_path):
            print(f"✗ {folder}/ — carpeta no encontrada")
            continue

        count = renumber_folder(folder_path)
        counts[folder] = count
        print(f"✓ {folder}/ — {count} fotos")

    print()
    print("Actualizando index.html...")
    update_html(counts)

    print()
    print("═" * 50)
    total = sum(counts.values())
    print(f"  Listo. {total} fotos en {len(counts)} series.")
    print("═" * 50)


if __name__ == '__main__':
    main()
