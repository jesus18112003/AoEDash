from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import re
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define tu URL de proyecto para cumplir con el requisito de la API.
# Utiliza la URL de tu repositorio de GitHub.
PROJECT_URL = "https://github.com/jesus18112003/AoEDash" 

HEADERS = {
    "User-Agent": PROJECT_URL
}

# Lista fija de IDs de jugadores
profile_ids = [21613744, 74521, 6774025, 21625064, 21640454, 21601763, 10383990, 21757962, 20604423, 22257462, 11930566, 17445170, 24156097, 5248290, 21619519, 12217397, 3908390]

# Patrón de expresión regular para **Nombre** (ELO) Rank #Ranking, ... Winrate%
pattern = r"(.+?)\s\((\d+)\)\sRank\s#(\d+).*?(\d+)%\swinrate"

def fetch_player_stats(pid):
    """
    Obtiene y procesa datos de un solo jugador, incluyendo el header User-Agent.
    """
    url = f"https://data.aoe2companion.com/api/nightbot/rank?profile_id={pid}"
    
    try:
        # 🔑 Usamos el parámetro 'headers' para pasar el User-Agent
        response = requests.get(url, headers=HEADERS, timeout=10) 
        response.raise_for_status() 
        
        texto = response.text.strip().replace("\xa0", " ").strip('"')
        match = re.search(pattern, texto)
        
        if match:
            nombre = match.group(1).strip()
            return {
                "id": pid,
                "nombre": nombre,
                "elo": int(match.group(2)),
                "ranking": int(match.group(3)),
                "winrate": int(match.group(4))
            }
        
        print(f"ID {pid}: Solicitud OK, pero no se pudo extraer la información.")
        print(f"Respuesta recibida: {texto}")
        
    except requests.exceptions.HTTPError as http_err:
        print(f"ERROR HTTP para ID {pid}: {http_err} - Respuesta: {response.text.strip()}")
        
    except requests.exceptions.RequestException as req_err:
        print(f"ERROR de CONEXIÓN para ID {pid}: {req_err}")
        
    except Exception as e:
        print(f"ERROR de PROCESAMIENTO para ID {pid}: {e}")
        
    return None


@app.get("/estadisticas")
async def obtener_estadisticas():
    # Ejecución concurrente usando asyncio.to_thread
    tasks = [asyncio.to_thread(fetch_player_stats, pid) for pid in profile_ids]
    results = await asyncio.gather(*tasks)
    valid_data = [d for d in results if d is not None]
    
    # Ordenar por ELO descendente
    return sorted(valid_data, key=lambda x: x["elo"], reverse=True)