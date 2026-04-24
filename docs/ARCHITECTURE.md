# 🏗️ AURIZA - Arquitectura Técnica

## Sistema de Capas

```
┌─────────────────────────────────────────────┐
│          🤖 AURIZA ASSISTANT               │
│         (Personalidad + Decisiones)        │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      API ROUTES (FastAPI)                  │
│  ├─ Chat (conversaciones)                  │
│  ├─ Voice (STT/TTS)                        │
│  └─ Decisions (autonomía)                  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        SERVICES LAYER                      │
│  ├─ AI Service (LLM)                       │
│  ├─ Memory Service (short/long term)       │
│  ├─ Voice Service (audio)                  │
│  └─ Decision Service (autonomy engine)     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        CORE LAYER                          │
│  ├─ Personality Config                     │
│  ├─ Intent Detection                       │
│  └─ Decision Rules                         │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        DATA LAYER                          │
│  ├─ SQLite (development)                   │
│  ├─ PostgreSQL (production)                │
│  ├─ MongoDB (long-term memory)             │
│  └─ Redis (caching)                        │
└─────────────────────────────────────────────┘
```

## Flujo de Procesamiento

### 1. Chat Request

```
User: \"Abre Spotify\"
        ↓
    [FastAPI Router]
        ↓
    [Decision Service]
    - Detecta intent: ACTION
    - Confidence: 0.88
    - Autonomy level: ASSISTED
        ↓
    \"¿Lo ejecuto?\"
        ↓
    User: \"Sí\"
        ↓
    [Android - Accessibility Service]
    - Abre Spotify
        ↓
    Response: \"Spotify abierto\"
```

### 2. Voice Request

```
User: \"Hey Auriza...\"
        ↓
[Audio Capture Service]
        ↓
    [STT - Whisper]
    Audio → \"Qué hora es\"
        ↓
[Intent Detection]
    → INFORMATION
        ↓
[AI Service]
    → \"Son las 9:30 AM\"
        ↓
    [TTS - Coqui]
    Text → Audio
        ↓
[Reproduce audio]
```

### 3. Memory Management

```
User Input
    ↓
[Store Short-term]
    ↓
[Analyze Patterns]
    ↓
[Move to Long-term if important]
    ↓
[Update User Profile]
```

## Decision Engine (Corazón de AURIZA)

```python
class DecisionService:
    
    async def analyze_and_decide(input, context):
        
        # Paso 1: Detectar Intención
        intent, confidence = detect_intent(input)
        
        # Paso 2: Evaluar Contexto
        context_score = evaluate_context(intent, context)
        
        # Paso 3: Calcular Confianza Final
        final_confidence = (confidence + context_score) / 2
        
        # Paso 4: Aplicar Regla de Decisión
        if autonomy_level == \"autonomous\":
            if final_confidence >= 0.85:
                return \"execute\"
            elif final_confidence >= 0.60:
                return \"execute_with_caution\"
            else:
                return \"inform\"
        
        elif autonomy_level == \"assisted\":
            if final_confidence >= 0.85:
                return \"execute\"
            elif final_confidence >= 0.60:
                return \"ask_permission\"
            else:
                return \"inform_and_ask\"
        
        else:  # manual
            return \"inform\"
```

## Niveles de Autonomía (Decision Matrix)

```
Confidence ≥ 0.85  | Confidence 0.60-0.85 | Confidence < 0.60
─────────────────────────────────────────────────────────────

AUTONOMOUS:
  Execute          | Execute + caution    | Ask for confirmation

ASSISTED:
  Execute          | Ask permission       | Ask for more info

MANUAL:
  Inform          | Inform               | Inform
```

## Memory Architecture

### Short-term (Sesión)
```
- In-memory storage
- Max 100 entradas
- FIFO cuando llena
- Conversación actual
```

### Long-term (Persistente)
```
- Base de datos
- Ilimitado
- Patrones + preferencias
- Organizado por tags
```

### Learning
```
Cada decisión → Feedback → Ajuste de confianza
Pattern confidence = 0.0 → 1.0 (actualiza con cada interacción)
```

## API Response Flow

```
Request
  ↓
[FastAPI Route]
  ↓
[Validate Input]
  ↓
[Get User Context]
  ↓
[Decision Service]
  ↓
[Store in Memory]
  ↓
[Generate Response]
  ↓
[Format Output]
  ↓
Response
```

## Componentes Principales

### 1. Personality System
**Archivo**: `app/core/personality.py`

