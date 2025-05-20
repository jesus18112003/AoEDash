from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pattern = r"^.{1,2}\s{2}(.+?)\s\((\d+)\)\sRank\s#(\w+),.*?(\w+)%\swinrate"

@app.get("/estadisticas")
def obtener_estadisticas(profile_id: int = Query(...)):  # Ahora recibe un ID por parámetro
    url = f"https://data.aoe2companion.com/api/nightbot/rank?profile_id={profile_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        texto = response.text.strip().replace("\xa0", " ").strip('"')
        match = re.search(pattern, texto)
        
        if not match:
            return {"error": "No se encontraron datos para este ID"}
            
        ranking = match.group(3)
        return {
            "nombre": match.group(1),
            "elo": int(match.group(2)),
            "ranking": int(ranking) if ranking.isdigit() else None,
            "winrate": int(match.group(4)) if match.group(4).isdigit() else None
        }
    except Exception as e:
        return {"error": f"Error al obtener datos: {str(e)}"}
