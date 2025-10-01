# Red Neuronal de Emociones en Español

## Descripción

Este proyecto implementa una red neuronal para la **clasificación de emociones en frases en español** usando **Python, TensorFlow y Programación Orientada a Objetos (POO)**.  
Permite predecir emociones como **ira, tristeza, felicidad, sorpresa, miedo** y **neutral**, guardar correcciones manuales, reentrenar el modelo en tiempo real y persistir tanto el modelo como el tokenizer y las correcciones en una base de datos.  
La arquitectura es modular y sigue principios de ingeniería de software como SOLID, herencia, polimorfismo y patrón singleton.

---

## Estructura del Proyecto

```.

src/
│   config.py              # Configuración general del sistema
│   evaluate.py            # Script para evaluar el modelo con 
│   init_db.py             # Inicializa la base de datos SQLite
│   main.py                # Interfaz por consola para 
│   modelo.keras           # Modelo inicial guardado
│   red_emociones.db       # Base de datos SQLite con 
│   retrain.py             # Script para reentrenar el modelo 
│
├───data/
│   base_data.py           # Dataset base de entrenamiento y 
│
├───db/
│   database.py            # Gestión de la conexión a la base
│   orm_models.py          # Modelos ORM para la base de datos
│
├───model/
│   emotion_model.py       # Definición de la red neuronal
│   tokenizer_manager.py   # Gestión y persistencia del 
│
├───repositories/
│   base_repository.py        # Repositorio base para 
│   correction_repository.py  # Manejo de correcciones de 
│   emotion_repository.py     # Manejo de predicciones guardadas
│
├───saved/
│   emotion_model.keras    # Modelo entrenado persistido
│   tokenizer.pkl          # Tokenizer guardado para uso 
│
├───services/
│   feedback_service.py    # Lógica para gestionar feedback y 
│   predictor_service.py   # Servicio principal de predicción y 
│
├───api/
│   main.py                # Punto de entrada para la API 
│   config.py              # Configuración específica de la API
│   dependencies.py        # Inyección de dependencias para la 
│   schemas.py             # Esquemas de datos para la API
│   utils.py               # Utilidades varias para la API
│   routes/
│       feedback.py        # Rutas para feedback/correcciones
│       health.py          # Ruta de salud del sistema
│       prediction.py      # Rutas de predicción de emociones
│       root.py            # Ruta raíz de la API
│       training.py        # Rutas para reentrenamiento
```

---

## Uso de Carpetas y Archivos

- **config.py**: Configuración global del sistema.
- **evaluate.py**: Evalúa el modelo con datos de prueba.
- **init_db.py**: Inicializa la base de datos SQLite.
- **main.py**: Interfaz por consola para probar el clasificador.
- **modelo.keras**: Modelo inicial guardado.
- **red_emociones.db**: Base de datos SQLite con correcciones y predicciones.
- **retrain.py**: Script para reentrenar el modelo con feedback del usuario.

**Carpetas:**
-**data/**: Contiene el dataset base para entrenamiento y prueba.
-**db/**: Gestión y modelos ORM de la base de datos.
-**model/**: Definición de la red neuronal y manejo del tokenizer.
-**repositories/**: Acceso y gestión de datos en la base de datos.
-**saved/**: Archivos persistentes del modelo y tokenizer.
-**services/**: Lógica de negocio para predicción y feedback.
-**api/**: Implementación de la API REST con FastAPI y sus rutas.

---

## Cómo ejecutar el proyecto

### 1. Instalar dependencias

Desde la raíz del proyecto:

```sh
pip install -r requirements.txt
```

### 2. Inicializar la base de datos

Antes del primer uso:

```sh
cd src
python init_db.py
```

### 3. Ejecutar el programa principal (consola)

Para probar predicciones en frases:

```sh
python main.py
```

### 4. Ejecutar la API con FastAPI

Desde la raíz del proyecto (sin la carpeta `src` en la ruta):

```sh
uvicorn api.main:app --reload
```

### 5. Reentrenar el modelo con correcciones

Si has agregado feedback en la base de datos:

```sh
python retrain.py
```

### 6. Evaluar el modelo

Con el dataset de prueba definido en `data/base_data.py` y con la base de datos:

```sh
python evaluate.py
```

---

## Detalles técnicos del modelo

### Dataset

El dataset utilizado se encuentra en `data/base_data.py`. Contiene frases en español etiquetadas con emociones como ira, tristeza, felicidad, sorpresa, miedo y neutral. Este conjunto de datos sirve tanto para el entrenamiento inicial como para la evaluación y el reentrenamiento del modelo, luego sigue los entrenamientos con este dataset y utiliza la base de datos para una mayor eficiencia.

### Modelo de la red neuronal

La red neuronal está definida en `model/emotion_model.py`. Utiliza TensorFlow/Keras y está diseñada para procesar texto tokenizado y clasificarlo en una de las emociones predefinidas.

### Configuración de capas y nodos/neuronas

La arquitectura del modelo incluye las siguientes capas principales:

- **Embedding**: Convierte las palabras en vectores densos que capturan su significado semántico.
- **GlobalAveragePooling**: Realiza un promedio de los embeddings para obtener un vector representativo de la frase completa.
- **Dense (oculta)**: Una o más capas densas para procesar el vector de la frase.
- **Dense (salida)**: Capa final con activación `softmax` para obtener la probabilidad de cada emoción.

### Compilar

El modelo se compila usando el optimizador Adam, la función de pérdida `categorical_crossentropy` y la métrica de precisión:

### Entrenar

El entrenamiento se realiza con los datos tokenizados y las etiquetas codificadas, especificando el número de épocas y el tamaño de lote. Este proceso puede repetirse utilizando el script `retrain.py` para incorporar nuevas correcciones y mejorar el rendimiento del modelo.

---

## Notas técnicas

- **Modelo** Se utiliza una **red neuronal ligera** implementada con **TensorFlow/Keras**.  
  Su arquitectura está compuesta por:  
  - `Embedding`: transforma palabras en vectores densos que capturan su significado.  
  - `GlobalAveragePooling`: resume toda la frase en un único vector representativo mediante el promedio de embeddings.  
  - Capas `Dense`: procesan ese vector y generan la predicción final con una activación `softmax`, devolviendo la probabilidad de cada emoción.
- **Tokenización**: Persistencia del tokenizer (`tokenizer.pkl`) para asegurar consistencia entre entrenamiento y predicción.
- **Base de datos**: Correcciones y datos almacenados en SQLite (`red_emociones.db`) mediante ORM.
- **Reentrenamiento**: El script `retrain.py` actualiza el modelo con los datos corregidos por el usuario.
- **Organización**: Arquitectura modular y limpia, con separación en capas (`model`, `repositories`, `services`, `api`).

---

## Flujo típico de uso

1. Ejecutar `main.py` para probar el clasificador por consola.
2. Ingresar frases y recibir predicciones con nivel de confianza.
3. Corregir manualmente cuando una emoción esté mal clasificada (se guarda en la BD).
4. Ejecutar `retrain.py` para reentrenar el modelo con las correcciones acumuladas.
5. (Opcional) Ejecutar `evaluate.py` para medir el rendimiento del modelo.
6. (Opcional) Levantar la API con FastAPI para integración con otros sistemas.
