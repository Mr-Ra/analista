# **Proyecto: APIs, Módulos Web y Uso de IA**

## **Capturas de proyecto**
<div style="display: flex; overflow-x: auto; gap: 10px; max-width: 100%; scroll-snap-type: x mandatory;">
    <img src="screenshots/ss1.png" alt="Captura #1" width="500" style="scroll-snap-align: start;">
    <img src="screenshots/ss2.png" alt="Captura #2" width="500" style="scroll-snap-align: start;">
    <img src="screenshots/ss3.png" alt="Captura #3" width="500" style="scroll-snap-align: start;">
</div>


Este proyecto incluye la implementación de APIs clave, módulos web avanzados, y el uso de herramientas de IA para análisis y optimización. Aquí se detallan las funcionalidades y características principales.

---

## **Parte 1: APIs**

### **1. API de Inicio de Sesión**
- **Descripción:**  
  Permite a usuarios anónimos iniciar sesión y obtener un JWT para autenticación.
- **Detalles del JWT:**  
  - Contenido:  
    - `id_usuario`  
    - `rol`  
    - Tiempo de expiración: 15 minutos.
  - Firmado digitalmente para garantizar seguridad.

---

### **2. API de Carga y Validación de Archivos**
- **Funcionalidad:**  
  Endpoint para subir archivos CSV junto con dos parámetros adicionales. Realiza las siguientes acciones:
  1. **Subida a AWS S3:**  
     - El archivo se almacena en un bucket configurado en AWS.
  2. **Procesamiento en SQL Server:**  
     - El contenido del archivo es procesado y almacenado en la base de datos.
  3. **Validaciones Aplicadas:**  
     - Detecta valores vacíos, tipos incorrectos o duplicados.  
     - Devuelve una lista detallada con las validaciones realizadas.

- **Requisitos de Acceso:**  
  - Endpoint restringido a usuarios con roles específicos.  
  - Validación mediante token JWT.

---

### **3. API de Renovación de Token**
- **Descripción:**  
  Proporciona un nuevo token JWT con tiempo de expiración adicional.
- **Requisitos:**  
  - Solo accesible si el token original aún no ha expirado.

---

## **Parte 2: Módulos Web (Análisis de Documentos con IA)**

### **1. Módulo de Análisis de Documentos**
- **Descripción:**  
  Pantalla web para cargar documentos en formatos PDF, JPG o PNG.  
  Ofrece las siguientes funcionalidades:  
  1. **Clasificación Automática:**  
     - Clasifica los documentos en:
       - **Factura:** Contiene datos financieros.
       - **Información:** Contenido general.
  2. **Extracción Automática de Datos:**  
     - **Si es Factura:** Extrae información como:
       - Cliente (nombre y dirección).
       - Proveedor (nombre y dirección).
       - Número de factura, fecha, productos (cantidad, nombre, precio unitario, total).
       - Total de la factura.
     - **Si es Información:**  
       - Extrae descripción y resumen del contenido.  
       - Realiza análisis de sentimiento (positivo, negativo o neutral).

- **Recomendación de IA:**  
  Herramientas como **AWS Textract**, **Azure Cognitive Services** o **OpenAI** para la extracción y análisis.

---

### **2. Módulo Histórico**
- **Descripción:**  
  Pantalla para visualizar un registro de eventos registrados en el sistema.
- **Detalles Registrados:**  
  - ID del evento  
  - Tipo (Carga de documento, IA, Interacción del usuario).  
  - Descripción del evento.  
  - Fecha y hora.
- **Funcionalidades Adicionales:**  
  - Filtros por tipo, descripción o rango de fechas.  
  - Exportación del log a formato Excel.

---

<!-- ## **Parte 3: Uso de IA y Refactorización de Código**

### **1. Refactorización Dinámica**
- **Herramientas Utilizadas:**  
  - ChatGPT, Copilot, Claude, entre otros.
- **Proceso:**  
  - Cada refactorización incluye un commit en GitHub con el código original.  
  - Los commits deben incluir:  
    - La frase: `"Refactorización con [Nombre de la IA]"`.

---

### **2. Documentación Generada con IA**
- **Requisitos:**  
  - Descripción clara para cada función.  
  - Detalles incluidos:
    - ¿Qué hace la función?  
    - ¿Qué parámetros recibe y de qué tipo?  
    - ¿Qué dato regresa y de qué tipo?

---

### **3. Pruebas Unitarias**
- **Requisitos:**  
  - Crear al menos **10 casos de prueba unitarios** para cada método.  
  - Herramientas: Pytest o Unittest. -->

---

## **Cómo Ejecutar el Proyecto**
1. **Configuración del Entorno:**
   - Crear entorno virtual con paquete **"venv"**: `python -m venv venv`
   - Activar entorno virtual:
    - **Windows**: `venv\scripts\activate`
    - **Linux**: `source venv\scripts\activate`   
   - Instalar dependencias: `pip install -r requirements.txt`
   - Configurar las siguientes variables de entorno en un archivo `.env` en la carpeta raiz:
   
      #### **a. Autenticación y autorización:**      
      - `JWT_SECRET`: Cadena para la firma de tokens de acceso y renovación.
      - `JWT_ALGORITHM`: Configurar con el valor ``"HS256"``
      - ``DATABASE_URL``: Para evitar conflictos de asincronicidad con SQL Server, asegúrese de que la cadena empiece con ``"mssql+aioodbc"``
        - **Ejemplo:**
          `mssql+aioodbc://user:password@server_name/db_name?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes`
          

      #### **b. AWS S3**:
        - `BUCKET_NAME` = `"analista-files"`

        - `AWS_ACCESS_KEY_ID` = `"test"`

        - `AWS_SECRET_ACCESS_KEY` = `"test"`

        - `S3_ENDPOINT_URL` = `"http://localhost.localstack.cloud:4566"`     

