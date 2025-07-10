# Proyecto de clasificación de emociones basado en POO y TensorFlow

## Descripción

Este proyecto implementa una red neuronal simple para la clasificación de emociones en frases en español. Utiliza Python, TensorFlow y Programación Orientada a Objetos (POO) para estructurar el código en servicios y modelos reutilizables.  
El sistema puede predecir emociones como **ira, tristeza, felicidad, sorpresa, miedo** y **neutral** a partir de texto ingresado por el usuario. Además, permite corregir manualmente las predicciones y reentrenar el modelo en tiempo real con los nuevos ejemplos.

## Cómo ejecutar el proyecto
1. **Instala las dependencias**  
   Abre una terminal en la carpeta raíz del proyecto y ejecuta:
   ```sh
   pip install -r requirements.txt
   ```

2. **Ejecuta el programa**  
   Cambia al directorio `src` y ejecuta el archivo principal como módulo:
   ```sh
   cd src
   python -m emotion_classifier.main
   ```

3. **Uso**  
   - Ingresa una frase para analizar su emoción.
   - El sistema mostrará la emoción predicha y el nivel de confianza.
   - Si la predicción es incorrecta, puedes corregirla y el modelo se actualizará automáticamente.

## Notas técnicas

- El modelo utiliza una red neuronal simple implementada con TensorFlow/Keras.
- La vectorización del texto es básica (puedes mejorarla según tus necesidades).
- Las correcciones se almacenan en `src/emotion_classifier/data/corrections.json` y se usan para reentrenar el modelo incrementalmente.
- El código está organizado usando POO para facilitar su mantenimiento y extensión.
