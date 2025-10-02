from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from api.dependencies import services_available

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    status = "✅ Funcionando" if services_available else "❌ Error en servicios"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Red Neuronal de Emociones</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; }}
            h1 {{ text-align: center; }}
            label {{ display: block; margin-top: 15px; }}
            input, select, button, textarea {{ width: 100%; padding: 8px; margin-top: 5px; border-radius: 5px; border: 1px solid #ccc; }}
            button {{ background: #007bff; color: white; font-weight: bold; cursor: pointer; }}
            button:hover {{ background: #0056b3; }}
            .result {{ margin-top: 20px; padding: 15px; border-radius: 5px; background: #e9ecef; }}
            #volverBtn {{ background: #28a745; margin-top: 10px; }}
            #volverBtn:hover {{ background: #1e7e34; }}
            .status {{ background: #d4edda; padding: 10px; border-radius: 5px; margin-bottom: 20px; color: #155724; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Predicción de Emociones</h1>
            <div class="status"><strong>Estado del sistema:</strong> {status}</div>

            <label for="textInput">Escribe un texto:</label>
            <textarea id="textInput" rows="3"></textarea>

            <button type="button" onclick="predictEmotion()">Predecir Emoción</button>

            <div id="prediction" class="result" style="display:none;">
                <p><strong>Predicción:</strong> <span id="predictedEmotion"></span></p>
                <p><strong>Confianza:</strong> <span id="confidence"></span></p>

                <label for="correctEmotion">¿Es correcta la emoción? (opcional, corrígela si es necesario)</label>
                <select id="correctEmotion">
                    <option value="">-- Selecciona si quieres corregir --</option>
                    <option value="ira">Ira</option>
                    <option value="tristeza">Tristeza</option>
                    <option value="felicidad">Felicidad</option>
                    <option value="sorpresa">Sorpresa</option>
                    <option value="miedo">Miedo</option>
                    <option value="neutral">Neutral</option>
                </select>

                <button type="button" onclick="sendFeedback()">Enviar Feedback</button>
                <p id="feedbackMsg" style="color: green; font-weight:bold;"></p>
                <button type="button" id="volverBtn" onclick="resetForm()">Volver a preguntar</button>
            </div>
        </div>

        <script>
            let lastPrediction = null;

            async function predictEmotion() {{
                const text = document.getElementById("textInput").value.trim();
                if (!text) return alert("Escribe algo para predecir.");

                const response = await fetch("/predict_feedback", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ text }})
                }});

                const data = await response.json();
                lastPrediction = data;

                document.getElementById("predictedEmotion").textContent = data.emotion;
                document.getElementById("confidence").textContent = data.confidence.toFixed(2);
                document.getElementById("prediction").style.display = "block";
                document.getElementById("feedbackMsg").textContent = "";
            }}

            async function sendFeedback() {{
                const corrected = document.getElementById("correctEmotion").value;
                if (!corrected) return alert("Selecciona una emoción corregida antes de enviar.");

                const text = document.getElementById("textInput").value.trim();

                const response = await fetch("/predict_feedback?corrected_emotion=" + corrected, {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ text }})
                }});

                const data = await response.json();
                document.getElementById("feedbackMsg").textContent = "✅ Feedback registrado. ID: " + data.feedback_id;
            }}

            function resetForm() {{
                document.getElementById("textInput").value = "";
                document.getElementById("predictedEmotion").textContent = "";
                document.getElementById("confidence").textContent = "";
                document.getElementById("correctEmotion").selectedIndex = 0;
                document.getElementById("feedbackMsg").textContent = "";
                document.getElementById("prediction").style.display = "none";
                lastPrediction = null;
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
