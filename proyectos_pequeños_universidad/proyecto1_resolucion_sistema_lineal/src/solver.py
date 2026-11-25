from typing import Any
import numpy as np

def _validar_y_preparar_estandar(problema: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """
    Valida si el problema es resoluble directamente mediante Simplex estándar
    (sin variables artificales) y lo transforma a forma estándar:
        min z' = c_std^T x
        s.a: A_std x = b_std, x >= 0, b_std >= 0 
    """
    
    objetivo = problema["objetivo"]
    c = np.array(problema["c"], dtype=float)
    A = np.array(problema["A"], dtype=float)
    operadores = list(problema["operadores"])
    b = np.array(problema["b"], dtype=float)
    
    num_rest, num_vars = A.shape
    
    # Convertir maximización a minimización: max c^T x <=> min -c^T
    es_max = objetivo == "max"
    c_std = -c if es_max else c.copy()
    
    # Normalizar restricciones y comprobar viabilidad directa
    filas_A = []
    nuevo_b = []
    
    for i in range(num_rest):
        fila = A[i].copy()
        op = operadores[i]
        val_b = b[i]
        
        # Si b < 0, multiplicamos toda la fila por -1 e invertimos el operador
        if val_b < 0:
            fila = -fila
            val_b = -val_b
            if op == "<=":
                op = ">="
            elif op == ">=":
                op = "<="
                
        # Comprobación temprana 1: Fila nula (0*x <= b, 0*x = b, 0*x >= b)
        if np.allclose(fila, 0):
            if (op == "=" and not np.isclose(val_b, 0)) or (op == ">=" and val_b > 0):
                return False, f"Restricción {i + 1} imposible (0 {op} {val_b}). Región factible vacía", {}
            continue # Restrcción redundante (0 <= b con b >= 0), se ignora
    
        # Comprobación temprana 2:  Todos los coeficientes >= 0 pero <= b con b < 0
        # (tras normalizar b >= 0, esto equivale a todos los coefs <= 0 y >= val_b > 0)
        if op == ">=" and val_b > 0 and np.all(fila <= 0):
            return (
                False,
                f"Restricción {i + 1} infactible con x >= 0 (todos los coeficientes <= 0 pero >= {val_b})",
                {}
            )
            
        # Comprobación tempreana 3: El simple directo requiere base indentidad inicial (<= con b >= 0)
        if op == "=" and not np.isclose(val_b, 0):
            return (
                False, 
                f"La restricción {i + 1} es una igualdad ('=') con b != 0. Requiere Método de Dos Fases o Gran M.",
                {}
            )
        if op == ">=" and not np.isclose(val_b, 0):
            return (
                False,
                f"La restricción {i + 1} es de tipo '>=' con b > 0. Requiere varialbes artificales (Dos Fases / Gran M)",
                {}
            )
        
        # Si es '>=' con b == 0, multiplicamos por -1 para dejarla como '<='
        if op == ">=" and np.isclose(val_b, 0):
            fila = -fila
            
        filas_A.append(fila)
        nuevo_b.append(val_b)
        
    if not filas_A:
        return False, "No quedan restricciones efectivas. El problema no está acotado.", {}
    
    A_norm = np.array(filas_A, dtype=float)
    b_std = np.array(nuevo_b, dtype=float)
    m_efectivas = A_norm.shape[0]
    
    # Añadir  valores de holgura (matriz identidad I_m)
    idendidad = np.eye(m_efectivas, dtype=float)
    A_std = np.hstack([A_norm, idendidad])
    c_std_completo = np.concatenate([c_std, np.zeros(m_efectivas, dtype=float)])
    
    datos_estandar = {
        "es_max": es_max,
        "num_vars_orig": num_vars,
        "c": c_std_completo,
        "A": A_std,
        "b": b_std,
    }
    
    return True, "OK", datos_estandar

def resolver_simplex(problema : dict[str, Any], mostrar_tablas: bool = True) -> dict[str, any]:
    """
    Resuelve un problema de Programación Lineal usando el Algoritmo Simplex en forma de tabla
    (siguiendo la convención del Tema 5: fila Z con z_j - c_j, entra el más positivo)
    """
    
    valido, mensaje, std = _validar_y_preparar_estandar(problema)
    if not valido:
        return{
            "exito": False,
            "estado": "NO_RESOLUBLE_DIRECTO",
            "mensaje": mensaje,
        }

    c = std["c"]
    A = std["A"]
    b = std["b"]
    num_vars_orig = std["num_vars_orig"]
    es_max = std["es_max"]
    
    m, n = A.shape
    # Las varialbes básicas iniciales son las de holgura (índices num_vars_orig ... n - 1)
    base = list(range(num_vars_orig, n))
    nombres_vars = [f"x{i + 1}" for i in range(n)]
    
    # Construcción de la tabla inicial:
    tabla = np.zeros((m + 1, n + 1), dtype=float)
    tabla[0, :n] = -c
    tabla[0, -1] = 0.0
    tabla[1:, :n] = A
    tabla[1:, -1] = b
    
    iteracion = 0
    max_iteracciones = 100
    
    while iteracion < max_iteracciones:
        if mostrar_tablas:
            _imprimir_tabla(tabla, base, nombres_vars, iteracion)
        
        fila_z = tabla[0, :n]
        max_zc = np.max(fila_z)
        
        if max_zc <= 1e-9:
            # Comprobar si hay soluciones múltiples (alguna variable no básica con z_j - c_j == 0)
            no_basicas = [j for j in range(n) if j not in base]
            solucion_multiple = any(np.isclose(fila_z[j], 0.0, atol=1e-8) for j in no_basicas)
            
            solucion_completa = np.zeros(n, dtype=float)
            for fila_idx, var_idx in enumerate(base):
                solucion_completa[var_idx] = tabla[fila_idx + 1, -1]
                
            z_min = tabla[0, -1]
            z_final = -z_min if es_max else z_min
            
            return {
                "exito" : True,
                "estado": "OPTIMO_MULTIPLE" if solucion_multiple else "OPTIMO_UNICO",
                "mensaje": "Solucción óptima múltiple encontrada." if solucion_multiple else "Solucioón óptima única encontrada",
                "z_optimo": float(z_final),
                "variables": solucion_completa[:num_vars_orig].tolist(),
                "variables_todas": solucion_completa.tolist(),
                "iteracciones" : iteracion 
            }
        
    
        # Columna pivote (variable que entra): mayor z_j - c_j
        col_pivote = int(np.argmax(fila_z))
        columna = tabla[1:, col_pivote]
        
        # Comprobación de problema no acotado: si todos y_ik <= 0
        if np.all(columna <= 1e-9):
            return {
                "exito": False,
                "estado" : "NO_ACOTADO",
                "mensaje" : f"Problema no acotado: la variable {nombres_vars[col_pivote]} puede crecer indefinidamente.",
            }
        
        # Fila pivote (variable que sale): mínimo cociente b_i / y_ik con y_ik > 0
        cocientes = np.full(m, np.inf)
        for i in range(m):
            if columna[i] > 1e-9:
                cocientes[i] = tabla[i + 1, -1] / columna[i]
            
        fila_pivote_idx = int(np.argmin(cocientes))
        fila_tabla_pivote = fila_pivote_idx + 1
        pivote = tabla[fila_tabla_pivote, col_pivote]
        
        # Pivotar (Gauss-Jordan): normalizar fila pivote y hacer ceros en la columna
        tabla[fila_tabla_pivote] /= pivote
        for r in range(m +1):
            if r != fila_tabla_pivote:
                factor = tabla[r, col_pivote]
                tabla[r] -= factor * tabla[fila_tabla_pivote]
            
        base[fila_pivote_idx] = col_pivote
        iteracion += 1
        
    return {
        "exito": False,
        "estado" : "MAX_ITERACIONES",
        "mensaje" : "Se alcanzó el limite de iteraciones (posible ciclaje por degenarción).",
    }
    
def _imprimir_tabla(tabla: np.ndarray, base: list[int], nombre: list[str], iteracion: int) -> None:
    """Imprime la tabla Simplex formateada en colosa igual que en los apuntes."""
    print(f"\n--- Tabla Simplex (Iteracción {iteracion}) ---")
    encabezado = f"{'V.B.':<6} | " + " ".join(f"{nom:>8}" for nom in nombre) + f" | {'Sol':>8}"
    print(encabezado)
    print("-" * len(encabezado))
    
    fila_z_str = f"{'Z':<6} | " + " ".join(f"{val:8.2f}" for val in tabla[0, :-1]) + f" | {tabla[0, -1]:8.2f}"
    print(fila_z_str)
    print("-" * len(encabezado))
    
    for i, var_idx in enumerate(base):
        vals = " ".join(f"{val:8.2f}" for val in tabla [i + 1, :-1])
        print(f"{nombre[var_idx]:<6} | {vals} | {tabla[i + 1, -1]:8.2f}")