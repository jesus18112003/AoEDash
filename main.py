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
# Busca: **Nombre** (ELO) Rank #Ranking, ... Winrate%
pattern = r"\*\*(.*?)\*\* \((\d+)\)\sRank\s#(\d+),.*?(\d+)%"

def fetch_player_stats(pid):
    """
    Función síncrona para obtener y procesar los datos de un solo jugador.
    Utiliza requests y se ejecuta concurrentemente usando asyncio.to_thread.
    """
    url = f"https://data.aoe2companion.com/api/nightbot/rank?profile_id={pid}"
    
    # DEBUG: Imprimir la URL para verificar la construcción
    print(f"-> Solicitando URL: {url}")
    
    try:
        response = requests.get(url, timeout=10) 
        
        # Lanza una excepción si el estado HTTP es 4xx o 5xx
        response.raise_for_status() 
        
        # Pre-procesamiento: reemplaza non-breaking spaces y quita comillas externas
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
        
        # Si la solicitud fue exitosa pero no hubo coincidencia (ej. jugador sin ranking)
        print(f"ID {pid}: Solicitud OK, pero no se pudo extraer la información con el patrón.")
        print(f"Respuesta recibida: {texto}")
        
    except requests.exceptions.HTTPError as http_err:
        # Esto captura específicamente errores 400 (Bad Request), 404, 500, etc.
        # Si recibes el error "Missing search..." es un HTTP 400.
        print(f"ERROR HTTP para ID {pid} ({url}): {http_err} - Respuesta: {response.text.strip()}")
        
    except requests.exceptions.RequestException as req_err:
        # Captura errores de conexión, timeout, DNS, etc.
        print(f"ERROR de CONEXIÓN para ID {pid} ({url}): {req_err}")
        
    except Exception as e:
        # Captura cualquier otro error, como un fallo de conversión int()
        print(f"ERROR de PROCESAMIENTO para ID {pid}: {e}")
        
    return None # Retorna None si hubo algún error o no se pudo extraer el dato


@app.get("/estadisticas")
async def obtener_estadisticas():
    # Creamos una lista de tareas asíncronas
    # asyncio.to_thread permite ejecutar funciones síncronas (requests.get) de forma concurrente
    tasks = [asyncio.to_thread(fetch_player_stats, pid) for pid in profile_ids]
    
    # Ejecutamos todas las tareas y esperamos a que terminen
    results = await asyncio.gather(*tasks)
    
    # Filtramos los resultados nulos (los que fallaron o no tuvieron match)
    valid_data = [d for d in results if d is not None]
    
    # Ordenar por ELO descendente
    return sorted(valid_data, key=lambda x: x["elo"], reverse=True)