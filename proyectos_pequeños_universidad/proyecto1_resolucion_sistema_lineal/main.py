import sys
from src.cli import pedir_sistema_pl as pspl
from src.solver import resolver_simplex as rs

def main():
    print("=== Solucionador de Sistemas Lineales ===")
    print("Entorno configurado correctamente. ¡Listo para programar!")
    
    problema = pspl()
    resultado = rs(problema, mostrar_tablas= True)
    
    print("\n" + "=" * 45)
    
    if resultado["exito"]:
        print(f"{resultado['mensaje']}")
        print(f"Valor óptimo Z = {resultado['z_optimo']:.4f}")
        for i, val in enumerate(resultado["variables"], start=1):
            print(f"    x{i} = {val:.4f}")
    else:
        print(f"No se puede resolver: {resultado['mensaje']}")
    print("\n" + "=" * 45)

    
# El arranque de la aplicacio
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEjecución cancleada por el usuario")
        sys.exit(0)
    