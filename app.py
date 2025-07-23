import os
import tempfile
import shutil
import asyncio
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from shadai_eval import analizar_cv,generar_pdf
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analizar", response_class=HTMLResponse)
async def analizar(
    request: Request,
    cargo: str = Form(...),
    archivo: List[UploadFile] = File(...)
):
    resultados = []

    for archivo_individual in archivo:
        # Crear carpeta temporal para cada archivo
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, archivo_individual.filename)
            with open(file_path, "wb") as f:
                f.write(await archivo_individual.read())

            resultado = await analizar_cv(file_path, cargo)
            resultados.append(resultado)

    # Selección de mejores resultados
    if len(resultados) >= 3:
        top_resultados = sorted(resultados, key=lambda x: x["score"], reverse=True)[:3]
    elif len(resultados) == 2:
        top_resultados = sorted(resultados, key=lambda x: x["score"], reverse=True)[:2]
    else:
        top_resultados = resultados

    pdf_path = os.path.join("static", "resultado.pdf")
    generar_pdf(top_resultados, cargo, pdf_path)

   
    return templates.TemplateResponse("index.html", {
        "request": request,
        "top_resultados": top_resultados,
        "cargo": cargo,
        "pdf_ready":True
    })
