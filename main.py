from fastapi import FastAPI
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

# Lista fija de IDs de jugadores
profile_ids = [21613744, 2664846, 416330, 2251804, 273913, 5592920,
               4489862, 394760, 1663584, 10718686, 2542803, 3075586, 
               10989132, 1790515, 5206099, 197388, 5825958, 4971]

pattern = r"^.{1,2}\s{2}(.+?)\s\((\d+)\)\sRank\s#(\w+),.*?(\w+)%\swinrate"

@app.get("/estadisticas")
def obtener_estadisticas():
    data = []
    for pid in profile_ids:
        try:
            url = f"https://data.aoe2companion.com/api/nightbot/rank?profile_id={pid}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            texto = response.text.strip().replace("\xa0", " ").strip('"')
            match = re.search(pattern, texto)
            
            if match:
                ranking = match.group(3)
                data.append({
                    "id": pid,  # Añadimos el ID para referencia
                    "nombre": match.group(1),
                    "elo": int(match.group(2)),
                    "ranking": int(ranking) if ranking.isdigit() else None,
                    "winrate": int(match.group(4)) if match.group(4).isdigit() else None
                })
        except:
            continue
    
    # Ordenar por ELO descendente
    return sorted(data, key=lambda x: x["elo"], reverse=True)
