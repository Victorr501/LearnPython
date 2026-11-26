import os
import subprocess
import sys
from pathlib import Path

# Raíz del repositorio (donde está este main.py)
REPO_ROOT = Path(__file__).resolve().parent

CATEGORIAS = {
    "1": ("Proyectos Universidad", REPO_ROOT / "proyectos_pequeños_universidad"),
    "2": ("LeetCode & Algoritmia", REPO_ROOT / "leet_code"),
    "3": ("Aprender Python", REPO_ROOT / "aprender"),
}


def limpiar_pantalla() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def buscar_ejecutables(carpeta: Path, es_proyecto: bool) -> list[tuple[str, Path]]:
    """
    Devuelve una lista de tuplas (nombre_visible, ruta_al_main_o_script).
    - Si es_proyecto=True ('proyectos' y 'leet_code'): busca subcarpetas que contengan un 'main.py'.
    - Si es_proyecto=False ('aprender'): busca archivos '.py' directamente.
    """
    if not carpeta.exists():
        return []

    items: list[tuple[str, Path]] = []

    if es_proyecto:
        for subcarpeta in sorted(carpeta.iterdir()):
            if subcarpeta.is_dir():
                punto_entrada = subcarpeta / "main.py"
                if punto_entrada.exists():
                    items.append((subcarpeta.name, punto_entrada))
    else:
        for archivo in sorted(carpeta.glob("*.py")):
            if archivo.name != "__init__.py":
                items.append((archivo.stem, archivo))

    return items


def ejecutar_script(ruta_script: Path) -> None:
    """Lanza el script en un subproceso aislado usando el Python actual (.venv)."""
    print(f"\n Ejecutando: {ruta_script.relative_to(REPO_ROOT)}")
    print("=" * 55)
    try:
        # cwd=ruta_script.parent asegura que sus imports internos (ej. 'from src...') funcionen
        subprocess.run([sys.executable, str(ruta_script)], cwd=ruta_script.parent)
    except KeyboardInterrupt:
        print("\n  Ejecución interrumpida por el usuario.")
    print("=" * 55)
    input("\nPresiona ENTER para volver al menú...")


def submenu_categoria(nombre_cat: str, carpeta: Path, es_proyecto: bool) -> None:
    """Muestra los scripts/proyectos dentro de una categoría hasta que el usuario vuelva."""
    while True:
        limpiar_pantalla()
        print(f"=== {nombre_cat.upper()} ===")
        items = buscar_ejecutables(carpeta, es_proyecto)

        if not items:
            print(f"\nNo se encontraron {'proyectos con main.py' if es_proyecto else 'scripts .py'} en '{carpeta.name}/'.")
            input("\nPresiona ENTER para volver...")
            return

        for idx, (nombre, _) in enumerate(items, start=1):
            print(f"  {idx}. {nombre}")
        print("  0. Volver al menú principal")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "0":
            return

        if opcion.isdigit() and 1 <= int(opcion) <= len(items):
            _, ruta_elegida = items[int(opcion) - 1]
            ejecutar_script(ruta_elegida)
        else:
            print("Opción no válida.")
            input("Presiona ENTER para continuar...")


def main() -> None:
    while True:
        limpiar_pantalla()
        print("==========================================")
        print("      🐍 LEARN PYTHON - LAUNCHER HUB      ")
        print("==========================================")
        for clave, (nombre, _) in CATEGORIAS.items():
            print(f"  {clave}. {nombre}")
        print("  0. Salir")
        print("==========================================")

        opcion = input("\n¿Qué quieres abrir hoy?: ").strip()

        if opcion == "0":
            print("\n¡Hasta la próxima!")
            break
        elif opcion in CATEGORIAS:
            nombre_cat, ruta_cat = CATEGORIAS[opcion]
            submenu_categoria(nombre_cat, ruta_cat, es_proyecto=(opcion in ("1", "2")))
        else:
            print("Opción no válida.")
            input("Presiona ENTER para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSaliendo del lanzador...")
        sys.exit(0)