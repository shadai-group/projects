# 🧠 Evaluador de Currículums con ShadAI

Este proyecto permite analizar automáticamente archivos PDF de currículums usando inteligencia artificial mediante la API de [ShadAI](https://docs.shadai.ai/). Está desarrollado con **FastAPI** y permite cargar múltiples archivos para obtener un informe evaluativo con puntuación, veredicto y justificación.

---

## 🚀 Características

- Evaluación automática de currículums en PDF para un cargo específico.
- Interfaz web amigable para cargar y visualizar resultados.
- Resultados exportables en PDF.
- Integración directa con agentes inteligentes de ShadAI.

---


## 📁 Estructura del proyecto

```text
Proyectos ShadAi/
├── app.py               # API principal con FastAPI
├── shadai_eval.py       # Lógica de análisis usando ShadAI
├── templates/
│   └── index.html       # Interfaz web
├── static/
│   ├── style.css        # Estilo del frontend
│   └── resultado.pdf    # PDF generado
├── archivos/            # Currículums temporales subidos
```
## ⚙️ Instalación

Instala las dependencias necesarias con:

```bash
pip install fastapi uvicorn jinja2 shadai aiofiles reportlab
```

## ▶️ Ejecución
Corre el servidor desde terminal con:

```bash

uvicorn app:app --reload
```
Luego abre tu navegador en:
http://127.0.0.1:8000

## 🧪 Uso
- Abre el navegador y entra a http://127.0.0.1:8000

- Especifica el cargo al que aplican los currículums.

- Carga uno o varios archivos .pdf.

- Haz clic en Analizar.

- Visualiza los resultados y descarga el informe si es necesario.
---

## ✨ Inspírate

Pon a prueba tus conocimientos e ideas, y con lo que aprendas de este proyecto, **empieza los propios tuyos**.  
**Los límites están en tu creatividad. 🚀**
