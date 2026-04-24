# 🚀 AURIZA - Backend API

**Adaptive Unified Responsive Intelligent Zenith Assistant**

Un asistente virtual avanzado tipo Jarvis, superior a Siri, con personalidad propia, memoria, interacción por voz, capacidad de tomar decisiones autónomas y control avanzado del teléfono Android.

## 🎯 Características

- **NLP Avanzado**: Comprensión de intenciones, no solo palabras
- **Memoria Conversacional**: Corto y largo plazo
- **Voz Completa**: STT (escucha) + TTS (habla)
- **Aprendizaje**: Aprende patrones y preferencias del usuario
- **Decisiones Autónomas**: 3 niveles de autonomía
- **Arquitectura Modular**: Escalable y mantenible

## 🏗️ Arquitectura

```
app/
├── main.py              # Punto de entrada FastAPI
├── core/
│   ├── personality.py   # Definición de AURIZA
│   └── config.py        # Configuración
├── services/
│   ├── ai_service.py    # Integración LLM
│   ├── memory_service.py # Sistema de memoria
│   ├── voice_service.py  # STT + TTS
│   └── decision_service.py # Decisiones autónomas
├── routes/
│   ├── chat.py          # Chat endpoints
│   ├── voice.py         # Voice endpoints
│   └── decisions.py     # Decision endpoints
├── models/
│   └── schemas.py       # Pydantic models
└── db/
    └── database.py      # Database setup
```

## 🔧 Instalación

### Requisitos
- Python 3.10+
- pip o poetry
- Virtual environment

### Setup

1. **Crear virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# o
source venv/bin/activate       # macOS/Linux
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus valores
```

4. **Ejecutar servidor**
```bash
python -m uvicorn app.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## 📡 Endpoints

### Chat
- `POST /api/chat/send` - Enviar mensaje
- `GET /api/chat/memory/{user_id}` - Obtener memoria del usuario
- `POST /api/chat/clear-history/{user_id}` - Limpiar historial

### Voice
- `POST /api/voice/transcribe` - STT (audio → texto)
- `POST /api/voice/synthesize` - TTS (texto → audio)
- `POST /api/voice/activate` - Activar listening
- `POST /api/voice/process-stream` - Procesar streaming audio

### Decisions
- `POST /api/decisions/analyze` - Analizar intención
- `POST /api/decisions/learn` - Registrar feedback
- `POST /api/decisions/set-autonomy` - Cambiar nivel de autonomía
- `GET /api/decisions/stats` - Obtener estadísticas

## 🧠 AURIZA Personality

```
"No solo respondo. Entiendo, decido y actúo."

Dirección: Habla directo, sin rodeos
Inteligencia: Entiende intención, no solo palabras
Seguridad: Decide con confianza
Humanidad: Ligeramente humana, sin exagerar
Crítica: Sugiere mejores formas cuando es necesario
```

## 🤖 Niveles de Autonomía

🟢 **Manual**
- Solo responde
- Espera confirmación

🔵 **Asistido** (default)
- Sugiere acciones
- Pregunta: "¿Lo ejecuto?"

🔴 **Autónomo**
- Ejecuta automáticamente
- Informa después: "Ya lo hice"

## 🗄️ Memoria

### Short-term (Sesión actual)
- Conversación reciente
- Contexto actual
- Último máx 100 entradas

### Long-term (Persistente)
- Preferencias del usuario
- Patrones aprendidos
- Historial importante

## 🔐 Seguridad

- JWT Authentication (en desarrollo)
- Rate limiting
- CORS configurado
- Validación de inputs

## 📝 Uso

### Chat Simple
```python
import requests

response = requests.post(
    \"http://localhost:8000/api/chat/send\",
    json={
        \"user_id\": \"user_123\",
        \"message\": \"¿Qué hora es?\",
        \"context\": {\"location\": \"home\"}
    }
)

print(response.json())
```

### Voice
```python
# Transcribir audio
with open(\"audio.wav\", \"rb\") as f:
    files = {\"file\": f}
    response = requests.post(
        \"http://localhost:8000/api/voice/transcribe\",
        files=files
    )

# Sintetizar voz
response = requests.post(
    \"http://localhost:8000/api/voice/synthesize\",
    params={
        \"text\": \"Hola, soy AURIZA\",
        \"language\": \"es\"
    }
)
```

## 🧪 Testing

```bash
pytest
pytest --cov=app  # Con cobertura
```

## 🐳 Docker

```bash
docker build -t auriza:latest .
docker run -p 8000:8000 auriza:latest
```

O con docker-compose:
```bash
docker-compose up
```

## 📚 Documentación API

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🚀 Próximos Pasos

- [ ] Integración OpenAI API completa
- [ ] Whisper STT (local)
- [ ] Coqui TTS (local)
- [ ] MongoDB setup
- [ ] Redis caching
- [ ] Celery para tareas async
- [ ] Android app
- [ ] Accessibility Service integration

## 📞 Soporte

Para reportar issues o sugerencias, abre un issue en el repositorio.

---

**AURIZA v1.0.0** | Made with ❤️ by AURIZA Team
