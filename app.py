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
d1, d2 = st.columns(2)
if len(filtrado):
    d1.metric("Precio máximo por m²", f"{filtrado['precio_m2'].max():,.0f}")
    d2.metric("Sector con más anuncios", str(filtrado["sector"].value_counts().idxmax()))

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
RETO 2 · Tarjetas nuevas
======================================================================
ESTE ES EL ARCHIVO DE:
  - Henry Gabriel Cupacan Benavides
  - Paula Andrea Paredes Maldonado
  - Sara Emilia Sanchez Sotomayor
(Si tu nombre no aparece aquí, abre el archivo con el número que sale junto a tu nombre en LEEME.txt o en la guía. Cada persona usa SOLO su archivo.)

CONCEPTO: Una tarjeta (KPI) es un número resumen calculado sobre lo filtrado
======================================================================

PASO 1 · COPIA el código de tu reto
Con el mouse selecciona SOLO las líneas de código que están entre las líneas «COPIA DESDE AQUÍ» y «HASTA AQUÍ» (sin incluir esas dos líneas) y copia con Ctrl+C.

vvvvvvvvvv COPIA DESDE AQUÍ (empieza en la línea de abajo) vvvvvvvvvv
d1, d2 = st.columns(2)
if len(filtrado):
    d1.metric("Precio máximo por m²", f"{filtrado['precio_m2'].max():,.0f}")
    d2.metric("Sector con más anuncios", str(filtrado["sector"].value_counts().idxmax()))
^^^^^^^^^^ HASTA AQUÍ (termina en la línea de arriba) ^^^^^^^^^^

PASO 2 · PEGA en app.py, DEBAJO del marcador
El marcador es una línea de app.py que empieza con «# >>> RETO». Es solo un cartel que dice dónde pegar; Python la ignora.
Tu marcador: «# >>> RETO 2»  (línea 64)
Cómo llegar: En el editor de GitHub pulsa Ctrl+F y escribe: RETO 2
Cómo pegar: haz clic sobre la línea del marcador, pulsa la tecla Fin (End), pulsa Enter y pega con Ctrl+V. No borres el marcador.
El código pegado debe quedar pegado al borde izquierdo (sin espacios antes del primer renglón). Los renglones que ya traen sangría se pegan tal cual.

ASÍ DEBE QUEDAR (las flechas <== son explicaciones, NO las copies):

  61  c1.metric("Anuncios", f"{len(filtrado):,}")
  62  c2.metric("Mediana USD por m²", f"{filtrado['precio_m2'].median():,.0f}" if len(filtrado) else "sin datos")
  63  
  64  # >>> RETO 2: si tu reto es el 2, pega aquí las tarjetas nuevas      <== el marcador (NO lo borres)
  65  d1, d2 = st.columns(2)      <== LO QUE PEGAS (líneas 65 a 68)
  66  if len(filtrado):
  67      d1.metric("Precio máximo por m²", f"{filtrado['precio_m2'].max():,.0f}")
  68      d2.metric("Sector con más anuncios", str(filtrado["sector"].value_counts().idxmax()))
  69  
  70  pestana1, pestana2, pestana3 = st.tabs(["📍 Sectores", "📈 Tendencia", "⭐ Mi reto"])

(Los números de la izquierda son los números de línea que verás en el editor de GitHub. Las líneas sin flecha ya estaban en app.py.)

PASO 3 · GUARDA en GitHub
Botón verde «Commit changes…», mensaje: S11: reto 2  y botón «Commit changes».

----------------------------------------------------------------------
QUÉ ANOTAS (para tu informe): Anota los dos valores con los filtros como están y luego con «departamento» quitado del filtro de tipo.

PREGUNTA DE TU INFORME: ¿Por qué el precio máximo cambia mucho más que la mediana al mover los filtros? ¿Cuál de los dos números te serviría más para decidir y por qué?
