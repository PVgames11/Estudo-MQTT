import streamlit as st
import mysql.connector
import pandas as pd
import time # <-- Importamos a biblioteca de tempo

st.set_page_config(page_title="Monitor Ultrassônico", layout="centered")
st.title("📡 Radar IoT - Tempo Real")
st.write("Monitoramento automático de distância usando MySQL.")

def carregar_dados():
    conn = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="", 
        database="mqtt_data"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, distancia_cm, alerta FROM historico_distancia ORDER BY timestamp DESC LIMIT 50")
    linhas = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(linhas, columns=colunas)
    conn.close()
    return df.iloc[::-1]

# Criamos um "container" vazio para injetar os dados. 
# Isso evita que a tela pisque quando a página recarregar sozinha.
placeholder = st.empty()

# Tudo o que é visual agora entra dentro desse container
with placeholder.container():
    try:
        df = carregar_dados()
        
        if not df.empty:
            ultima_distancia = df.iloc[-1]['distancia_cm']
            ultimo_alerta = df.iloc[-1]['alerta']

            col1, col2 = st.columns(2)
            col1.metric(label="Distância Atual", value=f"{ultima_distancia} cm")
            
            if "obstáculo" in ultimo_alerta.lower():
                col2.error(f"🚨 {ultimo_alerta.upper()}")
            else:
                col2.success(f"✅ {ultimo_alerta.upper()}")

            st.divider()

            st.subheader("📈 Histórico de Movimento")
            st.line_chart(df.set_index('timestamp')['distancia_cm'])

            with st.expander("Ver dados brutos do MySQL"):
                st.dataframe(df)
        else:
            st.info("Banco de dados MySQL conectado! Aguardando o ESP32...")
            
    except Exception as e:
        st.error(f"Erro ao conectar no banco: {e}")

# --- A MÁGICA DO TEMPO REAL ---
# O script pausa por 1 segundo e depois manda a página se recarregar sozinha
time.sleep(1)
st.rerun()