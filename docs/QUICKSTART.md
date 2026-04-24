# 🎯 AURIZA - Quick Start (5 minutos)

## ✅ Lo que haremos

1. Arrancar backend con FastAPI
2. Probar un endpoint
3. Ver Swagger docs
4. Hacer primer request

---

## 🚀 START

### Paso 1: Preparar Backend

```bash
# 1. Ir a carpeta backend
cd auriza-backend

# 2. Crear virtual environment
python -m venv venv

# 3. Activar (elige tu SO)
# Windows:
.\\venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias (esperar 1-2 min)
pip install -r requirements.txt

# 5. Copiar .env
copy .env.example .env
```

### Paso 2: Ejecutar Servidor

```bash
# Opción A: Directo
python -m uvicorn app.main:app --reload

# Opción B: Con script
python run.py

# Esperar hasta ver:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Paso 3: Probar Endpoints

**En otra terminal (con venv activado):**

```bash
# Test 1: Health check
curl http://localhost:8000/health

# Resultado esperado:
# {\"status\":\"healthy\",\"agent\":\"AURIZA\",\"version\":\"1.0.0\"}

# Test 2: Información
curl http://localhost:8000/info

# Test 3: Enviar mensaje
curl -X POST http://localhost:8000/api/chat/send \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"user_id\": \"demo_user\",
    \"message\": \"Hola AURIZA\",
    \"context\": {}
  }'
```

### Paso 4: Ver Documentación

Abre en tu navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎉 ¡Listo!

Ya tienes AURIZA corriendo. Ahora:

- 📖 Lee [SETUP_GUIDE.md](SETUP_GUIDE.md) para profundizar
- 📱 Mira los archivos de Android en `auriza-android/`
- 🧠 Explora `app/services/` para ver los componentes
- 🔧 Modifica `.env` para cambiar configuración

---

## 🆘 Problemas Comunes

### Error: \"module not found\"
```bash
# Verifica que venv esté activado
# En Windows, deberías ver (venv) en la terminal
# Si no, ejecuta:
.\\venv\\Scripts\\activate
```

### Puerto 8000 ya en uso
```bash
# Cambiar puerto en .env o:
python -m uvicorn app.main:app --reload --port 8001
```

### Error de dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## 📡 Primeros Requests

### Python
```python
import requests

response = requests.post(
    \"http://localhost:8000/api/chat/send\",
    json={
        \"user_id\": \"user_123\",
        \"message\": \"¿Qué puedes hacer?\",
        \"context\": {}
    }
)

print(response.json())
```

### JavaScript
```javascript
fetch('http://localhost:8000/api/chat/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    user_id: 'user_123',
    message: '¿Qué puedes hacer?',
    context: {}
  })
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción |\n|--------|----------|-------------|\n| GET | `/health` | Health check |\n| GET | `/info` | Info de AURIZA |\n| POST | `/api/chat/send` | Enviar mensaje |\n| GET | `/api/chat/memory/{user_id}` | Obtener memoria |\n| POST | `/api/voice/transcribe` | STT (audio→texto) |\n| POST | `/api/voice/synthesize` | TTS (texto→audio) |\n| POST | `/api/decisions/analyze` | Analizar intención |\n| POST | `/api/decisions/set-autonomy` | Cambiar autonomía |\n\n---

## 🎓 Siguiente Paso

Lee [ARCHITECTURE.md](ARCHITECTURE.md) para entender cómo funciona AURIZA internamente.\n\n**¡Disfruta!**\n"