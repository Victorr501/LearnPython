# Solucionador y Graficador de Programación Lineal (Algoritmo Simplex)

## Descripción del Proyecto
Este proyecto consiste en desarrollar una aplicación de línea de comandos (CLI) en **Python** diseñada para formular, transformar y resolver **Problemas de Programación Lineal (LPP)** mediante la implementación desde cero del **Algoritmo Simplex (en forma de tabla)**. Además, para problemas bidimensionales ($2$ variables de decisión), la herramienta genera una representación gráfica de la región factible y el punto óptimo.

El proyecto sirve como puente práctico entre la teoría matemática de optimización lineal y la ingeniería del software: manipulación matricial, transformación a forma estándar, operaciones elementales de pivoteo y visualización geométrica.

---

## Objetivos de Aprendizaje
* **Algoritmia y Álgebra Lineal:** Implementar paso a paso la conversión a forma estándar (variables de holgura y excedente) y las iteraciones de pivoteo del método Simplex usando `NumPy`.
* **Arquitectura de Software:** Separar responsabilidades en módulos independientes (`cli`, `solver`, `plotter`) aplicando tipado estático (*Type Hints*) y buenas prácticas.
* **Control y Validación de Datos:** Diseñar una interfaz de terminal robusta frente a errores de entrada del usuario.
* **Visualización Científica:** Representar semiplanos, intersecciones (politopo convexo de soluciones admisibles) y rectas de nivel de la función objetivo con `Matplotlib`.

---

## Requisitos Funcionales

### 1. Entrada de Datos (`src/cli.py`)
* Solicitar el sentido de la optimización: **Maximizar** (`max`) o **Minimizar** (`min`).
* Definir el número de variables de decisión ($n$) y de restricciones ($m$), asumiendo condiciones de no negatividad ($x_i \ge 0$).
* Recoger los coeficientes de la función objetivo $Z = c^t x$ y cada una de las restricciones ($A_i x \le b_i$, $\ge$ o $=$).
* Validar todas las entradas para evitar interrupciones por formato incorrecto.

### 2. Motor Matemático - Algoritmo Simplex (`src/solver.py`)
* **Conversión a Forma Estándar:**
  * Transformar problemas de maximización en minimización ($\max c^t x \equiv \min -c^t x$).
  * Asegurar que el vector de términos independientes sea no negativo ($b \ge 0$).
  * Añadir variables de holgura ($+s_i$) o excedente ($-e_i$) según el tipo de desigualdad.
* **Resolución en Forma de Tabla:**
  * Construir la tabla inicial del Simplex y mostrar por consola el estado de cada iteración (fila $z_j - c_j$, variable que entra, variable que sale y elemento pivote).
  * Identificar y reportar la naturaleza de la solución:
    * **Solución Óptima Única:** Mostrar el valor óptimo de $Z$ y los valores de las variables de decisión $(x_1, \dots, x_n)$.
    * **Solución Múltiple:** Detectar cuando existen soluciones óptimas infinitas en una arista de la región factible.
    * **Solución No Acotada:** Detectar cuando la función objetivo puede mejorar indefinidamente.
    * **Sin Solución (Región Factible Vacía):** Detectar incompatibilidad en las restricciones.

### 3. Visualización Gráfica 2D (`src/plotter.py`)
* Para problemas con **2 variables de decisión** ($x_1, x_2$):
  * Dibujar las rectas frontera de cada restricción en el primer cuadrante ($x_1 \ge 0, x_2 \ge 0$).
  * Sombrear la **región factible** (politopo convexo).
  * Marcar todos los vértices (soluciones básicas factibles) y destacar el **vértice óptimo** junto con la recta de la función objetivo pasando por él.
  * Permitir visualizar el gráfico en pantalla o exportarlo como imagen (`.png`).

---

## Estructura del Proyecto

```text
solucionador-lineal/
├── .venv/               # Entorno virtual aislado
├── src/                 # Paquete principal de la aplicación
│   ├── __init__.py      # Inicializador del paquete
│   ├── cli.py           # Interfaz de entrada/salida por terminal
│   ├── solver.py        # Transformación a forma estándar y Algoritmo Simplex
│   └── plotter.py       # Renderizado gráfico de la región factible (2D)
├── main.py              # Punto de entrada de la aplicación
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto
```

---

## Stack Tecnológico y Requisitos
* **Python 3.10+**
* **NumPy:** Operaciones vectoriales, matriciales y manipulación de las tablas del Simplex.
* **Matplotlib:** Generación de gráficos 2D.

### Instalación y Ejecución
```bash
# 1. Crear y activar el entorno virtual
python -m venv .venv
source .venv/bin/activate        # En Windows: .\.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python main.py
```

---

## Hoja de Ruta (Fases de Desarrollo)
- [x] **Fase 0:** Configuración de estructura del proyecto, entorno virtual y documentación.
- [x] **Fase 1:** Implementación de la interfaz CLI (`src/cli.py`) para captura y validación del problema.
- [x] **Fase 2:** Conversión a forma estándar y núcleo del Algoritmo Simplex en tabla (`src/solver.py`).
- [x] **Fase 3:** Soporte para restricciones $\ge$ e $=$ mediante el Método de las Dos Fases o Penalización (Gran M).
- [x] **Fase 4:** Generación de gráficos 2D de la región factible y solución óptima (`src/plotter.py`).