2. **Migraciones de Base de Datos:**
   - Generar migraciones: `alembic revision --autogenerate -m "init"`
   - Aplicar migraciones a DB: `alembic upgrade head`

3. **Iniciar el Servidor FastAPI:**
   - Correr servidor: `fastapi run main.py --reload`
   - Puede ver la documentación automática de los endpoints generada por Swagger accediendo a `localhost:8000/docs`
   - Para utilizar los endpoints de carga de archivos, se requiere que el usuario tenga rol de administrador `"admin"`. Por defecto, los usuarios creados a través de `/register` tendrán el rol `"user"`

   - **Actualizar rol de usuario a administrador**

      Para actualizar el rol de un usuario en la base de datos a "admin", puedes usar la siguiente consulta SQL:

      ```sql
      UPDATE [user]
      SET role = 'admin'
      WHERE email = 'example@mail.com';

4. ### **Comandos LocalStack para AWS S3**
    LocalStack es un emulador de servicios en la nube y soporta la emulación de varios servicios de AWS como S3, AWS Lambda, DynamoDB, etc.
    Además, es compatible con el SDK de AWS para Python **boto3**.
    Más información en: <a href="https://docs.localstack.cloud/getting-started/" target="_blank"> LocalStack Getting Started </a>


    - Cargar y ejecutar contenedor de LocalStack: ``docker-compose up``

    - Crear un bucket local de S3: ``aws --endpoint-url=http://localhost:4566 s3 mb s3://analista-files``

    - Enlista los buckets creados: `aws --endpoint-url=http://localhost:4566 s3 ls`
    
    - Puedes `cargar archivos` usando `aws --endpoint-url=http://localhost:4566 s3 cp sample.csv s3://analista-files`


    - Enlista los archivos cargados al bucket: `aws --endpoint-url=http://localhost:4566 s3 ls s3://analista-files`

    - Para descargar un archivo a partir de su S3 Key:
  `aws --endpoint-url=http://localhost:4566 s3 cp s3://analista-files/s3_key ./archivo_descargado.csv`.
    - Para efectos de este proyecto, el S3 Key se corresponde con el identificador único que se genera automáticamente en la DB al guardar un archivo en el bucket.

---

5. ### Descarga de modelo LLM ###
  - Descarga el modelo `llama-3.2-1b-instruct-q8_0.gguf` (Ver más sobre <a href="https://huggingface.co/hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF" target="_blank"> llama-3.2-1b </a>)
  - Puedes utilizar diferentes alternativas para su descarga, por ejemplo, utilicé LM Studio para descargarlo desde HuggingFace
  - Asegúrate de llevar el modelo al directorio `./llms/models` para que este sea reconocido y se puedan ejecutar las inferencias localmente

---

6. ### **Servir el módulo de carga de archivos** ###
 - Este módulo permite cargar archivos PDF o imágenes para hacer inferencias
 - Cambia al directorio `frontend` con el comando `cd frontend`
 - Ejecuta el siguiente comando para servir el módulo de carga: `python -m http.server 8001`
 - Accede a `http://localhost:8001/index.html` e inicia sesión si ya has creado un usuario
 - Asegúrate de acceder con un usuario con rol de administrador, ya que los endpoints relacionados a este módulo no son de acceso público

---

### **Tecnologías Utilizadas**
- **Backend:** Python (FastAPI, SQLModel, SQLAlchemy, Alembic, PyDantic)
- **Base de Datos:** SQL Server para documentos (relacional), ChromaDB para embeddings (vectorial)
- **Almacenamiento:** AWS S3 (Con LocalStack)
- **Inteligencia Artificial:**
  - Small Vision Language Model con SmolVLM para procesamiento multimodal de imágenes (Ver más sobre <a href="https://huggingface.co/spaces/HuggingFaceTB/SmolVLM" target="_blank"> SmolVLM </a>)
  - Modelo LLM para procesamiento de PDFs localmente: `llama-3.2-1b-instruct-q8_0.gguf`
  - Modelo de embeddings para búsqueda semántica: `all-mpnet-base-v2` de HuggingFace (Ver más sobre <a href="https://huggingface.co/sentence-transformers/all-mpnet-base-v2" target="_blank"> all-mpnet-base-v2 </a>)
  - Langchain 
  - Gradio


---

# **Limitaciones**
- Al ejecutar el modelo de llama localmente, podrían presentarse periodos largos de inferencia
- Al estar utilizando un modelo con una baja cantidad de parámetros, su precisión se puede ver afectada 
- Al procesar PDFs, el cáculo de similitud por coseno entre embeddings y almacenamiento vectorial se realizan en memoria durante las ejecuciones de las inferencias, por lo que no persisten
- Para efectos experimentales, se recomienda que los PDFs contengan máximo 2 páginas, ya que la ventana de contexto es limitada (límite de tokens de entrada)
- El procesamiento de imágenes con SmolVLM varía en precisión al rellenar los campos especificados


---










