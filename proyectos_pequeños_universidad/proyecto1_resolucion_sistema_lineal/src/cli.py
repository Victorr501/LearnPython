from typing import Any

def _pedir_entero_positivo(mensaje: str) -> int:
    """Solicita un número entero mayor que 0, repitiendo si hay error."""
    while True:
        entrada = input(mensaje).strip()
        try :
            valor = int(entrada)
            if valor <= 0:
                print("Por favor, introduce un número mayor que 0.")
                continue
            return valor
        except ValueError:
            print("Entrada no válida. Debes introducir un número entero.")    
            
def _pedir_objetivo() -> str:
    """Solicita si el problema es de maximización o minimización"""
    while True:
        op = input("¿Objetivo del problema? (max / min): ").strip().lower()
        if op in ("max", "min"):
            return op
        print("Escribe 'max' para maximizar o 'min' para minimizar.")
        
def _pedir_vector(mensaje: str, longitud: int) -> list[float]:
    """Solicita una lista de números flotantes de longitud exacta."""
    while True:
        entrada = input(mensaje).strip().replace(",", " ").split()
        if len(entrada) != longitud:
            print(f"Se esperaban {longitud} números, recibidos {len(entrada)}.")
            continue
        try:
            return [float(x) for x in entrada]
        except ValueError:
            print("Todos los valores deben ser números validos.")
            
def _pedir_restriccion(num: int, num_vars: int) -> tuple[list[float], str, float]:
    """
    Solicita una restricción completa: coeficientes, operador (<=, >=, =) y término b
    Ejemplo de entrada del usuario: 2 3 <= 10
    """
    
    operadores_validos = ("<=", ">=", "=")
    total_tokens = num_vars + 2
    
    while True:
        print(f"\nRestricción {num} (ej. para {num_vars} vars: {' '.join(['1']*num_vars)} <= 10):")
        tokens = input(" > ").strip().split()
        
        if len(tokens) != total_tokens:
            print(f"Formato incorrecto. Se esperaban {num_vars} coeficientes, un operador (<=, >=, =) y el valor b.")
            continue
        
        operador = tokens[-2]
        if operador not in operadores_validos:
            print(f"Operador '{operador}' no válido. Usa <= , >= 0 =.")
            continue
        
        try:
            coefs =[float(x) for x in tokens[:-2]]
            b_val = float(tokens[-1])
            return coefs, operador, b_val
        except ValueError:
            print("Los coefiecientes y el término independiende deben ser números.")
    
         
def pedir_sistema_pl() -> dict[str, Any]:
    """Recoge todos los datos de un Problema de Programación Lineal (asumiendo x_i >= 0)."""
    print("\n=== CONFIGURACIÓN DEL PROBLEMA DE PROGRAMACIÓN LINEAL ===")
    objetivo = _pedir_objetivo()
    num_vars = _pedir_entero_positivo("Número de variables de decisión (n): ")
    num_rest = _pedir_entero_positivo("Número de restricciones (m, sin contar x >= 0): ")
    
    c = _pedir_vector(f"\nIntrodce los {num_vars} coeficientes de la función objetivo Z: ", num_vars)
    
    matriz_A: list[list[float]] = []
    operadores: list[str] = []
    vector_b: list[float] = []
    
    for i in range(1, num_rest + 1):
        coefs, op, b_val = _pedir_restriccion(i, num_vars)
        matriz_A.append(coefs)
        operadores.append(op)
        vector_b.append(b_val) 
    
    return {
        "objetivo": objetivo,
        "c": c,
        "A": matriz_A,
        "operadores": operadores,
        "b": vector_b,
    }