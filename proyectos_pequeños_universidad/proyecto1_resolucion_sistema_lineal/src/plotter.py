from typing import Any
import numpy as np
import matplotlib.pyplot as plt

def graficar_pl(problema: dict[str, Any], resultado: dict[str, Any], guardar_ruta: str = "solucion_pl.png") -> None:
    """
    Despachador grafico: genera visualización 2D si n=2 o 3D si n=3
    """
    
    num_vars = len(problema["c"])
    if num_vars == 2:
        _graficar_2d(problema, resultado, guardar_ruta)
    elif num_vars == 3:
        _graficar_3d(problema, resultado, guardar_ruta)
    else:
        print(f"\nVísualización no disponible para n = {num_vars} (solo soporta 2D y 3D)")
        
def _calcular_limite_ejes(A: np.ndarray, b: np.ndarray, resultado: dict[str, Any]) -> float:
    """
    Clacula un límite superior dinámico para los ejes positivos.
    """
    puntos_corte = [1.0]
    if resultado.get("exito"):
        puntos_corte.extend(resultado["variables"])
        
    num_vars = A.shape[1]
    for i in range(len(b)):
        for j in range(num_vars):
            if not np.isclose(A[i,j], 0) and b[i] > 0:
                corte = b[i] / A[i, j]
                if corte > 0:
                    puntos_corte.append(corte)

    return max(puntos_corte) * 1.25

def _graficar_2d(problema: dict[str, Any], resultado: dict[str, Any], guardar_ruta: str) -> None:
    """Genera el gráfico 2D con región factible sombreada, rectas y punto óptico"""
    A = np.array(problema["A"], dtype=float)
    b = np.array(problema["b"], dtype=float)
    operadores = problema["operadores"]
    c = np.array(problema["c"], dtype=float)
    
    limite_max = _calcular_limite_ejes(A, b, resultado)
    
    # Malla 2D para sombrear la región factible
    x1_grid = np.linspace(0, limite_max, 500)
    x2_grid = np.linspace(0, limite_max, 500)
    X1, X2 = np.meshgrid(x1_grid, x2_grid)
    
    region_factible = (X1 >= 0) & (X2 >= 0)
    for i in range(len(b)):
        expr = A[i, 0] * X1 + A[i, 1] * X2
        op = operadores[i]
        if op == "<=":
            region_factible &= (expr <= b[i] + 1e-7)
        elif op == ">=":
            region_factible &= (expr >= b[i] - 1e-7)
        elif op == "=":
            region_factible &= np.isclose(expr, b[i], atol=1e-2)
    
    fig, ax = plt.subplots(figsize=(8,6))
    
    ax.imshow(
        region_factible.astype(int),
        extent = (0, limite_max, 0, limite_max),
        origin = "lower",
        cmap = "Greens",
        alpha = 0.25,
        aspect = "auto",
    )
    
    x_vals = np.linspace(0, limite_max, 400)
    colores = plt.cm.tab10.colors
    
    for i in range(len(b)):
        a1, a2 = A[i]
        bi = b[i]
        op = operadores[i]
        color = colores[i % len(colores)]
        etiqueta = f"R{i + 1}: {a1:g}x₁ + {a2:g}x₂ {op} {bi:g}"
        
        if not np.isclose(a2, 0):
            y_vals = (bi - a1 * x_vals) / a2
            ax.plot(x_vals, y_vals, label = etiqueta, color=color, linewidth = 2)
        elif not np.isclose(a1, 0):
            ax.axvline(x = bi / a1, label=etiqueta, color=color, linewidth = 2)
            
    if resultado.get("exito"):
        opt_x1, opt_x2 = resultado["variables"]
        z_opt = resultado["z_optimo"]
        
        if not np.isclose(c[1], 0):
            z_vals = (z_opt - c[0] * x_vals) / c[1]
            ax.plot(x_vals, z_vals, "--", color="crimson", linewidth=1.5, label=f"Z óptimo = {z_opt:.2f}")
            
        ax.scatter([opt_x1], [opt_x2], color="red", zorder=5, s=90, edgecolors="black")
        
        ax.annotate(
            f"Óptimo ({opt_x1:.2f}, {opt_x2:.2f})\nZ = {z_opt:.2f}",
            xy=(opt_x1, opt_x2),
            xytext=(opt_x1 + limite_max * 0.04, opt_x2 + limite_max * 0.04),
            fontsize=9,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", edgecolor="red", alpha=0.9),
            arrowprops=dict(arrowstyle="->", color="red"),
        )

    ax.set_xlim(0, limite_max)
    ax.set_ylim(0, limite_max)
    ax.set_xlabel("x₁", fontsize=11, fontweight="bold")
    ax.set_ylabel("x₂", fontsize=11, fontweight="bold")
    ax.set_title(f"Programación Lineal 2D ({problema['objetivo'].upper()} Z)", fontsize=13, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.7)
    ax.legend(loc="upper right", fontsize=9)

    plt.tight_layout()
    plt.savefig(guardar_ruta, dpi=150)
    print(f"\nGráfico 2D guardado en '{guardar_ruta}'. Cierra la ventana para finalizar.")
    plt.show()
        
        
