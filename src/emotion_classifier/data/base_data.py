class BaseDataManager:
    """Gestiona el acceso a las frases, etiquetas y emociones base para entrenamiento."""
    def __init__(self):
        self.frases = [
            'Estoy furioso con lo que pasó',
            'Me siento muy triste hoy',
            '¡Qué felicidad tan grande!',
            '¡Qué sorpresa tan inesperada!',
            'Tengo miedo de lo que pueda pasar',
            'Solo estoy aquí, sin emociones fuertes',
            'Me enoja cuando las cosas no salen bien',
            'Lloro porque extraño a mi amigo',
            'Estoy muy contento por el premio',
            'No esperaba que eso sucediera',
            'Estoy asustado por la noticia',
            'No siento nada en particular'
        ]
        # Las etiquetas corresponden a las emociones en el mismo orden
        self.etiquetas = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
        self.emociones = ['ira', 'tristeza', 'felicidad', 'sorpresa', 'miedo', 'neutral']

    def obtener_datos(self):
        """Devuelve las frases y etiquetas base."""
        return self.frases, self.etiquetas

    def obtener_emocion(self, etiqueta):
        """Devuelve el nombre de la emoción dado el índice de etiqueta."""
        return self.emociones[etiqueta]

