# 🧪 AURIZA - Ejemplos de Testing

## Testing del Backend

### 1. Health Check

```bash
curl http://localhost:8000/health

# Response:
# {
#   \"status\": \"healthy\",
#   \"agent\": \"AURIZA\",
#   \"version\": \"1.0.0\"
# }
```

### 2. Get AURIZA Info

```bash
curl http://localhost:8000/info

# Response:
# {
#   \"name\": \"AURIZA\",
#   \"full_name\": \"Adaptive Unified Responsive Intelligent Zenith Assistant\",
#   \"version\": \"1.0.0\",
#   \"personality\": \"Direct, Intelligent, Confident, Slightly Humane\",
#   \"autonomy_level\": \"assisted\",
#   \"language\": \"es\",
#   \"capabilities\": [...]
# }
```

### 3. Chat - Simple Message

```bash
curl -X POST http://localhost:8000/api/chat/send \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"user_id\": \"user_123\",
    \"message\": \"Hola AURIZA\",
    \"context\": {}
  }'
```

### 4. Chat - With Context

```bash
curl -X POST http://localhost:8000/api/chat/send \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"user_id\": \"user_123\",
    \"message\": \"¿Qué hora es?\",
    \"context\": {
      \"location\": \"home\",
      \"time_of_day\": \"morning\",
      \"device\": \"android\"
    }
  }'
```

### 5. Analyze Intent

```bash
curl -X POST \"http://localhost:8000/api/decisions/analyze?user_id=user_123&user_input=Abre%20Spotify\" \\
  -H \"Content-Type: application/json\" \\
  -d '{}'

# Response:
# {
#   \"user_id\": \"user_123\",
#   \"intent\": \"action\",
#   \"confidence\": 0.85,
#   \"action\": \"execute\",
#   \"requires_confirmation\": false,
#   \"suggested_response\": \"Listo. Ejecutado.\",
#   \"context_score\": 0.80
# }
```

### 6. Set Autonomy Level

```bash
curl -X POST \"http://localhost:8000/api/decisions/set-autonomy?user_id=user_123&level=autonomous\" \\
  -H \"Content-Type: application/json\"

# Response:
# {
#   \"status\": \"updated\",
#   \"user_id\": \"user_123\",
#   \"autonomy_level\": \"autonomous\"
# }
```

### 7. Get User Memory

```bash
curl http://localhost:8000/api/chat/memory/user_123?limit=10

# Response:
# {
#   \"user_id\": \"user_123\",
#   \"profile\": {
#     \"short_term_memory_count\": 25,
#     \"long_term_memory_count\": 50,
#     \"learned_patterns\": [\"morning_routine\", \"work_hours\"],
#     \"patterns_confidence\": {
#       \"morning_routine\": 0.9,
#       \"work_hours\": 0.85
#     }
#   },
#   \"recent_memories\": [...]
# }
```

### 8. Decision Learning

```bash
curl -X POST \"http://localhost:8000/api/decisions/learn?user_id=user_123&intent=action&was_correct=true\" \\
  -H \"Content-Type: application/json\" \\
  -d '{\"feedback\": \"User was satisfied with the action\"}'

# Response:
# {
#   \"status\": \"learned\",
#   \"user_id\": \"user_123\",
#   \"intent\": \"action\",
#   \"feedback_recorded\": true
# }
```

---

## Python Testing Script

```python
import requests
import json

BASE_URL = \"http://localhost:8000\"

class AurizaTester:
    def __init__(self):
        self.session = requests.Session()
    
    def health_check(self):
        \"\"\"Verify server is running\"\"\"
        response = self.session.get(f\"{BASE_URL}/health\")
        print(\"✅ Health Check:\", response.json())
        return response.status_code == 200
    
    def get_info(self):
        \"\"\"Get AURIZA info\"\"\"
        response = self.session.get(f\"{BASE_URL}/info\")
        print(\"✅ Info:\", response.json())
    
    def send_message(self, user_id, message, context=None):
        \"\"\"Send a message\"\"\"
        payload = {
            \"user_id\": user_id,
            \"message\": message,
            \"context\": context or {}
        }
        response = self.session.post(
            f\"{BASE_URL}/api/chat/send\",
            json=payload
        )
        print(f\"✅ Message Response: {response.json()}\")
        return response.json()
    
    def analyze_intent(self, user_id, user_input):
        \"\"\"Analyze user input\"\"\"
        response = self.session.post(
            f\"{BASE_URL}/api/decisions/analyze\",
            params={
                \"user_id\": user_id,
                \"user_input\": user_input
            },
            json={}
        )
        print(f\"✅ Intent Analysis: {response.json()}\")
        return response.json()
    
    def get_memory(self, user_id):
        \"\"\"Get user memory\"\"\"
        response = self.session.get(
            f\"{BASE_URL}/api/chat/memory/{user_id}\"
        )
        print(f\"✅ User Memory: {response.json()}\")
        return response.json()
    
    def run_all_tests(self):
        \"\"\"Run all tests\"\"\"
        print(\"\\n🧪 Running AURIZA Tests...\\n\")
        
        # Test 1
        if not self.health_check():
            print(\"❌ Server not running!\")
            return
        
        # Test 2
        self.get_info()
        
        # Test 3
        print(\"\\n--- Testing Chat ---\")
        self.send_message(\"demo_user\", \"Hola AURIZA\")
        self.send_message(\"demo_user\", \"¿Qué hora es?\", {\"location\": \"home\"})\n        \n        # Test 4\n        print(\"\\n--- Testing Decisions ---\")\n        self.analyze_intent(\"demo_user\", \"Abre Spotify\")\n        self.analyze_intent(\"demo_user\", \"¿Cuál es mi nombre?\")\n        \n        # Test 5\n        print(\"\\n--- Testing Memory ---\")\n        self.get_memory(\"demo_user\")\n        \n        print(\"\\n✅ All tests completed!\")\n\n# Run\nif __name__ == \"__main__\":\n    tester = AurizaTester()\n    tester.run_all_tests()\n```