def _graficar_3d(problema: dict[str, Any], resultado: dict[str, Any], guardar_ruta: str) -> None:
    """Genera el gráfico 3D con los planos de restricciones en el primer octante y el punto óptimo."""
    A = np.array(problema["A"], dtype=float)
    b = np.array(problema["b"], dtype=float)
    operadores = problema["operadores"]

    limite_max = _calcular_limite_ejes(A, b, resultado)
    grid_1d = np.linspace(0, limite_max, 60)

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    colores = plt.cm.tab10.colors
    handles_leyenda = []

    for i in range(len(b)):
        a1, a2, a3 = A[i]
        bi = b[i]
        op = operadores[i]
        color = colores[i % len(colores)]
        etiqueta = f"R{i + 1}: {a1:g}x₁ + {a2:g}x₂ + {a3:g}x₃ {op} {bi:g}"

        # Despejamos la variable con coeficiente no nulo para parametrizar el plano
        if not np.isclose(a3, 0):
            X1, X2 = np.meshgrid(grid_1d, grid_1d)
            X3 = (bi - a1 * X1 - a2 * X2) / a3
            X3 = np.where((X3 >= 0) & (X3 <= limite_max), X3, np.nan)
        elif not np.isclose(a2, 0):
            X1, X3 = np.meshgrid(grid_1d, grid_1d)
            X2 = (bi - a1 * X1 - a3 * X3) / a2
            X2 = np.where((X2 >= 0) & (X2 <= limite_max), X2, np.nan)
        elif not np.isclose(a1, 0):
            X2, X3 = np.meshgrid(grid_1d, grid_1d)
            X1 = (bi - a2 * X2 - a3 * X3) / a1
            X1 = np.where((X1 >= 0) & (X1 <= limite_max), X1, np.nan)
        else:
            continue

        ax.plot_surface(X1, X2, X3, color=color, alpha=0.35, edgecolor="none")
        # Proxy artist para que Matplotlib pueda mostrar superficies en la leyenda
        handles_leyenda.append(plt.Line2D([0], [0], linestyle="none", marker="s", markersize=10, markerfacecolor=color, alpha=0.6, label=etiqueta))

    if resultado.get("exito"):
        opt_x1, opt_x2, opt_x3 = resultado["variables"]
        z_opt = resultado["z_optimo"]

        # Punto óptimo
        punto = ax.scatter(
            [opt_x1], [opt_x2], [opt_x3],
            color="red", s=110, edgecolors="black", zorder=10,
            label=f"Óptimo ({opt_x1:.2f}, {opt_x2:.2f}, {opt_x3:.2f}) | Z = {z_opt:.2f}",
        )
        handles_leyenda.append(punto)

        # Líneas guía de proyección hacia los planos coordenados para apreciar profundidad
        ax.plot([opt_x1, opt_x1], [opt_x2, opt_x2], [0, opt_x3], "--", color="red", alpha=0.6, linewidth=1.2)
        ax.plot([opt_x1, opt_x1], [0, opt_x2], [0, 0], ":", color="gray", alpha=0.6)
        ax.plot([0, opt_x1], [opt_x2, opt_x2], [0, 0], ":", color="gray", alpha=0.6)

        ax.text(
            opt_x1, opt_x2, opt_x3 + limite_max * 0.05,
            f"  Óptimo\n  ({opt_x1:.2f}, {opt_x2:.2f}, {opt_x3:.2f})\n  Z = {z_opt:.2f}",
            fontsize=9,
            fontweight="bold",
            color="darkred",
        )

    ax.set_xlim(0, limite_max)
    ax.set_ylim(0, limite_max)
    ax.set_zlim(0, limite_max)
    ax.set_xlabel("x₁", fontsize=11, fontweight="bold")
    ax.set_ylabel("x₂", fontsize=11, fontweight="bold")
    ax.set_zlabel("x₃", fontsize=11, fontweight="bold")
    ax.set_title(f"Programación Lineal 3D ({problema['objetivo'].upper()} Z)", fontsize=13, fontweight="bold")
    ax.legend(handles=handles_leyenda, loc="upper left", fontsize=8.5)

    plt.tight_layout()
    plt.savefig(guardar_ruta, dpi=150)
    print(f"\nGráfico 3D guardado en '{guardar_ruta}'. Puedes rotarlo con el ratón antes de cerrar.")
    plt.show()