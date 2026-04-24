# 🚀 AURIZA - Guía Completa de Configuración

**Adaptive Unified Responsive Intelligent Zenith Assistant**

## 📋 Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Instalación Rápida](#instalación-rápida)
3. [Arquitectura](#arquitectura)
4. [Características](#características)
5. [API Endpoints](#api-endpoints)
6. [Configuración](#configuración)
7. [Personalidad IA](#personalidad-ia)
8. [Sistema de Decisiones](#sistema-de-decisiones)
9. [Memoria](#memoria)
10. [Voz](#voz)
11. [Android Integration](#android-integration)
12. [Deployment](#deployment)

---

## 📋 Requisitos

### Backend
- Python 3.10+
- FastAPI 0.104+
- SQLAlchemy (DB)
- Redis (opcional, pero recomendado)
- FFmpeg (para procesamiento de audio)

### Android
- Android SDK 29+
- Kotlin 1.9+
- Android Studio
- Gradle 8.0+

### Herramientas
- Docker & Docker Compose (para deployment)
- Git
- cURL o Postman (para testing)

---

## ⚡ Instalación Rápida

### Backend (5 minutos)

```bash
# 1. Clonar/descargar proyecto
cd auriza-backend

# 2. Crear virtual environment
python -m venv venv

# Activar (Windows)
.\\venv\\Scripts\\activate
# Activar (macOS/Linux)
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar .env con tus valores

# 5. Ejecutar servidor
python -m uvicorn app.main:app --reload

# 🎉 ¡Listo! Servidor en http://localhost:8000
```

**Testing rápido:**
```bash
# Health check
curl http://localhost:8000/health

# Obtener info de AURIZA
curl http://localhost:8000/info

# Enviar mensaje
curl -X POST http://localhost:8000/api/chat/send \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"user_id\": \"user_123\",
    \"message\": \"Hola AURIZA\",
    \"context\": {}
  }'
```

### Docker (3 minutos)

```bash
# Con docker-compose (más fácil)
docker-compose up

# O manualmente
docker build -t auriza:latest .
docker run -p 8000:8000 auriza:latest
```

---

## 🏗️ Arquitectura

### Backend Structure

```
auriza-backend/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── core/
│   │   ├── personality.py      # AURIZA personality
│   │   └── config.py           # Configuration
│   ├── services/
│   │   ├── ai_service.py       # LLM integration
│   │   ├── memory_service.py   # Memory system
│   │   ├── voice_service.py    # STT/TTS
│   │   └── decision_service.py # Autonomous decisions
│   ├── routes/
│   │   ├── chat.py             # Chat endpoints
│   │   ├── voice.py            # Voice endpoints
│   │   └── decisions.py        # Decision endpoints
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   └── db/
│       └── database.py         # Database setup
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

### Android Structure

```
auriza-android/
├── app/
│   ├── src/main/
│   │   ├── AndroidManifest.xml
│   │   ├── java/com/auriza/
│   │   │   ├── MainActivity.kt
│   │   │   ├── services/
│   │   │   │   ├── AudioCaptureService.kt
│   │   │   │   ├── VoiceRecognitionService.kt
│   │   │   │   └── AurizaAccessibilityService.kt
│   │   │   ├── network/
│   │   │   │   └── AurizaApiClient.kt
│   │   │   └── ui/
│   │   └── res/
│   ├── build.gradle
│   └── proguard-rules.pro
└── build.gradle (project level)
```

---

## ✨ Características Principales

### 1️⃣ NLP Avanzado
- Detección de intención
- Análisis de contexto
- Entidad recognition (en desarrollo)

### 2️⃣ Sistema de Memoria
**Short-term**: Conversación actual (100 últimas entradas)
**Long-term**: Preferencias y patrones del usuario

```python
# Almacenar memoria
await memory_service.store_memory(
    user_id=\"user_123\",
    content=\"El usuario ama el café\",
    memory_type=\"long_term\",
    tags=[\"preferences\"],
    importance=8
)

# Recuperar
memories = await memory_service.retrieve_memory(
    user_id=\"user_123\",
    tags=[\"preferences\"],
    limit=5
)
```

### 3️⃣ Voz Completa
- **STT**: Whisper (local o API)
- **TTS**: Coqui o gTTS
- **Wake word**: \"Hey Auriza\" detection

### 4️⃣ Decisiones Autónomas

3 niveles de autonomía:

🟢 **Manual**
```
Input → Responde
```

🔵 **Asistido** (por defecto)
```
Input → Analiza → Sugiere → Pide permiso (\"¿Lo ejecuto?\")
```

🔴 **Autónomo**
```
Input → Analiza → Ejecuta automáticamente → Informa
```

---

## 📡 API Endpoints

### Chat

#### POST `/api/chat/send`
Enviar mensaje a AURIZA

**Request:**
```json
{
  \"user_id\": \"user_123\",
  \"message\": \"¿Qué hora es?\",
  \"context\": {
    \"location\": \"home\",
    \"time_of_day\": \"morning\"
  }
}
```

**Response:**
```json
{
  \"response\": \"Son las 9:30 AM\",
  \"action\": \"inform\",
  \"confidence\": 0.95,
  \"executed\": true
}
```

#### GET `/api/chat/memory/{user_id}`
Obtener memoria del usuario

**Response:**
```json
{
  \"user_id\": \"user_123\",
  \"profile\": {
    \"short_term_memory_count\": 25,
    \"long_term_memory_count\": 50,
    \"learned_patterns\": [\"morning_routine\", \"work_hours\"]
  },
  \"recent_memories\": [...]
}
```

### Voice

#### POST `/api/voice/transcribe`
Convertir audio a texto (STT)

**Request:** Multipart form-data con archivo de audio

**Response:**
```json
{
  \"text\": \"Abre Spotify\",
  \"confidence\": 0.92
}
```

#### POST `/api/voice/synthesize`
Convertir texto a voz (TTS)

**Request:**
```
POST /api/voice/synthesize?text=Hola&language=es
```

**Response:**
```json
{
  \"text\": \"Hola\",
  \"audio_base64\": \"SUQzBAAAAAAAI1NDT0tFTkQ...\",
  \"content_type\": \"audio/mp3\"
}
```

### Decisions

#### POST `/api/decisions/analyze`
Analizar intención y sugerir acción

**Request:**
```json
{
  \"user_id\": \"user_123\",
  \"user_input\": \"Abre WhatsApp y envía un mensaje a Juan\",
  \"context\": {}
}
```

**Response:**
```json
{
  \"user_id\": \"user_123\",
  \"intent\": \"action\",
  \"confidence\": 0.88,
  \"action\": \"execute_with_confirmation\",
  \"requires_confirmation\": true,
  \"suggested_response\": \"¿Lo ejecuto?\"
}
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=True
ENVIRONMENT=development

# APIs
OPENAI_API_KEY=sk-xxx
DEEPGRAM_API_KEY=xxx

# Database
DATABASE_URL=sqlite:///./auriza.db
MONGODB_URL=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379

# Voice
LANGUAGE=es
VOICE_SAMPLE_RATE=16000

# AI
AI_MODEL=gpt-4
DECISION_AUTONOMY_LEVEL=assisted

# Security
SECRET_KEY=your_secret_key
```

### Niveles de Configuración

**development**
- Debug habilitado
- Logs detallados
- Hot reload

**production**
- Debug deshabilitado
- Optimizaciones
- Logs limitados

---

## 🧠 Personalidad IA

AURIZA tiene una personalidad bien definida:

**Características:**
- Directa y clara
- Inteligente
- Segura
- Ligeramente humana
- Crítica cuando es necesario

**Respuestas base:**
- \"Listo.\" - Confirmación simple
- \"Hecho.\" - Tarea completada
- \"Hay una mejor forma.\" - Sugerencia
- \"¿Lo ejecuto?\" - Pedir confirmación

**Principio central:**
\"No solo respondo. Entiendo, decido y actúo.\"

---

## 🤖 Sistema de Decisiones

El corazón de AURIZA es su capacidad de tomar decisiones:

### Flujo de Decisión

```
Input
  ↓
Intent Detection (¿Qué quiere el usuario?)
  ↓
Context Evaluation (¿Es seguro y posible?)
  ↓
Confidence Calculation (¿Cuán seguro estoy?)
  ↓
Decision Rule Application (¿Qué debo hacer?)
  ↓
Action (Ejecutar, Pedir permiso, o Informar)
```

### Confidence Thresholds

- **≥0.85**: Ejecutar automáticamente
- **0.60-0.85**: Pedir confirmación (asistido)
- **<0.60**: Pedir más información

### Learning from Decisions

```python
# AURIZA aprende de sus decisiones
await decision_service.learn_from_decision(
    intent=\"open_app\",
    was_correct=True,  # ¿Fue la decisión correcta?
    feedback=\"User was satisfied\"
)
```

---

## 💾 Sistema de Memoria

### Short-term Memory (Sesión)

```python
await memory_service.store_memory(
    user_id=\"user_123\",
    content=\"Usuario pregunta qué hora es\",
    memory_type=\"short_term\",
    importance=3
)
```

### Long-term Memory (Persistente)

```python
await memory_service.store_memory(
    user_id=\"user_123\",
    content=\"Usuario prefiere café con leche\",
    memory_type=\"long_term\",
    tags=[\"preferences\", \"coffee\"],
    importance=8
)
```

### Pattern Learning

```python
await memory_service.learn_pattern(
    user_id=\"user_123\",
    pattern_name=\"morning_routine\",
    pattern_data={
        \"actions\": [\"open_spotify\", \"start_coffee_maker\"],
        \"time\": \"07:00\"
    },
    confidence=0.9
)
```

---

## 🎤 Sistema de Voz

### STT (Speech-to-Text)

```python
text, confidence = await voice_service.speech_to_text(
    audio_data=audio_bytes,
    language=\"es\"
)
```

### TTS (Text-to-Speech)

```python
audio_bytes = await voice_service.text_to_speech(
    text=\"Hola, soy AURIZA\",
    language=\"es\",
    voice=\"neural\"
)
```

### Wake Word Detection

AURIZA se activa con:
- \"Hey Auriza\"
- \"Auriza\"
- Custom wake words (configurable)

---

## 📱 Android Integration

### AudioCaptureService

Captura audio de forma continua

```kotlin
// Iniciar captura
val intent = Intent(context, AudioCaptureService::class.java)
intent.action = \"ACTION_START_RECORDING\"
startService(intent)

// Detener
intent.action = \"ACTION_STOP_RECORDING\"
startService(intent)
```

### AurizaAccessibilityService

El \"Modo Dios\" - Control total del dispositivo

```kotlin
// Abrir aplicación
accessibilityService.openApp(\"com.whatsapp\")

// Buscar elemento
val element = accessibilityService.findElementByText(\"Send\")

// Hacer clic
accessibilityService.clickElement(element)

// Escribir texto
accessibilityService.writeText(\"Hola!\")

// Ejecutar rutina automática
accessibilityService.executeRoutine(listOf(
    AurizaAccessibilityService.RoutineStep(\"open_app\", \"com.whatsapp\"),
    AurizaAccessibilityService.RoutineStep(\"click\", \"Search\"),
    AurizaAccessibilityService.RoutineStep(\"type\", \"Juan\"),
    AurizaAccessibilityService.RoutineStep(\"click\", \"Juan García\"),
    AurizaAccessibilityService.RoutineStep(\"type\", \"Hola, ¿cómo estás?\"),
    AurizaAccessibilityService.RoutineStep(\"click\", \"Send\")
))
```

### API Client

```kotlin
// Enviar mensaje
val response = AurizaApiClient.apiService.sendMessage(
    ChatRequest(
        user_id = \"user_123\",
        message = \"Abre WhatsApp\",
        context = emptyMap()
    )
)

// Transcribir audio
val file = File(\"/path/to/audio.wav\")
val requestFile = file.asRequestBody(\"audio/wav\".toMediaType())
val part = MultipartBody.Part.createFormData(\"file\", file.name, requestFile)
val transcription = AurizaApiClient.apiService.transcribeAudio(part)
```

---

## 🚀 Deployment

### Local Development

```bash
# Backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# O con el script
python run.py
```

### Docker

```bash
# Build & Run
docker build -t auriza:latest .
docker run -p 8000:8000 auriza:latest

# Docker Compose (incluye databases)
docker-compose up
```

### Production

```bash
# Usar Gunicorn con múltiples workers
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# O con supervisord para monitoreo
supervisorctl start auriza
```

---

## 🧪 Testing

### Backend

```bash
# Unit tests
pytest

# Con cobertura
pytest --cov=app

# Test específico
pytest tests/test_decision_service.py
```

### API Testing

```bash
# cURL
curl -X POST http://localhost:8000/api/chat/send \\
  -H \"Content-Type: application/json\" \\
  -d '{\"user_id\":\"user_123\",\"message\":\"Hola\"}'

# Postman/Insomnia
# Importar endpoints de /docs
```

---

## 🔐 Seguridad

### Implementado

- ✅ CORS configurado
- ✅ Validación de inputs
- ✅ Rate limiting (en desarrollo)

### Por implementar

- [ ] JWT Authentication
- [ ] API Key management
- [ ] Encriptación de datos sensibles
- [ ] Audit logging

---

## 📊 Monitoring & Logs

### Logs

```bash
# Ver logs en tiempo real
tail -f auriza.log

# Filtrar por nivel
grep ERROR auriza.log
```

### Health Check

```bash
# Verificar que el servidor está activo
curl http://localhost:8000/health

# Obtener información
curl http://localhost:8000/info
```

---

## 🚀 Próximos Pasos

### Inmediatos
- [ ] Integrar Whisper para STT
- [ ] Implementar Coqui para TTS
- [ ] Setup MongoDB
- [ ] Redis caching

### Corto plazo
- [ ] Android app UI
- [ ] Accessibility Service testing
- [ ] WebSocket para real-time communication
- [ ] JWT Authentication

### Largo plazo
- [ ] Multi-language support
- [ ] Cloud deployment (AWS/GCP)
- [ ] Mobile optimization
- [ ] Advanced NLP (transformer models)
- [ ] Emotion recognition
- [ ] Custom wake words

---

## 📞 Soporte

- 📚 Documentación: `/docs`
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

**AURIZA v1.0.0** | \"No solo respondo. Entiendo, decido y actúo.\"
