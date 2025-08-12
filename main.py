import streamlit as st
import subprocess
import json
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt




# Titulo
st.title("Movimento Oblíquo com Python")

# Inicializa o estado da interface (só uma vez)
if "mostrar_video" not in st.session_state:
    st.session_state.mostrar_video = False

if "mostrar_grafico" not in st.session_state:
    st.session_state.mostrar_grafico = False

# Inputs do usuário
velocidade_inicial = st.number_input("Velocidade Inicial:", min_value=0, max_value=90)
angulo = st.number_input("Ângulo de Lançamento:", min_value=0, max_value=90)

# Botões em colunas
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    if st.button("Mostrar gráfico"):
        st.session_state.mostrar_grafico = True

with col2:
    if st.button("Mostrar vídeo"):
        st.session_state.mostrar_video = True

#----- area do video -----
if st.session_state.mostrar_video:
    

    # Caminhos
    output_path = Path("media/videos/obliquo/480p15")
    output_path.mkdir(parents=True, exist_ok=True)

    # 1. Salva os parâmetros em JSON
    parametros = {
        "velocidade_inicial": velocidade_inicial,
        "angulo": angulo
    }
    with open("parametros.json", "w") as f:
        json.dump(parametros, f)

    # 2. Chama o Manim com subprocess
    comando = [
        "manim",
        "-ql",  # ou -pqh
        "obliquo.py",
        "MovimentoObliquo"
    ]

    with st.spinner("Gerando vídeo..."):
        resultado = subprocess.run(comando, capture_output=True, text=True)

    # 3. Verifica o vídeo
    if resultado.returncode == 0:
        video_path = output_path / "MovimentoObliquo.mp4"
        if video_path.exists():
            with open(video_path, "rb") as f:
                st.video(f.read())
        else:
            st.error("Vídeo não encontrado.")
    else:
        st.error("Erro ao gerar o vídeo.")
        st.text(resultado.stderr)


#----- area do grafico -----# Botão para gerar gráfico com NumPy
if st.session_state.mostrar_grafico:

    v0 = float(velocidade_inicial)
    ang = float(angulo)
    theta = ang * np.pi / 180  # converte para radianos
    g = 9.8

    traj = lambda t: [
        v0 * np.cos(theta) * t,
        v0 * np.sin(theta) * t - 0.5 * g * t**2
    ]

    t_total = 2 * v0 * np.sin(theta) / g
    t_vals = np.linspace(0, t_total, 300)
    x_vals = [traj(t)[0] for t in t_vals]
    y_vals = [traj(t)[1] for t in t_vals]

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="Trajetória", color="blue")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("Gráfico da Trajetória")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)
