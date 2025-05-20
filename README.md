# Teamboard AOE2 – Estadísticas en Tiempo Real

Este proyecto muestra un dashboard interactivo con estadísticas en tiempo real de jugadores de **Age of Empires II**, utilizando la API pública de [AoE2 Companion](https://aoe2companion.com/).

Se enfoca principalmente en visualizar datos clave como:

- 🧠 ELO (puntuación de habilidad)
- 🏆 Ranking global
- 📈 Winrate (porcentaje de victorias)
- 📊 Gráficas interactivas del Top 5 por ELO y Winrate

---

## 🚀 ¿Cómo funciona?

El sistema carga automáticamente un conjunto de `profile_id` predefinidos de jugadores del clan **Jaguares México**, y consulta su información en tiempo real a través de un backend alojado en Render.

La información se visualiza en:

- Una tabla ordenada por ELO
- Dos gráficas interactivas (Top 5 ELO y Top 5 Winrate)
- Opción para exportar los datos en CSV

---

## 💻 Archivos incluidos

- `aoe2_dashboard.html`: frontend que carga los datos y genera visualización
- `main.py`: (en el backend asociado) consulta la API de AoE2 Companion usando IDs fijos
- `requirements.txt`: dependencias mínimas para ejecutar el backend

---

## 📦 Implementación recomendada

1. Despliega el backend (FastAPI) en [Render.com](https://render.com)
2. Sube el archivo `aoe2_dashboard.html` a tu servidor, GitHub Pages, Netlify o dominio propio
3. Asegúrate que el `API_URL` en el HTML apunte a tu backend (Render u otro)
4. Comparte el dashboard con tu comunidad

---

## 👨‍💻 Autor

Proyecto desarrollado por **Jaziel Carballo**  
Última actualización: **Mayo 2025**

---