**Ejecutar:**
```bash
python test_auriza.py\n```\n\n---\n\n## Postman Collection\n\n```json\n{\n  \"info\": {\n    \"name\": \"AURIZA API\",\n    \"schema\": \"https://schema.getpostman.com/json/collection/v2.1.0/collection.json\"\n  },\n  \"item\": [\n    {\n      \"name\": \"Health Check\",\n      \"request\": {\n        \"method\": \"GET\",\n        \"url\": \"{{baseUrl}}/health\"\n      }\n    },\n    {\n      \"name\": \"Send Message\",\n      \"request\": {\n        \"method\": \"POST\",\n        \"header\": [\n          {\"key\": \"Content-Type\", \"value\": \"application/json\"}\n        ],\n        \"url\": \"{{baseUrl}}/api/chat/send\",\n        \"body\": {\n          \"mode\": \"raw\",\n          \"raw\": \"{\\n  \\\"user_id\\\": \\\"user_123\\\",\\n  \\\"message\\\": \\\"Hola\\\",\\n  \\\"context\\\": {}\\n}\"\n        }\n      }\n    },\n    {\n      \"name\": \"Analyze Intent\",\n      \"request\": {\n        \"method\": \"POST\",\n        \"url\": {\n          \"raw\": \"{{baseUrl}}/api/decisions/analyze?user_id=user_123&user_input=Abre%20Spotify\",\n          \"protocol\": \"http\",\n          \"host\": [\"localhost\"],\n          \"port\": \"8000\",\n          \"path\": [\"api\", \"decisions\", \"analyze\"],\n          \"query\": [\n            {\"key\": \"user_id\", \"value\": \"user_123\"},\n            {\"key\": \"user_input\", \"value\": \"Abre Spotify\"}\n          ]\n        }\n      }\n    }\n  ]\n}\n```\n\n---\n\n## Performance Testing\n\n### Load Test con Apache Bench\n\n```bash\n# Test 100 requests, 10 concurrent\nab -n 100 -c 10 http://localhost:8000/health\n\n# Resultado esperado:\n# Requests per second: > 1000\n# Time per request: < 10ms\n```\n\n### Load Test con Locust\n\n```python\nfrom locust import HttpUser, task, between\n\nclass AurizaUser(HttpUser):\n    wait_time = between(1, 3)\n    \n    @task(1)\n    def health_check(self):\n        self.client.get(\"/health\")\n    \n    @task(2)\n    def send_message(self):\n        self.client.post(\n            \"/api/chat/send\",\n            json={\n                \"user_id\": \"user_123\",\n                \"message\": \"Hola\",\n                \"context\": {}\n            }\n        )\n    \n    @task(1)\n    def analyze_intent(self):\n        self.client.post(\n            \"/api/decisions/analyze\",\n            params={\n                \"user_id\": \"user_123\",\n                \"user_input\": \"Abre Spotify\"\n            }\n        )\n```\n\n**Ejecutar:**\n```bash\nlocust -f locustfile.py --host=http://localhost:8000\n```\n\n---\n\n## Unit Tests\n\n```python\nimport pytest\nfrom app.services.decision_service import DecisionService, IntentType\n\n@pytest.mark.asyncio\nasync def test_intent_detection():\n    service = DecisionService()\n    \n    # Test ACTION intent\n    intent, confidence = await service._detect_intent(\n        \"Abre Spotify\",\n        {}\n    )\n    assert intent == IntentType.ACTION\n    assert confidence > 0.7\n    \n    # Test INFORMATION intent\n    intent, confidence = await service._detect_intent(\n        \"¿Qué hora es?\",\n        {}\n    )\n    assert intent == IntentType.INFORMATION\n\n@pytest.mark.asyncio\nasync def test_decision_autonomy():\n    service = DecisionService(autonomy_level=\"assisted\")\n    \n    result = await service.analyze_and_decide(\n        user_input=\"Abre Spotify\",\n        user_context={},\n        user_preferences={}\n    )\n    \n    assert \"intent\" in result\n    assert \"confidence\" in result\n    assert \"action\" in result\n    assert result[\"confidence\"] <= 1.0\n```\n\n**Ejecutar:**\n```bash\npytest tests/\npytest --cov=app tests/\n```\n\n---\n\n**¡Listo para testear!**\n"