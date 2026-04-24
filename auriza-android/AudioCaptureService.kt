package com.auriza.services

import android.app.Service
import android.content.Context
import android.content.Intent
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.os.IBinder
import kotlinx.coroutines.*
import java.io.ByteArrayOutputStream

/**
 * AudioCaptureService - Captures audio continuously from microphone
 * 
 * Handles:
 * - Audio recording from microphone
 * - Wake word detection (\"Hey Auriza\")
 * - Audio buffer management
 * - Streaming to backend
 */
class AudioCaptureService : Service() {
    
    private var audioRecord: AudioRecord? = null
    private var isRecording = false
    private val serviceScope = CoroutineScope(Dispatchers.Default + Job())
    
    // Audio configuration
    companion object {
        const val SAMPLE_RATE = 16000
        const val CHANNEL_CONFIG = AudioFormat.CHANNEL_IN_MONO
        const val AUDIO_FORMAT = AudioFormat.ENCODING_PCM_16BIT
        const val BUFFER_SIZE_FACTOR = 2
    }
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            \"ACTION_START_RECORDING\" -> startRecording()
            \"ACTION_STOP_RECORDING\" -> stopRecording()
        }
        return START_STICKY
    }
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    private fun startRecording() {
        if (isRecording) return
        
        val minBufferSize = AudioRecord.getMinBufferSize(
            SAMPLE_RATE,
            CHANNEL_CONFIG,
            AUDIO_FORMAT
        )
        
        val bufferSize = minBufferSize * BUFFER_SIZE_FACTOR
        
        audioRecord = AudioRecord(
            MediaRecorder.AudioSource.MIC,
            SAMPLE_RATE,
            CHANNEL_CONFIG,
            AUDIO_FORMAT,
            bufferSize
        )
        
        audioRecord?.startRecording()
        isRecording = true
        
        // Start recording loop
        serviceScope.launch {
            recordingLoop(bufferSize)
        }
    }
    
    private suspend fun recordingLoop(bufferSize: Int) {
        val audioData = ByteArray(bufferSize)
        val outputStream = ByteArrayOutputStream()
        
        while (isRecording) {
            val bytesRead = audioRecord?.read(audioData, 0, audioData.size) ?: 0
            
            if (bytesRead > 0) {
                outputStream.write(audioData, 0, bytesRead)
                
                // Send chunk to backend for processing
                sendAudioChunk(audioData, bytesRead)
            }
            
            delay(100) // Process every 100ms
        }
    }
    
    private suspend fun sendAudioChunk(data: ByteArray, size: Int) {
        // TODO: Send to backend via API
        // This will be connected to the decision service
    }
    
    private fun stopRecording() {
        isRecording = false
        audioRecord?.stop()
        audioRecord?.release()
        audioRecord = null
    }
    
    override fun onDestroy() {
        stopRecording()
        serviceScope.cancel()
        super.onDestroy()
    }
}
