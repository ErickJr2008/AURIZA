# 📱 AURIZA Android App

Aplicación Android nativa para controlar tu dispositivo con AURIZA.

## 📋 Requisitos

- Android SDK 29+
- Kotlin 1.9+
- Gradle 8.0+
- Android Studio

## 🏗️ Estructura del Proyecto

```
auriza-android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── java/com/auriza/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── services/
│   │   │   │   │   ├── AudioCaptureService.kt
│   │   │   │   │   ├── VoiceRecognitionService.kt
│   │   │   │   │   └── AccessibilityService.kt
│   │   │   │   ├── network/
│   │   │   │   │   └── ApiClient.kt
│   │   │   │   ├── ui/
│   │   │   │   │   ├── screens/
│   │   │   │   │   └── components/
│   │   │   │   └── utils/
│   │   │   └── res/
│   │   └── test/
│   └── build.gradle
├── build.gradle
└── settings.gradle
```

## ⚙️ Permisos Necesarios

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name=\"android.permission.INTERNET\" />
<uses-permission android:name=\"android.permission.RECORD_AUDIO\" />
<uses-permission android:name=\"android.permission.QUERY_ALL_PACKAGES\" />
<uses-permission android:name=\"android.permission.CHANGE_NETWORK_STATE\" />
```

## 🔧 Configuración

1. Crear proyecto en Android Studio
2. Configurar build.gradle
3. Añadir dependencias
4. Configurar API base URL

## 🎤 Características Principales

- **Voice Capture**: Grabación de audio contínua
- **Wake Word Detection**: Detecta \"Hey Auriza\"
- **Accessibility Service**: Control del dispositivo
- **Real-time Communication**: WebSocket con backend
- **UI Jarvis-style**: Interfaz minimalista y animada

## 📝 Próximos Pasos

- [ ] Setup Kotlin/Gradle
- [ ] Implementar AudioCaptureService
- [ ] Crear VoiceRecognitionService
- [ ] Implementar AccessibilityService
- [ ] Crear UI/UX
- [ ] Testing
