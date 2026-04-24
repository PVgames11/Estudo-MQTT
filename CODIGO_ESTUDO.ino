#include <WiFi.h>
#include <PubSubClient.h>

// 1. Configurações da sua Rede Wi-Fi (COLOQUE SEUS DADOS AQUI)
const char* ssid = "WIFI";
const char* password = "SENHA";

// 2. Configurações do MQTT (Exatamente iguais ao Python)
const char* mqtt_server = "broker.hivemq.com";
const char* topico = "estudo/sensores/ultrassonico";

// 3. Pinos do Sensor HC-SR04
const int trigPin = 5;
const int echoPin = 18;

// Criando os "motores" de rede
WiFiClient espClient;
PubSubClient client(espClient);

// Função para conectar no Wi-Fi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando na rede: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Wi-Fi Conectado!");
}

// Função para reconectar ao MQTT se cair
void reconectar() {
  while (!client.connected()) {
    Serial.print("Tentando conectar ao Broker MQTT...");
    // Cria um ID aleatório para o ESP32 não dar conflito
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("✅ Conectado ao broker!");
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando de novo em 5 segundos...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  // Configura os pinos do sensor
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Inicia o Wi-Fi e configura o MQTT
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  // Garante que o MQTT está conectado e rodando
  if (!client.connected()) {
    reconectar();
  }
  client.loop();

  // --- LÓGICA DO SENSOR ULTRASSÔNICO ---
  // Limpa o pino do Trigger
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Manda o pulso sonoro por 10 microsegundos
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Lê o tempo que o som demorou para voltar (Echo)
  long duracao = pulseIn(echoPin, HIGH);
  
  // Calcula a distância em cm (velocidade do som é ~0.034 cm/us)
  float distancia_cm = duracao * 0.034 / 2;

  // Lógica de alerta (menor que 10cm)
  String alerta = "livre";
  if (distancia_cm < 10.0) {
    alerta = "obstáculo muito perto!";
  }

  // --- MONTANDO E ENVIANDO O JSON ---
  // Criamos a string no formato JSON "na mão" para o Python entender
  String payload = "{\"sensor_id\":\"HC-SR04-Físico\",\"distancia_cm\":" + String(distancia_cm) + ",\"alerta\":\"" + alerta + "\"}";

  Serial.print("Enviando dados: ");
  Serial.println(payload);

  // Manda para a nuvem!
  client.publish(topico, payload.c_str());

  // Espera 2 segundos antes de ler e mandar de novo
  delay(2000);
}