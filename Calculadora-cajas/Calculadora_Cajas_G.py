import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Calculadora🤓 de Cajas 📦",
    page_icon="📦🤓",
    layout="wide"
)

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
    }
    .titulo {
        font-size:32px;
        font-weight:bold;
        color:#2C3E50;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: gray;
        font-size: 13px;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES ---
def calcular_kits_por_caja(caja_kit, caja_embalaje):
    largo_kit, ancho_kit, alto_kit = caja_kit
    largo_emb, ancho_emb, alto_emb = caja_embalaje

    if (largo_kit > largo_emb or ancho_kit > ancho_emb or alto_kit > alto_emb):
        return 0, None

    orientaciones = [
        (largo_kit, ancho_kit, alto_kit),
        (ancho_kit, largo_kit, alto_kit),
        (largo_kit, alto_kit, ancho_kit),
        (alto_kit, ancho_kit, largo_kit),
        (ancho_kit, alto_kit, largo_kit),
        (alto_kit, largo_kit, ancho_kit)
    ]

    max_kits = 0
    mejor_orientacion = None
    mejor_distribucion = None

    for l, a, h in orientaciones:
        if l <= largo_emb and a <= ancho_emb and h <= alto_emb:
            en_largo = int(largo_emb // l)
            en_ancho = int(ancho_emb // a)
            en_alto = int(alto_emb // h)
            kits_total = en_largo * en_ancho * en_alto

            if kits_total > max_kits:
                max_kits = kits_total
                mejor_orientacion = (l, a, h)
                mejor_distribucion = (en_largo, en_ancho, en_alto)

    return max_kits, (mejor_orientacion, mejor_distribucion)


def mostrar_visualizacion_3d(caja_kit, caja_embalaje, distribucion):
    """Devuelve una figura matplotlib con la distribución en 3D"""
    l_kit, a_kit, h_kit = caja_kit
    l_emb, a_emb, h_emb = caja_embalaje
    en_largo, en_ancho, en_alto = distribucion

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Caja de embalaje transparente
    embalaje = np.array([[0, 0, 0],
                       [l_emb, 0, 0],
                       [l_emb, a_emb, 0],
                       [0, a_emb, 0],
                       [0, 0, h_emb],
                       [l_emb, 0, h_emb],
                       [l_emb, a_emb, h_emb],
                       [0, a_emb, h_emb]])
    caras_embalaje = [
        [embalaje[0], embalaje[1], embalaje[2], embalaje[3]],
        [embalaje[4], embalaje[5], embalaje[6], embalaje[7]], 
        [embalaje[0], embalaje[1], embalaje[5], embalaje[4]],
        [embalaje[2], embalaje[3], embalaje[7], embalaje[6]],
        [embalaje[1], embalaje[2], embalaje[6], embalaje[5]],
        [embalaje[4], embalaje[7], embalaje[3], embalaje[0]]
    ]
    ax.add_collection3d(Poly3DCollection(caras_embalaje, facecolors='cyan', linewidths=1, 
                                       edgecolors='blue', alpha=0.1))

    colores = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']

    # Dibujar los kits
    for i in range(en_largo):
        for j in range(en_ancho):
            for k in range(en_alto):
                x = i * l_kit
                y = j * a_kit
                z = k * h_kit

                vertices = np.array([
                    [x, y, z],
                    [x + l_kit, y, z],
                    [x + l_kit, y + a_kit, z],
                    [x, y + a_kit, z],
                    [x, y, z + h_kit],
                    [x + l_kit, y, z + h_kit],
                    [x + l_kit, y + a_kit, z + h_kit],
                    [x, y + a_kit, z + h_kit]
                ])
                caras = [
                    [vertices[0], vertices[1], vertices[2], vertices[3]],
                    [vertices[4], vertices[5], vertices[6], vertices[7]], 
                    [vertices[0], vertices[1], vertices[5], vertices[4]],
                    [vertices[2], vertices[3], vertices[7], vertices[6]],
                    [vertices[1], vertices[2], vertices[6], vertices[5]],
                    [vertices[4], vertices[7], vertices[3], vertices[0]]
                ]
                color_idx = (i + j + k) % len(colores)
                ax.add_collection3d(Poly3DCollection(caras, facecolors=colores[color_idx], 
                                                   linewidths=1, edgecolors='black', alpha=0.7))

    ax.set_xlim(0, l_emb)
    ax.set_ylim(0, a_emb)
    ax.set_zlim(0, h_emb)
    ax.set_xlabel("Largo (cm)")
    ax.set_ylabel("Ancho (cm)")
    ax.set_zlabel("Alto (cm)")
    ax.set_title("Distribución de cajas en el embalaje")

    return fig


# --- INTERFAZ ---
st.markdown('<p class="titulo">📦 Calculadora de Cajas de Embalaje🤓</p>', unsafe_allow_html=True)
st.write("Una herramienta sencilla para calcular cuántas cajas necesitas para tus kits.")

col1, col2 = st.columns([1,1])

with col1:
    st.header("👉 Datos de entrada")
    largo_kit = st.number_input("Largo kit (cm)", min_value=1.0, value=10.0)
    ancho_kit = st.number_input("Ancho kit (cm)", min_value=1.0, value=10.0)
    alto_kit = st.number_input("Alto kit (cm)", min_value=1.0, value=10.0)

    largo_emb = st.number_input("Largo embalaje (cm)", min_value=1.0, value=30.0)
    ancho_emb = st.number_input("Ancho embalaje (cm)", min_value=1.0, value=30.0)
    alto_emb = st.number_input("Alto embalaje (cm)", min_value=1.0, value=30.0)

    cantidad_kits = st.number_input("¿Cuántos kits necesitas enviar?", min_value=1, value=10)

    calcular = st.button("📐 Calcular cajas", use_container_width=True)

with col2:
    st.header("📊👨🏻‍🔬 Resultados")
    if calcular:
        kits_por_caja, distribucion = calcular_kits_por_caja(
            (largo_kit, ancho_kit, alto_kit),
            (largo_emb, ancho_emb, alto_emb)
        )

        if kits_por_caja > 0:
            cajas_necesarias = -(-cantidad_kits // kits_por_caja)
            espacio_utilizado = (kits_por_caja * largo_kit * ancho_kit * alto_kit) / (largo_emb * ancho_emb * alto_emb) * 100

            st.success("✅ Cálculo exitoso")
            st.write(f"**Kits por caja de embalaje:** {kits_por_caja}")
            st.write(f"**Cajas necesarias:** {cajas_necesarias}")
            st.write(f"**Espacio utilizado:** {espacio_utilizado:.1f}%")

            orientacion, distrib = distribucion
            if orientacion and distrib:
                st.subheader("Distribución sugerida")
                st.write(f"• Orientación: {orientacion[0]} × {orientacion[1]} × {orientacion[2]} cm")
                st.write(f"• Distribución: {distrib[0]} × {distrib[1]} × {distrib[2]}")
                st.write(f"• Total: {kits_por_caja} kits/caja")

                # Visualización 3D
                fig = mostrar_visualizacion_3d(orientacion, (largo_emb, ancho_emb, alto_emb), distrib)
                st.pyplot(fig)
        else:
            st.error("❌ Las cajas del kit no caben en la caja de embalaje.")

# --- FOOTER ---
st.markdown('<div class="footer">Creado con ❤️ por Germán Millán👨🏻‍🔬</div>', unsafe_allow_html=True)





