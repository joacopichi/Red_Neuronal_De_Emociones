# Red Neuronal de Emociones en Español

## Descripción

Este proyecto implementa una red neuronal para la **clasificación de emociones en frases en español** usando **Python, TensorFlow y Programación Orientada a Objetos (POO)**.  
Permite predecir emociones como **ira, tristeza, felicidad, sorpresa, miedo** y **neutral**, guardar correcciones manuales, reentrenar el modelo en tiempo real y persistir tanto el modelo como el tokenizer y las correcciones en una base de datos.  
La arquitectura es modular y sigue principios de ingeniería de software como SOLID, herencia, polimorfismo y patrón singleton.

---

## Estructura del Proyecto

```.
Red_Neuronal_De_Emociones/
│
├── requirements.txt                # Dependencias del proyecto
├── Dockerfile                      # Imagen Docker para despliegue
├── README.md                       # Documentación principal
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # Flujo de integración continua (lint, test, build)
│
├── src/
│   ├── config.py                   # Configuración global del sistema
│   ├── init_db.py                  # Inicializa la base de datos SQLite
│   ├── modelo.keras                # Archivo del modelo inicial guardado
│   ├── red_emociones.db            # Base de datos SQLite con correcciones y predicciones
│   │
│   ├── terminal/
│   │   ├── __init__.py             # Inicialización del módulo terminal
│   │   ├── main.py                 # Interfaz por consola para probar el clasificador
│   │   ├── retrain.py              # Script para reentrenar el modelo con feedback del usuario
│   │   └── evaluate.py             # Script para evaluar el modelo con datos de prueba
│   │
│   ├── data/
│   │   └── base_data.py            # Dataset base de entrenamiento y pruebas
│   │
│   ├── db/
│   │   ├── __init__.py             # Inicialización del módulo db
│   │   ├── database.py             # Gestión de la conexión a la base de datos (singleton)
│   │   └── orm_models.py           # Modelos ORM para la base de datos
│   │
│   ├── model/
│   │   ├── __init__.py             # Inicialización del módulo model
│   │   ├── emotion_model.py        # Definición de la red neuronal y lógica de predicción
│   │   └── tokenizer_manager.py    # Gestión y persistencia del tokenizer
│   │
│   ├── repositories/
│   │   ├── __init__.py             # Inicialización del módulo repositories
│   │   ├── base_repository.py      # Repositorio base para operaciones genéricas en la BD
│   │   ├── correction_repository.py# Manejo de correcciones de usuarios
│   │   └── emotion_repository.py   # Manejo de predicciones guardadas
│   │
│   ├── saved/
│   │   ├── emotion_model.keras     # Modelo entrenado persistido
│   │   └── tokenizer.pkl           # Tokenizer guardado para uso consistente
│   │
│   ├── services/
│   │   ├── __init__.py             # Inicialización del módulo services
│   │   ├── feedback_service.py     # Lógica para gestionar feedback y correcciones
│   │   └── predictor_service.py    # Servicio principal de predicción y entrenamiento
│   │
│   └── api/
│       ├── __init__.py             # Inicialización del módulo api
│       ├── config.py               # Configuración específica de la API
│       ├── dependencies.py         # Inyección de dependencias para la API
│       ├── main.py                 # Punto de entrada de la API FastAPI
│       ├── schemas.py              # Esquemas de datos para la API
│       ├── utils.py                # Funciones utilitarias para la API
│       └── routes/
│           ├── feedback.py         # Rutas para feedback/correcciones
│           ├── health.py           # Ruta de salud del sistema
│           ├── prediction.py       # Rutas de predicción de emociones
│           ├── root.py             # Ruta raíz de la API
│           └── training.py         # Rutas para reentrenamiento del modelo
│
├── tests/
│   ├── __init__.py                 # Inicialización del módulo tests
│   ├── test_emotion_model.py       # Pruebas unitarias para emotion_model
│   ├── test_predictor_service.py   # Pruebas unitarias para predictor_service
│   ├── test_feedback_service.py    # Pruebas unitarias para feedback_service
│   ├── test_database.py            # Pruebas unitarias para la conexión a la base de datos
│   └── test_api_routes.py          # Pruebas de integración para las rutas de la API
```

---

## Uso de Carpetas y Archivos

- **config.py**: Configuración global del sistema.
- **init_db.py**: Inicializa la base de datos SQLite.
- **modelo.keras**: Modelo inicial guardado.
- **red_emociones.db**: Base de datos SQLite con correcciones y predicciones.

**Carpetas:**
-**terminal/**: Scripts de consola para interacción, reentrenamiento y evaluación del modelo:
  -`main.py`: Interfaz por consola para probar el clasificador.
  -`retrain.py`: Script para reentrenar el modelo con feedback del usuario.
  -`evaluate.py`: Script para evaluar el modelo con datos de prueba.
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

### 3. Ejecutar los scripts de consola

Ubícate en la carpeta `src` para ejecutar los scripts de consola usando el flag `-m` y el módulo `terminal`:

- Para probar predicciones en frases:
  .```sh
  python -m terminal.main
  .```
- Para reentrenar el modelo con correcciones:
  .```sh
  python -m terminal.retrain
  .```
- Para evaluar el modelo:
  .```sh
  python -m terminal.evaluate
  .```

### 4. Ejecutar la API con FastAPI

Desde la raíz del proyecto (sin la carpeta `src` en la ruta):

```sh
uvicorn api.main:app --reload
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

El entrenamiento se realiza con los datos tokenizados y las etiquetas codificadas, especificando el número de épocas y el tamaño de lote. Este proceso puede repetirse utilizando el script `terminal/retrain.py` para incorporar nuevas correcciones y mejorar el rendimiento del modelo.

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

## Ejecución con Docker

Puedes levantar la API fácilmente usando Docker:

```sh
docker build -t red-emociones .
docker run -p 8000:8000 red-emociones
```

Esto expondrá la API en `http://localhost:8000`.

---

## Integración continua (CI)

Este proyecto incluye un flujo de trabajo de GitHub Actions para asegurar calidad y despliegue:

- **Lint:** Verifica la calidad del código con flake8.
- **Test:** Ejecuta los tests con pytest.
- **Build:** Construye la imagen Docker.

El flujo se encuentra en `.github/workflows/ci.yml` y se ejecuta automáticamente en cada push o pull request a la rama `main`.

---

## Flujo típico de uso

1. Ejecutar `main.py` para probar el clasificador por consola.
2. Ingresar frases y recibir predicciones con nivel de confianza.
3. Corregir manualmente cuando una emoción esté mal clasificada (se guarda en la BD).
4. Ejecutar `retrain.py` para reentrenar el modelo con las correcciones acumuladas.
5. (Opcional) Ejecutar `evaluate.py` para medir el rendimiento del modelo.
6. (Opcional) Levantar la API con FastAPI para integración con otros sistemas.
7. (Opcional) Levantar la API con Docker para despliegue sencillo.
8. (Opcional) Validar calidad y despliegue automático con GitHub Actions.

---

## Pruebas automáticas

Las pruebas unitarias y de integración se encuentran en la carpeta `tests/`.  
Para ejecutarlas, usa:

```sh
pytest tests
```

Los principales módulos testeados son:

- `model/emotion_model.py`
- `services/predictor_service.py`
- `services/feedback_service.py`
- `db/database.py`
- `api/routes/*.py`

La integración continua ejecuta automáticamente estos tests en cada push o pull request.

---
