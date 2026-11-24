# 🧮 Solucionador y Graficador de Sistemas de Ecuaciones Lineales (CLI)

## 📋 Descripción del Proyecto
Este proyecto consiste en desarrollar una aplicación de línea de comandos (CLI) en **Python** capaz de resolver cualquier sistema de ecuaciones lineales $A \cdot \mathbf{x} = \mathbf{b}$ de dimensión $n \times n$ (o rectangular $m \times n$, según el alcance que decidas darle). Además de calcular la solución matemática y clasificar el sistema, la herramienta generará una representación gráfica del mismo cuando las dimensiones lo permitan (2D y 3D).

El objetivo principal es afianzar el manejo de estructuras de datos en Python, el control de excepciones, la modularización del código y el uso de librerías estándar del ecosistema científico.

---

## 🎯 Objetivos de Aprendizaje
* **Manipulación de matrices y vectores:** Uso de listas anidadas y transición a arrays de `NumPy`.
* **Lógica matemática y control de flujo:** Clasificación de sistemas según el Teorema de Rouché–Frobenius (Compatible Determinado, Compatible Indeterminado e Incompatible).
* **Interacción por terminal:** Validación de entradas de usuario y presentación limpia de resultados.
* **Visualización de datos:** Representación geométrica de rectas (2 variables) y planos (3 variables) mediante `Matplotlib`.

---

## ⚙️ Requisitos Funcionales

### 1. Entrada de Datos (Interfaz de Terminal)
* El programa debe solicitar al usuario el número de ecuaciones ($m$) y de incógnitas ($n$).
* Debe permitir introducir los coeficientes de la matriz $A$ y los términos independientes del vector $\mathbf{b}$ de forma intuitiva (fila por fila o ecuación por ecuación).
* **Validación:** El programa no debe colapsar si el usuario introduce texto en lugar de números; debe capturar el error y volver a pedir el dato.

### 2. Análisis y Resolución Matemática
El motor de cálculo debe evaluar el sistema y actuar según su naturaleza:
* **Sistema Compatible Determinado (SCD):** Calcular y mostrar la solución única $(x_1, x_2, \dots, x_n)$.
* **Sistema Compatible Indeterminado (SCI):** Indicar que el sistema tiene infinitas soluciones (opcional: mostrar la solución paramétrica o el rango de las matrices).
* **Sistema Incompatible (SI):** Indicar claramente que el sistema no tiene solución (rectas/planos paralelos o inconsistentes).

### 3. Generación de Gráficos
* **Para sistemas de 2 incógnitas ($2 \times 2$):**
  * Dibujar cada ecuación como una recta en el plano cartesiano ($X, Y$).
  * Si es **SCD**, marcar con un punto destacado y una etiqueta las coordenadas exactas donde se cortan las rectas.
  * Incluir leyenda con las ecuaciones, ejes coordenados centrados, cuadrícula y título descriptivo.
* **Para sistemas de 3 incógnitas ($3 \times 3$) *(Nivel Avanzado)*:**
  * Renderizar los planos en un espacio tridimensional (`3D projection`) y señalar el punto de intersección si existe.
* **Exportación:** Dar la opción al usuario de visualizar el gráfico en pantalla o guardarlo automáticamente como imagen (ej. `resultado_sistema.png`).

---

## 🛠️ Stack Tecnológico Recomendado
* **Lenguaje:** Python 3.10+
* **Cálculo Numérico:** `numpy` (para álgebra lineal, rangos y resolución de matrices).
* **Gráficos:** `matplotlib` (para renderizado 2D/3D).
* *(Opcional)* **Interfaz CLI mejorada:** `rich` o `colorama` para darle color y formato de tablas a la salida por consola.

---

## 🚀 Fases de Desarrollo Sugeridas

1. **Fase 1 (Core Matemático):** Crear las funciones que reciben una matriz $A$ y un vector $\mathbf{b}$, comprueban los rangos ($\text{rg}(A)$ vs $\text{rg}(A|b)$) y devuelven la solución.
2. **Fase 2 (CLI y Validación):** Construir el menú en terminal para que el usuario introduzca los datos cómodamente y gestionar errores de entrada.
3. **Fase 3 (Gráficos 2D):** Integrar `Matplotlib` para dibujar los sistemas de 2 incógnitas y guardar la imagen.
4. **Fase 4 (Extras / Reto):** Añadir soporte para gráficos 3D, lectura de sistemas desde un archivo `.txt`/`.csv`, o implementar el método de Gauss-Jordan "a mano" sin usar `numpy.linalg.solve` para practicar algoritmia pura.