Define:
- Tone and voice
- Response patterns
- Decision rules
- System prompt para IA

### 2. Decision Service
**Archivo**: `app/services/decision_service.py`

Implementa:
- Intent detection
- Context evaluation
- Confidence calculation
- Action determination

### 3. Memory Service
**Archivo**: `app/services/memory_service.py`

Gestiona:
- Short-term memory
- Long-term memory
- Pattern learning
- User profile

### 4. AI Service
**Archivo**: `app/services/ai_service.py`

Proporciona:
- LLM integration
- Response generation
- Conversation history

### 5. Voice Service
**Archivo**: `app/services/voice_service.py`

Maneja:
- Speech-to-text
- Text-to-speech
- Audio processing

## Intent Detection Algorithm

```python
def detect_intent(user_input):
    intent_patterns = {
        ACTION: [\"abre\", \"reproduce\", \"envía\"],
        CONTROL: [\"sube\", \"apaga\", \"enciende\"],
        INFORMATION: [\"qué\", \"cuál\", \"cuándo\"],
        AUTOMATION: [\"rutina\", \"configura\"],
        DECISION: [\"debería\", \"está bien\"],
        LEARNING: [\"recuerda\", \"aprende\"]
    }
    
    # Buscar patrones
    for intent, patterns in intent_patterns.items():\n        for pattern in patterns:
            if pattern in user_input.lower():
                confidence = 0.85 if user_input.startswith(pattern) else 0.70
                return intent, confidence
    
    return QUERY, 0.60  # Default
```

## Data Models

### ChatRequest
```
- user_id: str
- message: str
- context: Dict[str, Any]
- autonomy_override: Optional[str]
```

### ChatResponse
```
- response: str
- action: Optional[str]
- confidence: float (0-1)
- executed: bool
- timestamp: datetime
```

### Decision
```
- user_id: str
- intent: str
- action: str
- confidence: float (0-1)
- autonomy_level: str
- parameters: Dict[str, Any]
- requires_confirmation: bool
```

## Escalabilidad

### Horizontal Scaling
```
┌─────────────┐     ┌─────────────┐
│ AURIZA API  │     │ AURIZA API  │
│ Instance 1  │     │ Instance 2  │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └───────┬───────────┘
               │
         ┌─────▼──────┐
         │   Redis    │
         │  (Cache)   │
         └─────┬──────┘
               │
         ┌─────▼──────┐
         │  MongoDB   │
         │  (Memory)  │
         └────────────┘
```

### Vertical Scaling
```
- Gunicorn workers: 4-8
- Uvicorn workers per process
- Connection pooling
- Query optimization
```

## Seguridad

### Niveles
1. **Input Validation**: Pydantic models
2. **Authentication**: JWT (en desarrollo)
3. **Authorization**: Role-based access
4. **Encryption**: HTTPS en production
5. **Rate Limiting**: Token bucket

### CORS
```python
CORSMiddleware(
    allow_origins=[\"*\"],  # Configurar en prod
    allow_credentials=True,
    allow_methods=[\"*\"],
    allow_headers=[\"*\"]
)
```

## Monitoreo & Logging

### Levels
```
DEBUG   - Información detallada
INFO    - Eventos generales
WARNING - Advertencias
ERROR   - Errores
CRITICAL- Críticos
```

### Metrics (Future)
```
- Request count
- Response time
- Error rate
- Memory usage
- CPU usage
- Decision accuracy
```

## Integración Android

### Services
1. **AudioCaptureService**: Captura de audio
2. **VoiceRecognitionService**: Reconocimiento de voz
3. **AurizaAccessibilityService**: Control del dispositivo

### Communication
```
Android App
    ↓
REST API (HTTP)
    ↓
Backend Services
    ↓
Ejecutar acciones
```

### Accessibility Service Features
```
- Leer contenido de pantalla
- Hacer clics
- Escribir texto
- Navegar interfaces
- Automatizar tareas
```

## Deployment Architecture

### Development
```
Local machine
├── Backend (uvicorn)
├── SQLite
└── Redis (opcional)
```

### Production
```
Docker Container
├── Backend (Gunicorn)
├── PostgreSQL
├── MongoDB
├── Redis
└── Load Balancer
```

---

## Performance Targets

- **Response time**: < 500ms (50th percentile)
- **Decision confidence**: > 80% en promedio
- **Memory accuracy**: > 95%
- **API availability**: 99.9%

---

**AURIZA v1.0.0** | Built with FastAPI, Kubernetes-ready, AI-powered
