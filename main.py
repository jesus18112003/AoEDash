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

# Lista fija de IDs de jugadores
profile_ids = [21613744, 74521, 6774025, 21625064, 21640454, 21601763, 10383990, 21757962, 20604423, 22257462, 16244914, 17445170]

# Patrón de expresión regular definitivo basado en la documentación de la API
# 1: Nombre, 2: ELO, 3: Ranking, 4: Winrate
pattern = r"\*\*(.*?)\*\* \((\d+)\)\sRank\s#(\d+),.*?(\d+)%"

def fetch_player_stats(pid):
    """Función síncrona para obtener y procesar los datos de un solo jugador."""
    url = f"https://data.aoe2companion.com/api/nightbot/rank?profile_id={pid}"
    
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status()
        
        # El texto de la respuesta se limpia de non-breaking spaces y comillas.
        texto = response.text.strip().replace("\xa0", " ").strip('"')
        
        match = re.search(pattern, texto)
        
        if match:
            # Extracción de datos usando los grupos del patrón
            nombre = match.group(1).strip()
            elo = int(match.group(2))
            ranking = int(match.group(3))
            winrate = int(match.group(4))
            
            return {
                "id": pid,
                "nombre": nombre,
                "elo": elo,
                "ranking": ranking,
                "winrate": winrate
            }
        
        # Si no hay coincidencia, puede ser porque el jugador no tiene partidas
        print(f"ID {pid}: No se pudo extraer la información con el patrón. Respuesta: {texto}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP para ID {pid}: {e}")
    except Exception as e:
        print(f"Error de procesamiento general para ID {pid}: {e}")
        
    return None


@app.get("/estadisticas")
async def obtener_estadisticas():
    # Se utiliza asyncio.to_thread para ejecutar las solicitudes HTTP síncronas de forma concurrente
    tasks = [asyncio.to_thread(fetch_player_stats, pid) for pid in profile_ids]
    
    # Espera a que todas las solicitudes terminen
    results = await asyncio.gather(*tasks)
    
    # Filtra los resultados nulos (jugadores con error o sin coincidencia)
    valid_data = [d for d in results if d is not None]
    
    # Ordenar por ELO descendente (descendente)
    return sorted(valid_data, key=lambda x: x["elo"], reverse=True)

# Nota: Para ejecutar esta aplicación, necesitas un servidor ASGI como Uvicorn:
# uvicorn main:app --reload