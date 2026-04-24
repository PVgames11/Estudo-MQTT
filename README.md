# Estudo-MQTT
# 📡 Radar IoT: Sistema de Telemetria Full-Stack em Tempo Real

![Status](https://img.shields.io/badge/Status-Concluído-success)
![IoT](https://img.shields.io/badge/IoT-ESP32-blue)
![Backend](https://img.shields.io/badge/Backend-Python-yellow)
![Database](https://img.shields.io/badge/Database-MySQL-orange)
![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red)

## 📌 Sobre o Projeto
Este projeto é uma **Prova de Conceito (PoC)** e um Laboratório de Estudos Avançados em Internet das Coisas (IoT). O objetivo principal foi desenvolver e validar uma arquitetura ponta a ponta (Full-Stack) para sistemas de telemetria e monitoramento em tempo real.

Nesta implementação, um sensor ultrassônico atua como o dispositivo de borda (Edge Device), enviando dados de distância. A arquitetura foi desenhada para ser escalável e agnóstica em relação ao sensor, servindo como base sólida para projetos reais de monitoramento industrial (como pesagem de cilindros, controle de nível de tanques, etc.).

## 🏗️ Arquitetura do Sistema
O fluxo de dados foi projetado para garantir baixa latência e persistência confiável:

1. **Hardware (C++):** Um ESP32 realiza a leitura do sensor HC-SR04, processa a distância, embarca os dados em um payload `JSON` e os transmite via Wi-Fi.
2. **Mensageria (MQTT):** O payload é publicado em um tópico específico no broker HiveMQ, garantindo comunicação leve e assíncrona.
3. **Backend (Python):** Um script atua como *Subscriber* (ouvinte) ininterrupto. Ao receber o JSON, ele decodifica, extrai as variáveis e as insere de forma estruturada no banco de dados.
4. **Persistência (MySQL):** Um banco de dados relacional armazena todo o histórico de telemetria, garantindo integridade e facilitando consultas futuras.
5. **Frontend (Streamlit):** Um dashboard web consome os dados do MySQL e renderiza, em tempo real, os gráficos de variação e alertas visuais, recarregando automaticamente sem intervenção do usuário.

## 🚀 Tecnologias Utilizadas

* **Microcontrolador:** ESP32
* **Sensor:** Ultrassônico HC-SR04
* **Linguagens:** C++ (Arduino IDE) e Python 3
* **Protocolo de Rede:** MQTT (Broker HiveMQ e biblioteca `PubSubClient`)
* **Banco de Dados:** MySQL (via `mysql-connector-python`)
* **Visualização de Dados:** Streamlit e Pandas

## ⚙️ Como Executar o Projeto

### Pré-requisitos
* Servidor MySQL rodando localmente (ex: XAMPP).
* Python 3 instalado com ambiente virtual (`venv`).
* Arduino IDE configurada para a placa ESP32.

### 1. Configurando o Banco de Dados e Backend
Clone este repositório, ative seu ambiente virtual e instale as dependências:
```bash
pip install -r requirements.txt
