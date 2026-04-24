import mysql.connector
import paho.mqtt.client as mqtt
import json

# ---------------------------------------------------------
# Configurações do seu MySQL (Mude se o seu tiver senha!)
# ---------------------------------------------------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "" # Se você usa XAMPP, a senha padrão é vazia
DB_NAME = "mqtt_data"

def setup_db():
    # Conecta no servidor MySQL (ainda sem selecionar o banco)
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
    cursor = conn.cursor()
    
    # Cria o banco de dados se ele não existir
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    
    # Agora sim, dizemos para o Python usar esse banco
    conn.database = DB_NAME
    
    # A sintaxe do MySQL para criar tabela muda um pouquinho
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_distancia (
            id INT AUTO_INCREMENT PRIMARY KEY,
            topic VARCHAR(255) NOT NULL,
            sensor_id VARCHAR(100),
            distancia_cm FLOAT,
            alerta VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Conectado! Servidor MySQL ATIVO.")
        tópico = "estudo/sensores/ultrassonico"
        client.subscribe(tópico)
        print(f"📡 Escutando: {tópico}")

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode('utf-8')
    
    try:
        dados = json.loads(payload_str)
        sensor = dados.get("sensor_id", "Desconhecido")
        distancia = float(dados.get("distancia_cm", 0.0))
        alerta = dados.get("alerta", "ok")
        
        print(f"📏 Distância: {distancia}cm | Status: {alerta}")
        
        cursor = db_conn.cursor()
        # No MySQL, usamos %s no lugar do ?
        cursor.execute(
            "INSERT INTO historico_distancia (topic, sensor_id, distancia_cm, alerta) VALUES (%s, %s, %s, %s)",
            (msg.topic, sensor, distancia, alerta)
        )
        db_conn.commit()
        print("💾 Salvo no banco de dados MySQL!")
        
    except Exception as e:
        print(f"⚠️ Erro ao processar: {e}")

if __name__ == "__main__":
    print("Iniciando conexão com MySQL...")
    db_conn = setup_db()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) 
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n🛑 Encerrando...")
        db_conn.close()
        client.disconnect()