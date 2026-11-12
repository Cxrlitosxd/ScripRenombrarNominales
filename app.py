import streamlit as st
import csv
import os
import shutil
from pathlib import Path
from collections import Counter

# ==========================================
# 1. CONFIGURACION
# ==========================================

st.set_page_config(
    page_title="Nominal Manager",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. ESTILOS Y ANIMACIONES
# ==========================================

st.markdown("""
<style>

/* ==========================================
   FONDO Y CONFIGURACION GENERAL
========================================== */

.stApp {
    background: #F8FAFC !important;
    color: #334155 !important;
}

.block-container {
    max-width: 1100px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}

#MainMenu,
footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* ==========================================
   ANIMACIONES
========================================== */

@keyframes aparecer {
    from {
        opacity: 0;
        transform: translateY(18px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes entradaSuave {
    from {
        opacity: 0;
        transform: translateY(12px) scale(0.99);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes flotar {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-4px);
    }
}

@keyframes pulsoAzul {
    0%, 100% {
        box-shadow: 0 0 0 0 rgba(59, 130, 246, 0);
    }
    50% {
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.08);
    }
}

@keyframes pulsoVerde {
    0%, 100% {
        box-shadow: 0 0 0 0 rgba(34, 160, 107, 0);
    }
    50% {
        box-shadow: 0 0 0 4px rgba(34, 160, 107, 0.08);
    }
}

@keyframes brilloLinea {
    0% {
        background-position: 0% 50%;
    }
    100% {
        background-position: 200% 50%;
    }
}

/* ==========================================
   ENCABEZADO
========================================== */

.encabezado {
    background: linear-gradient(120deg, #102A56, #1554A5, #1687D9);
    background-size: 200% 200%;
    padding: 25px 30px;
    border-radius: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    animation: aparecer 0.8s ease;
    margin-bottom: 55px;
    box-shadow: 0 8px 20px rgba(18, 52, 90, 0.12);
}

.logo {
    color: #FFFFFF !important;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 1px;
    animation: flotar 4s infinite ease-in-out;
}

.logo span {
    color: #93C5FD !important;
}

.encabezado-derecha {
    color: #FFFFFF !important;
    font-size: 13px;
}

/* ==========================================
   PRESENTACION
========================================== */

.presentacion {
    animation: entradaSuave 0.8s ease;
    margin-bottom: 35px;
}

.presentacion h1 {
    color: #12345A !important;
    font-size: 39px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 12px;
}

.presentacion p {
    color: #526783 !important;
    font-size: 16px;
    line-height: 1.7;
}

/* ==========================================
   SECCION CARPETA
========================================== */

.seccion-carpeta {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 25px;
    animation: entradaSuave 0.8s ease;
    margin-bottom: 30px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.seccion-carpeta:hover {
    border-color: #CBD5E1;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
}

.seccion-titulo {
    color: #12345A !important;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 8px;
}

/* ==========================================
   CAMPO DE RUTA
========================================== */

div[data-testid="stTextInput"] input,
div[data-testid="stTextInput"] input:hover,
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextInput"] input:active {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
    caret-color: #2563EB !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 13px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    outline: none !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}

div[data-testid="stTextInput"] input:-webkit-autofill,
div[data-testid="stTextInput"] input:-webkit-autofill:hover,
div[data-testid="stTextInput"] input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0 1000px #FFFFFF inset !important;
    -webkit-text-fill-color: #172B4D !important;
    background-color: #FFFFFF !important;
    caret-color: #2563EB !important;
}

div[data-testid="stTextInput"] input:focus {
    border: 1px solid #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.10) !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
    opacity: 1 !important;
    font-weight: 400 !important;
}

div[data-testid="stTextInput"] input::selection {
    background: #DBEAFE !important;
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
}

div[data-testid="stTextInput"] label {
    color: #12345A !important;
}

/* ==========================================
   BOTONES - BASE GENERAL
========================================== */

div[data-testid="stButton"] {
    animation: entradaSuave 0.6s ease;
}

div[data-testid="stButton"] button {
    min-height: 46px !important;
    width: 100% !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    font-weight: 650 !important;
    letter-spacing: 0.1px !important;
    opacity: 1 !important;
    box-shadow: none !important;
    outline: none !important;
    transition:
        background-color 0.25s ease,
        border-color 0.25s ease,
        transform 0.25s ease,
        box-shadow 0.25s ease !important;
}

/* ==========================================
   BOTON ANALIZAR - AZUL MINIMALISTA
========================================== */

div[data-testid="stButton"] button[kind="primary"],
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
    background: #E8F1FF !important;
    background-color: #E8F1FF !important;
    background-image: none !important;
    border: 1px solid #C7DBFA !important;
    color: #174EA6 !important;
    -webkit-text-fill-color: #174EA6 !important;
    animation: pulsoAzul 4s infinite ease-in-out;
}

div[data-testid="stButton"] button[kind="primary"] *,
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] * {
    color: #174EA6 !important;
    -webkit-text-fill-color: #174EA6 !important;
    opacity: 1 !important;
    text-shadow: none !important;
}

div[data-testid="stButton"] button[kind="primary"] svg,
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] svg {
    color: #174EA6 !important;
    fill: #174EA6 !important;
}

div[data-testid="stButton"] button[kind="primary"]:hover,
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover {
    background: #DCEAFF !important;
    background-color: #DCEAFF !important;
    border: 1px solid #A9C9F5 !important;
    color: #123B78 !important;
    -webkit-text-fill-color: #123B78 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.09) !important;
}

div[data-testid="stButton"] button[kind="primary"]:hover *,
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover * {
    color: #123B78 !important;
    -webkit-text-fill-color: #123B78 !important;
}

/* ==========================================
   BOTON PROCESAR - VERDE MINIMALISTA
========================================== */

div[data-testid="stButton"] button[kind="secondary"],
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"] {
    background: #E8F7EE !important;
    background-color: #E8F7EE !important;
    background-image: none !important;
    border: 1px solid #BDE5CC !important;
    color: #176B3A !important;
    -webkit-text-fill-color: #176B3A !important;
    animation: pulsoVerde 4s infinite ease-in-out;
}

div[data-testid="stButton"] button[kind="secondary"] *,
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"] * {
    color: #176B3A !important;
    -webkit-text-fill-color: #176B3A !important;
    opacity: 1 !important;
    text-shadow: none !important;
}

div[data-testid="stButton"] button[kind="secondary"] svg,
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"] svg {
    color: #176B3A !important;
    fill: #176B3A !important;
}

div[data-testid="stButton"] button[kind="secondary"]:hover,
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover {
    background: #D8F1E2 !important;
    background-color: #D8F1E2 !important;
    border: 1px solid #A5D9B8 !important;
    color: #14532D !important;
    -webkit-text-fill-color: #14532D !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(22, 163, 74, 0.09) !important;
}

div[data-testid="stButton"] button[kind="secondary"]:hover *,
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover * {
    color: #14532D !important;
    -webkit-text-fill-color: #14532D !important;
}

div[data-testid="stButton"] button:active {
    transform: scale(0.98) !important;
    box-shadow: none !important;
}

div[data-testid="stButton"] button:focus-visible {
    outline: 3px solid #93C5FD !important;
    outline-offset: 3px !important;
}

div[data-testid="stButton"] button:disabled {
    opacity: 0.55 !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ==========================================
   SELECTORES Y CHECKBOX
========================================== */

.stSelectbox label {
    color: #12345A !important;
}

[data-baseweb="select"] {
    background: #FFFFFF !important;
    border-radius: 9px !important;
}

[data-baseweb="select"] div,
[data-baseweb="select"] span {
    color: #243B53 !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: #FFFFFF !important;
}

[data-baseweb="menu"] * {
    color: #243B53 !important;
}

.stCheckbox label,
.stCheckbox label p,
.stCheckbox label span {
    color: #243B53 !important;
}

/* ==========================================
   RESULTADOS E INFORMACION
========================================== */

.resultado-titulo {
    color: #12345A !important;
    font-size: 23px;
    font-weight: 750;
    margin-top: 35px;
    margin-bottom: 8px;
    animation: aparecer 0.7s ease;
}

.resultado-descripcion {
    color: #526783 !important;
    margin-bottom: 20px;
}

.informacion {
    background: #EFF6FF !important;
    border: 1px solid #D7E7FC;
    border-left: 4px solid #3B82F6;
    padding: 15px;
    border-radius: 9px;
    color: #315477 !important;
    font-size: 14px;
    margin: 20px 0;
    animation: entradaSuave 0.7s ease;
}

/* ==========================================
   ALERTAS PERSONALIZADAS (CLARITAS)
========================================== */

.alerta {
    padding: 16px 20px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 500;
    margin: 10px 0 20px 0;
    animation: entradaSuave 0.5s ease;
    display: flex;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}

.alerta-exito {
    background: #ECFDF3 !important;
    border: 1px solid #BBE7CA !important;
    border-left: 5px solid #22A06B !important;
    color: #166534 !important;
}

.alerta-info {
    background: #EFF6FF !important;
    border: 1px solid #C7DBFA !important;
    border-left: 5px solid #3B82F6 !important;
    color: #1E40AF !important;
}

.alerta-advertencia {
    background: #FFFBEB !important;
    border: 1px solid #FEF3C7 !important;
    border-left: 5px solid #F59E0B !important;
    color: #92400E !important;
}

.alerta-error {
    background: #FEF2F2 !important;
    border: 1px solid #FEE2E2 !important;
    border-left: 5px solid #EF4444 !important;
    color: #991B1B !important;
}

/* ==========================================
   TABLAS Y EXPANDER
========================================== */

div[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    overflow: hidden;
    animation: entradaSuave 0.7s ease;
}

[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    transition: border-color 0.25s ease;
}

[data-testid="stExpander"]:hover {
    border-color: #CBD5E1 !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary p {
    color: #12345A !important;
}

/* ==========================================
   BARRA DE PROGRESO
========================================== */

div[data-testid="stProgressBar"] > div {
    background: #E2E8F0 !important;
    border-radius: 20px !important;
    overflow: hidden;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #2563EB, #60A5FA, #2563EB) !important;
    background-size: 200% 100% !important;
    animation: brilloLinea 2s linear infinite;
    border-radius: 20px !important;
}

/* ==========================================
   PIE DE PAGINA Y TEXTOS
========================================== */

.pie {
    text-align: center;
    color: #94A3B8 !important;
    font-size: 12px;
    border-top: 1px solid #E2E8F0;
    padding-top: 20px;
    margin-top: 60px;
}

.stApp p,
.stApp label,
.stApp li {
    color: #243B53;
}

@media (max-width: 768px) {
    .presentacion h1 { font-size: 29px; }
    .encabezado {
        padding: 18px;
        flex-direction: column;
        gap: 10px;
        text-align: center;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. ENCABEZADO WEB
# ==========================================

st.markdown("""
<div class="encabezado">
    <div class="logo">
        NOMINAL<span>MANAGER</span>
    </div>
    <div class="encabezado-derecha">
        Sistema de organización CSV
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. PRESENTACION
# ==========================================

st.markdown("""
<div class="presentacion">
    <h1>Organiza tus archivos<br>de manera inteligente.</h1>
    <p>
        Analiza, identifica y renombra tus archivos nominales
        automáticamente mediante sus columnas Anio y Mes.
        Simple, rápido y seguro.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 5. MESES
# ==========================================

MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}


# ==========================================
# 6. ALERTAS PERSONALIZADAS CLARITAS
# ==========================================

def mostrar_exito(mensaje):
    st.markdown(f'<div class="alerta alerta-exito">✅ &nbsp; {mensaje}</div>', unsafe_allow_html=True)

def mostrar_error(mensaje):
    st.markdown(f'<div class="alerta alerta-error">⚠️ &nbsp; {mensaje}</div>', unsafe_allow_html=True)

def mostrar_advertencia(mensaje):
    st.markdown(f'<div class="alerta alerta-advertencia">🔔 &nbsp; {mensaje}</div>', unsafe_allow_html=True)

def mostrar_info(mensaje):
    st.markdown(f'<div class="alerta alerta-info">ℹ️ &nbsp; {mensaje}</div>', unsafe_allow_html=True)


# ==========================================
# 7. FUNCION DE ANALISIS
# ==========================================

def analizar_csv(ruta, modo):
    periodos = set()
    try:
        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.reader(archivo)
            encabezados = next(lector, None)
            if not encabezados:
                return None, "Archivo vacío"

            encabezados = [columna.strip() for columna in encabezados]

            if "Anio" not in encabezados or "Mes" not in encabezados:
                return None, "No contiene Anio y Mes"

            pos_anio = encabezados.index("Anio")
            pos_mes = encabezados.index("Mes")

            for fila in lector:
                if len(fila) <= max(pos_anio, pos_mes):
                    continue

                anio = fila[pos_anio].strip()
                mes = fila[pos_mes].strip()

                if not anio or not mes:
                    continue

                try:
                    anio = int(anio)
                    mes = int(mes)
                except ValueError:
                    return None, "Anio o Mes inválido"

                if anio < 1 or mes not in MESES:
                    return None, "Anio o Mes fuera de rango"

                periodos.add((anio, mes))

                if modo == "Rápido":
                    break

                if len(periodos) > 1:
                    return None, "Contiene varios meses o años"

        if not periodos:
            return None, "No se encontraron registros"

        return next(iter(periodos)), None

    except Exception as error:
        return None, str(error)


# ==========================================
# 8. BUSCAR ARCHIVOS
# ==========================================

def buscar_archivos(carpeta, modo):
    resultados = []
    errores = []
    carpeta = Path(carpeta).resolve()
    carpeta_salida = carpeta.parent / "Nominales_Renombrados"
    archivos_csv = []

    for raiz, subcarpetas, archivos in os.walk(carpeta):
        subcarpetas[:] = [
            nombre for nombre in subcarpetas
            if (Path(raiz) / nombre).resolve() != carpeta_salida.resolve()
        ]
        for nombre in archivos:
            if nombre.lower().endswith(".csv"):
                origen = Path(raiz) / nombre
                if carpeta_salida.resolve() in origen.resolve().parents:
                    continue
                archivos_csv.append(origen)

    total = len(archivos_csv)
    if total == 0:
        return resultados, errores

    barra = st.progress(0)
    estado = st.empty()

    for numero, origen in enumerate(archivos_csv, start=1):
        estado.caption(f"Procesando {numero} de {total}: {origen.name}")
        periodo, error = analizar_csv(origen, modo)

        if error:
            errores.append({"Archivo": origen.name, "Motivo": error})
        else:
            anio, numero_mes = periodo
            resultados.append({
                "Archivo original": origen.name,
                "Mes": MESES[numero_mes],
                "Año": anio,
                "Nuevo nombre": f"NominalTrama{MESES[numero_mes]}.csv",
                "Origen": str(origen),
                "Tamaño": round(origen.stat().st_size / (1024 * 1024), 2)
            })
        barra.progress(numero / total)

    estado.markdown('<div class="alerta alerta-exito">✅ &nbsp; Análisis completado correctamente.</div>', unsafe_allow_html=True)
    return resultados, errores


# ==========================================
# 9. SELECCION DE CARPETA
# ==========================================

st.markdown("""
<div class="seccion-carpeta">
    <div class="seccion-titulo">01. Selecciona tu carpeta</div>
    <p style="color:#64748B;font-size:14px;">
        Introduce la ubicación donde se encuentran tus archivos CSV.
    </p>
</div>
""", unsafe_allow_html=True)

carpeta = st.text_input(
    "Ruta de la carpeta principal",
    placeholder=r"C:\Users\Lenovo\Downloads\nominalesxd",
    label_visibility="collapsed"
)

col1, col2 = st.columns([1, 2])

with col1:
    modo = st.selectbox("Tipo de análisis", ["Seguro", "Rápido"])

with col2:
    st.markdown("""
    <div style="color:#526783; font-size:13px; padding-top:30px;">
        El modo seguro comprueba todos los registros.
        El modo rápido revisa solamente el primer registro válido.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 10. BOTON ANALIZAR
# ==========================================

if st.button("🔍  Analizar archivos", type="primary", width="stretch"):
    if not carpeta.strip():
        mostrar_error("Introduce primero la ruta de la carpeta.")
    elif not os.path.isdir(carpeta.strip()):
        mostrar_error("La carpeta indicada no existe.")
    else:
        with st.spinner("Preparando tus archivos..."):
            resultados, errores = buscar_archivos(carpeta.strip(), modo)

        st.session_state["resultados"] = resultados
        st.session_state["errores"] = errores
        st.session_state["carpeta"] = carpeta.strip()
        st.session_state["modo"] = modo

        mostrar_exito("¡La revisión de archivos ha terminado!")


# ==========================================
# 11. VISTA PREVIA
# ==========================================

if "resultados" in st.session_state:
    resultados = st.session_state["resultados"]
    errores = st.session_state["errores"]

    st.markdown("""
    <div class="resultado-titulo">
        02. Vista previa de archivos
    </div>
    <div class="resultado-descripcion">
        Revisa los nombres nuevos antes de realizar cualquier movimiento.
    </div>
    """, unsafe_allow_html=True)

    duplicados = Counter(r["Nuevo nombre"] for r in resultados)
    cantidad_duplicados = sum(1 for cantidad in duplicados.values() if cantidad > 1)

    st.write(
        f"**{len(resultados)}** archivos identificados · "
        f"**{len(errores)}** con errores · "
        f"**{cantidad_duplicados}** nombres duplicados"
    )

    if resultados:
        datos = []
        for r in resultados:
            datos.append({
                "Archivo original": r["Archivo original"],
                "Mes": r["Mes"],
                "Año": r["Año"],
                "Nuevo nombre": r["Nuevo nombre"],
                "Tamaño MB": r["Tamaño"]
            })
        st.dataframe(datos, width="stretch", hide_index=True)
    else:
        mostrar_advertencia("No se encontraron archivos válidos.")


    # ======================================
    # 12. ERRORES
    # ======================================
    if errores:
        with st.expander("Ver archivos que necesitan revisión"):
            st.dataframe(errores, width="stretch", hide_index=True)


    # ======================================
    # 13. PROCESAR ARCHIVOS
    # ======================================
    st.markdown("""
    <div class="resultado-titulo">
        03. Organizar archivos
    </div>
    <div class="informacion">
        Los archivos originales serán trasladados a una carpeta
        llamada Nominales_Renombrados, fuera de la carpeta principal.
        Su contenido no será modificado.
    </div>
    """, unsafe_allow_html=True)

    if st.session_state["modo"] == "Rápido":
        mostrar_advertencia(
            "El modo rápido no verifica todos los registros. "
            "Para proteger los datos, recomendamos repetir el análisis en modo seguro antes de moverlos."
        )

    confirmar = st.checkbox("He revisado los resultados y autorizo mover los archivos.")

    if st.button("📦  Procesar y organizar archivos", type="secondary", width="stretch"):
        if not confirmar:
            mostrar_error("Debes confirmar antes de continuar.")
        elif not resultados:
            mostrar_error("No hay archivos para procesar.")
        elif st.session_state["modo"] != "Seguro":
            mostrar_error("Para mover archivos debes realizar primero un análisis en modo seguro.")
        else:
            destino = Path(st.session_state["carpeta"]).resolve().parent / "Nominales_Renombrados"
            destino.mkdir(exist_ok=True)

            movidos = 0
            omitidos = 0
            fallidos = 0
            conteo = Counter(r["Nuevo nombre"] for r in resultados)
            total = len(resultados)
            barra = st.progress(0)

            for i, r in enumerate(resultados, start=1):
                origen = Path(r["Origen"])
                ruta_destino = destino / r["Nuevo nombre"]

                if conteo[r["Nuevo nombre"]] > 1:
                    omitidos += 1
                    barra.progress(i / total)
                    continue

                if not origen.exists() or ruta_destino.exists():
                    omitidos += 1
                    barra.progress(i / total)
                    continue

                try:
                    shutil.move(str(origen), str(ruta_destino))
                    movidos += 1
                except Exception:
                    fallidos += 1

                barra.progress(i / total)

            mostrar_exito("¡Organización finalizada!")
            st.write(f"Archivos movidos: **{movidos}**")
            st.write(f"Archivos omitidos: **{omitidos}**")
            st.write(f"Archivos fallidos: **{fallidos}**")

            st.write("Ubicación de los resultados:")
            st.code(str(destino))

            del st.session_state["resultados"]
            del st.session_state["errores"]

            mostrar_info("Vuelve a analizar la carpeta para actualizar la vista previa.")



st.markdown("""
<div class="pie">
    NOMINAL MANAGER · Organización inteligente de archivos CSV
    <br><br>
    Procesamiento local · Protección de información
</div>
""", unsafe_allow_html=True)