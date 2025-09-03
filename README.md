# Proyecto de clasificación de emociones basado en POO y TensorFlow

## Descripción

Este proyecto implementa una red neuronal para la **clasificación de emociones en frases en español**, utilizando **Python, TensorFlow y Programación Orientada a Objetos (POO)**.  

El sistema permite:  

- Predecir emociones como **ira, tristeza, felicidad, sorpresa, miedo** y **neutral**.
- Guardar correcciones manuales de las predicciones.  
- Reentrenar el modelo en tiempo real con los nuevos ejemplos.  
- Persistir tanto el modelo como el tokenizer y las correcciones en base de datos.  

Está diseñado de manera modular, siguiendo principios de **arquitectura limpia**, con separación en capas (`model`, `services`, `repositories`, etc.).

## Estructura del proyecto

src/
│   config.py              # Configuración general
│   evaluate.py            # Script para evaluar el modelo con datos de prueba
│   init_db.py             # Inicializa la base de datos SQLite
│   main.py                # Punto de entrada principal (interfaz por consola)
│   modelo.keras           # Modelo inicial (si existe)
│   red_emociones.db       # Base de datos SQLite
│   retrain.py             # Reentrenamiento con feedback
│   __init_.py
│
├───data/
│   base_data.py           # Dataset base de entrenamiento
│
├───db/
│   database.py            # Configuración de la conexión a la BD
│   orm_models.py          # Modelos ORM para la BD
│__init_.py
│
├───model/
│   emotion_model.py       # Definición de la red neuronal (EmotionModel)
│   tokenizer_manager.py   # Tokenizer persistente (manejo de secuencias)
│   __init_.py
│
├───repositories/
│   base_repository.py        # Repositorio base (manejo genérico de la sesión DB)
│   correction_repository.py  # Manejo de correcciones (feedback del usuario)
│   emotion_repository.py     # Manejo de predicciones guardadas
│   __init_.py
│
├───saved/
│   emotion_model.keras    # Modelo entrenado persistido
│   tokenizer.pkl          # Tokenizer guardado
│
├───services/
│   feedback_service.py    # Manejo de feedback/correcciones
│   predictor_service.py   # Servicio principal de predicción y entrenamiento
│   __init_.py
│

## Cómo ejecutar el proyecto

### 1. Instalar dependencias

Desde la raíz del proyecto:

```sh
pip install -r requirements.txt
````

### 2. Inicializar la base de datos

Antes del primer uso:

```sh
cd src
python init_db.py
```

### 3. Ejecutar el programa principal

Interfaz por consola para probar predicciones en frases:

```sh
python main.py
```

### 4. Reentrenar el modelo con correcciones

Si ya has agregado feedback en la base de datos:

```sh
python retrain.py
```

### 5. Evaluar el modelo

Con un dataset de prueba definido en `data/base_data.py`:

```sh
python evaluate.py
```

## Notas técnicas

- **Modelo**: Red neuronal simple con `Embedding + GlobalAveragePooling + Dense` implementada en TensorFlow/Keras.
- **Tokenización**: Persistencia del tokenizer (`tokenizer.pkl`) para garantizar que los datos de entrenamiento y predicción usen la misma representación.
- **Base de datos**: Correcciones y datos se almacenan en SQLite (`red_emociones.db`) usando un pequeño ORM.
- **Reentrenamiento**: El script `retrain.py` permite que el modelo se actualice con los datos corregidos por el usuario.
- **Organización**: Arquitectura modular con capas separadas (`model`, `repositories`, `services`, `utils`).

## Flujo típico de uso

1. Ejecutar `main.py` para probar el clasificador.
2. Ingresar frases y recibir predicciones con nivel de confianza.
3. Corregir manualmente cuando una emoción esté mal clasificada (se guarda en la BD).
4. Ejecutar `retrain.py` para reentrenar el modelo con las correcciones acumuladas.
5. (Opcional) Ejecutar `evaluate.py` para medir el rendimiento del modelo.
