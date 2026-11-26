# 🐍 LearnPython - Laboratorio & Launcher Hub

Repositorio personal de prácticas, algoritmos y proyectos de ingeniería desarrollados en Python. Incluye un **lanzador interactivo por terminal (`main.py`)** que unifica todo el espacio de trabajo y permite ejecutar cualquier script o aplicación de forma aislada desde un único menú.

---

## 📂 Estructura del Repositorio

```text
LearnPython/
├── .venv/                              # Entorno virtual global del repositorio
├── main.py                             # Lanzador principal (CLI Hub interactivo)
├── requirements.txt                    # Dependencias compartidas (NumPy, Matplotlib, etc.)
├── proyectos_pequeños_universidad/     # Aplicaciones completas y prácticas de Ingeniería
│   └── proyecto1_resolucion_sistema_lineal/
│       ├── src/                        # Lógica modularizada (cli, solver, plotter)
│       ├── main.py                     # Punto de entrada del proyecto
│       └── README.md                   # Documentación específica del proyecto
├── leet_code/                          # Resolución de problemas de algoritmia y estructuras de datos
└── aprender/                           # Apuntes ejecutables, sintaxis y pruebas de concepto
```

---

## 🚀 Cómo funciona el Lanzador (`main.py`)

El archivo `main.py` en la raíz actúa como un **centro de control en bucle infinito** hasta que decidas salir:

1. **Autodescubrimiento dinámico:** Escanea automáticamente las tres carpetas principales sin necesidad de registrar manualmente cada archivo nuevo:
   * En **`proyectos_pequeños_universidad/`** busca subcarpetas que contengan su propio `main.py`.
   * En **`leet_code/`** y **`aprender/`** lista directamente todos los scripts `.py`.
2. **Aislamiento de ejecución (`cwd`):** Cada programa se ejecuta en un subproceso independiente dentro de su propio directorio de trabajo. Esto evita conflictos con rutas relativas o importaciones internas (como `from src.solver import ...`).
3. **Entorno unificado:** Al ejecutarse mediante `sys.executable`, hereda automáticamente el entorno virtual `.venv` activo en la raíz.

---

## 🛠️ Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Victorr501/LearnPython.git
   cd LearnPython
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv .venv
   ```
   * **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
   * **Linux / macOS:** `source .venv/bin/activate`

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Arrancar el lanzador principal:**
   ```bash
   python main.py
   ```

---

## ➕ Cómo añadir contenido nuevo

* **Nuevo proyecto completo:** Crea una carpeta dentro de `proyectos_pequeños_universidad/` con su propio `main.py` (y su carpeta `src/` con `__init__.py` si usa varios módulos). Aparecerá automáticamente en la opción **1**.
* **Nuevo ejercicio o apunte:** Guarda cualquier archivo `.py` dentro de `leet_code/` (opción **2**) o `aprender/` (opción **3**).