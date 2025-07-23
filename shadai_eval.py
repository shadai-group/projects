import asyncio
from shadai.core.agents import Agent
from shadai.core.session import Session
from shadai.core.enums import AIModels
import os
import json

os.environ['SHADAI_API_KEY'] = 'your_api_key'

async def analizar_cv(pdf_path: str, cargo: str):
    async with Session(
        type="standard",
        language="es",
        llm_model=AIModels.GEMINI_2_0_FLASH,
        delete=False
    ) as session:

        input_dir = os.path.dirname(pdf_path)
        await session.ingest(input_dir=input_dir)

        agente = Agent(
            name="EvaluadorCurriculum",
            session=session,
            description="Agente que evalúa CVs para un cargo específico",
            agent_prompt=f"""
Eres un experto en selección de personal. Evalúa si el CV cargado (PDF) corresponde al perfil:

'{cargo}'

Devuelve tu respuesta en JSON estricto con los campos:
{{
  "nombre": "Nombre del candidato",
  "score": 0-100,
  "decision": "Apto" o "No Apto",
  "justificacion": "Breve análisis del perfil en relación al cargo"
}}
""",
            use_history=True
        )

        prompt = f"""
Eres un experto en selección de personal. Evalúa el currículum cargado para el cargo: **{cargo}**.
 Responde únicamente con un bloque de código Python que contenga un `dict(...)` estructurado así:

```python
dict(
    nombre="Nombre completo del candidato",
    score=75.5,
    decision="Apto" o "No Apto",
    justificacion="Breve justificación del puntaje y decisión"
)

 No agregues ningún texto fuera del bloque ```python ... ```.

 El contenido debe ser completamente parseable como un diccionario de Python usando eval().
"""

        response = await session.chat(prompt)

        try:
            if not response or not str(response).strip():
                raise ValueError("Respuesta vacía del agente")

            print(" Respuesta bruta:", response)

            # Limpiar y preparar el texto para parseo
            cleaned = clean_code_block(str(response))
            formatted = format_dict_keys_and_values(cleaned)

            result = json.loads(formatted)
            print(result)
            result["score"] = float(result.get("score", 0))
            return result

        except Exception as e:
            print(" Error interpretando dict estilo Python:", e)
            return {
                "nombre": os.path.basename(pdf_path),
                "score": 0.0,
                "decision": "No evaluado",
                "justificacion": f" Error interpretando la respuesta: {e}"
            }

import re

def clean_code_block(text):
    return re.sub(r'```[a-zA-Z]*', '', text).replace('```', '').strip()

def format_dict_keys_and_values(text):
    text = text.replace("dict(", "{").replace(")", "}")
    text = re.sub(r'(\w+)=', r'"\1":', text)
    return text

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generar_pdf(resultados, cargo, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    flowables = []

    # Título
    titulo = f"<b>■ Evaluación de Currículums – Cargo: {cargo}</b>"
    flowables.append(Paragraph(titulo, styles['Title']))
    flowables.append(Spacer(1, 12))

    # Contenido de candidatos
    for i, r in enumerate(resultados, start=1):
        nombre = r["nombre"]
        score = r["score"]
        decision = r["decision"]
        justificacion = r["justificacion"]

        texto = f"<b>{i}. {nombre} – {decision} (Score: {score:.1f}/100)</b><br/><br/>{justificacion}"
        flowables.append(Paragraph(texto, styles['Normal']))
        flowables.append(Spacer(1, 16))

    # Generar PDF
    doc.build(flowables)
