## Introducción a QQSM

Este proyecto es el Trabajo de Fin de Grado (TFG) de cuatro alumnos de la facultad de informática de la Universidad Complutense de Madrid (UCM). Se trata de una implementación moderna del conocido concurso **¿Quién quiere ser millonario?**, en la que **todas las preguntas son generadas y verificadas por inteligencia artificial**.

QQSM recolecta estadísticas de juego de cada usuario (aciertos, tiempos, puntuaciones) y ofrece varios modos de juego:

* **Clásico**: partida de **15 preguntas** con las reglas estándar del concurso.

* **Infinito**: preguntas continuas **hasta fallar**, sin límite de rondas.

* **Elección**: variante del modo Clásico con **15 preguntas**, donde antes de cada una el usuario elige **entre 2 temas** disponibles.

* **Modo IA vs IA (pasivo)**: espectador de enfrentamientos entre motores de IA sin intervención del usuario, tales como:

  * **Gemini** (clave **GIA\_API\_KEY**).
  * **DeepSeek**, **OpenAI** y **Llama** (opcionales para duelos IA vs IA).

## Tecnologías empleadas

* **Python 3.9+**: lenguaje de programación principal.
* **Reflex**: framework full‑stack para frontend y backend en un único servidor.
* **PostgreSQL**: base de datos relacional para almacenamiento de estadísticas.
* **SQLAlchemy**: ORM para interacción con la base de datos.
* **Passlib\[bcrypt]**: gestión de hashing y autenticación segura.

## Guía de Instalación

1. **Clonar el repositorio**

   Clona el repositorio y sitúate en la carpeta del proyecto:

   ```bash
   git clone https://github.com/MVGDCRB/QQSM.git
   cd QQSM
   ```

2. **Crear y activar un entorno virtual**

   Crea un entorno virtual y actívalo. Mantén el entorno activo durante la instalación **y** la ejecución de la aplicación:

   * **Windows (PowerShell)**:

     ```powershell
     py -m venv venv
     venv\Scripts\activate
     ```
   * **macOS / Linux**:

     ```bash
     python3 -m venv venv   # o python -m venv venv
     source venv/bin/activate
     ```

   > **Importante:** Asegúrate de que el entorno virtual permanezca activo en **todos** los pasos siguientes y de ejecutar siempre los comandos desde el directorio raíz `QQSM`.

3. **Instalar dependencias**

   Desde el directorio `QQSM` y con el entorno virtual activo, instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. **Crear el archivo de secretos**

   Define tus claves en `QQSM/secrets.py`. La clave **GIA\_API\_KEY** es obligatoria; las demás son opcionales para modos IA vs IA:

   ```python
   # QQSM/secrets.py
   class Secrets:
       GIA_API_KEY    = "tu_clave_de_Gemini_aquí"     # imprescindible
       DEEP_API_KEY   = "tu_clave_de_DeepSeek_aquí"   # opcional
       OPENAI_API_KEY = "tu_clave_de_OpenAI_aquí"     # opcional
       LLAMA_API_KEY  = "tu_clave_de_Llama_aquí"      # opcional
   ```

5. **Instalar PostgreSQL**

   Instala y configura PostgreSQL antes de definir la conexión:

   * **Windows**:

     1. Descarga e instala desde [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/).
     2. Durante la instalación, abre **Stack Builder** para instalar **pgAdmin** (herramienta utilizada para la gestión de la base de datos), extensiones y drivers.

   * **macOS**:

     ```bash
     brew install postgresql
     brew services start postgresql
     ```

   * **Linux (Debian/Ubuntu)**:

     ```bash
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     sudo systemctl enable postgresql
     sudo systemctl start postgresql
     ```

6. **Configurar la conexión a la base de datos**

   El archivo de configuración está en `QQSM/db/database.py`. Abre ese fichero y edita estos parámetros para cambiar la conexión:

   ```python
   # db/database.py
   DB_USER     = "postgres"
   DB_PASSWORD = "5555"
   DB_HOST     = "localhost"
   DB_PORT     = "5432"
   DB_NAME     = "qqsm_db"

   DATABASE_URL = (
       f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
   )
   ```

7. **Crear la base de datos**

   Con PostgreSQL en ejecución, accede a la consola y ejecuta:

   ```bash
   psql -U postgres
   ```

   ```sql
   CREATE DATABASE qqsm_db;
   \q
   ```

   Ejecuta este paso desde cualquier ubicación de tu sistema; no es necesario el entorno virtual.

8. **Cargar el esquema de la base de datos**

   Desde el directorio `QQSM` y con el entorno virtual activo, ejecuta el script `setupDB.sql` para crear tablas y datos iniciales:

   ```bash
   psql -U postgres -d qqsm_db -f setupDB.sql
   ```

9. **Ejecutar la aplicación**

Inicia la aplicación desde el directorio `QQSM`, con el entorno virtual activo:

```bash
reflex run
```

La aplicación se abrirá por defecto en [http://localhost:3000](http://localhost:3000). Puedes cambiar este puerto y otras opciones en el fichero `rx.config.py`.

---

## Recursos

* **Carpeta `img/`**: contiene imágenes utilizadas en la interfaz y assets del proyecto.

## Autores

* [acatocaton](https://github.com/acatocaton)
* [arojosan](https://github.com/arojosan)
* [cintiacpr](https://github.com/cintiacpr)
* [MVGDCRB](https://github.com/MVGDCRB)

*Este README ha sido generado como parte del Trabajo de Fin de Grado de la UCM.* ha sido generado como parte del Trabajo de Fin de Grado de la UCM.\* como parte del Trabajo de Fin de Grado de la UCM.\*
