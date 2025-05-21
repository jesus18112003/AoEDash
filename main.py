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
profile_ids = [21613744,74521,6774025,21625064,21640454,21601763]

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
