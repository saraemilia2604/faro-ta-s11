# ============================================================================
# ARCHIVO: app.py (en la raíz de tu repositorio personal faro-ta-s11)   (TU TABLERO · P3-TA-A1)
# QUÉ HACE:  Es una versión corta del tablero del Faro. Sobre esta base haces TU reto.
# RECIBE:    Los archivos de la carpeta data/ de tu repositorio (copia de los datos del Faro).
# ENTREGA:   Una página web. Tu reto (el de tu nombre en la guía) añade algo nuevo.
# ESTO PUEDES CAMBIARLO: tu reto, pegándolo donde dicen los marcadores «>>> RETO».
# ============================================================================
import math
from pathlib import Path

import pandas as pd
import streamlit as st

TITULO = "Mi tablero · P3-TA-A1"
st.set_page_config(page_title=TITULO, page_icon="🏠", layout="wide")


def buscar_raiz():
    """Sube de carpeta hasta encontrar la que contiene data/ (la raíz del repositorio)."""
    aqui = Path(__file__).resolve().parent
    for carpeta in [aqui, *aqui.parents]:
        if (carpeta / "data" / "anuncios_limpios.csv").exists():
            return carpeta
    return aqui


RAIZ = buscar_raiz()


@st.cache_data(ttl=600)
def leer(ruta):
    ruta = Path(ruta)
    return pd.read_csv(ruta) if ruta.exists() else None


anuncios = leer(RAIZ / "data" / "anuncios_limpios.csv")
st.title(TITULO)
if anuncios is None or anuncios.empty:
    st.error("No encuentro data/anuncios_limpios.csv. Corre el robot (pestaña Actions) y recarga.")
    st.stop()

# --- FILTROS (columna izquierda) ---
st.sidebar.header("Filtros")
tipos = sorted(anuncios["tipo"].dropna().unique())
tipo_elegido = st.sidebar.multiselect("Tipo de vivienda", tipos, default=tipos)
# floor/ceil: el deslizador usa enteros; así no deja fuera el anuncio más barato ni el más caro
pmin, pmax = math.floor(anuncios["precio_m2"].min()), math.ceil(anuncios["precio_m2"].max())
rango = st.sidebar.slider("Precio por m² (USD)", pmin, pmax, (pmin, pmax))
min_anuncios = st.sidebar.slider("Mínimo de anuncios por sector", 1, 30, 5)

# >>> RETO 1 · PARTE A: si tu reto es el 1, pega aquí el filtro nuevo

filtrado = anuncios[anuncios["tipo"].isin(tipo_elegido) & anuncios["precio_m2"].between(rango[0], rango[1])]

# >>> RETO 1 · PARTE B: si tu reto es el 1, pega aquí la línea que aplica el filtro

st.sidebar.write(f"**{len(filtrado):,}** anuncios con estos filtros")

# --- TARJETAS ---
c1, c2 = st.columns(2)
c1.metric("Anuncios", f"{len(filtrado):,}")
c2.metric("Mediana USD por m²", f"{filtrado['precio_m2'].median():,.0f}" if len(filtrado) else "sin datos")

# >>> RETO 2: si tu reto es el 2, pega aquí las tarjetas nuevas

pestana1, pestana2, pestana3 = st.tabs(["📍 Sectores", "📈 Tendencia", "⭐ Mi reto"])

with pestana1:
    st.subheader("¿Qué sectores son más caros?")
    por_sector = (filtrado.groupby("sector").agg(anuncios=("id", "count"), mediana_m2=("precio_m2", "median"))
                  .round(0).reset_index())
    por_sector = por_sector[por_sector["anuncios"] >= min_anuncios].sort_values("mediana_m2", ascending=False).head(12)
    if por_sector.empty:
        st.info("Ningún sector llega al mínimo. Bájalo en la columna izquierda.")
    else:
        st.bar_chart(por_sector.set_index("sector")["mediana_m2"], color="#002A54", horizontal=True)

with pestana2:
    st.subheader("¿Sube o baja el precio por m²?")
    historico = leer(RAIZ / "data" / "historico" / "resumen_diario.csv")
    if historico is None or historico.empty:
        st.info("Todavía no hay histórico.")
    else:
        h = historico.sort_values("fecha").copy()
        h["fecha"] = pd.to_datetime(h["fecha"])
        st.line_chart(h.set_index("fecha")["mediana_m2"], color="#C8102E")

pestana3.write("Esta pestaña es para tu reto si es el 3, el 4 o el 5.")

# >>> RETO 3, 4 y 5: si tu reto es el 3, el 4 o el 5, pega aquí el bloque de tu reto (solo uno)
