package com.auriza.network

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import okhttp3.OkHttpClient
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Response
import com.google.gson.JsonObject
import java.util.concurrent.TimeUnit

/**
 * AURIZA API Client - Comunicación con backend
 */
interface AurizaApiService {
    
    @POST(\"api/chat/send\")
    suspend fun sendMessage(@Body request: ChatRequest): Response<ChatResponse>
    
    @Multipart
    @POST(\"api/voice/transcribe\")
    suspend fun transcribeAudio(
        @Part file: MultipartBody.Part
    ): Response<VoiceResponse>
    
    @POST(\"api/voice/synthesize\")
    suspend fun synthesizeSpeech(
        @Query(\"text\") text: String,
        @Query(\"language\") language: String = \"es\"
    ): Response<SynthesizeResponse>
    
    @POST(\"api/decisions/analyze\")
    suspend fun analyzeIntent(
        @Query(\"user_id\") userId: String,
        @Query(\"user_input\") userInput: String,
        @Body context: JsonObject?
    ): Response<DecisionResponse>
    
    @GET(\"health\")
    suspend fun healthCheck(): Response<HealthResponse>
    
    @GET(\"info\")
    suspend fun getAurizaInfo(): Response<AurizaInfoResponse>
}

/**
 * Request/Response Models
 */
data class ChatRequest(
    val user_id: String,
    val message: String,
    val context: Map<String, Any>? = null
)

data class ChatResponse(
    val response: String,
    val action: String? = null,
    val confidence: Float,
    val executed: Boolean
)

data class VoiceResponse(
    val text: String,
    val audio_url: String? = null,
    val confidence: Float
)

data class SynthesizeResponse(
    val text: String,
    val audio_base64: String,
    val content_type: String
)

data class DecisionResponse(
    val user_id: String,
    val intent: String,
    val confidence: Float,
    val action: String,
    val requires_confirmation: Boolean
)

data class HealthResponse(
    val status: String,
    val agent: String,
    val version: String
)

data class AurizaInfoResponse(
    val name: String,
    val full_name: String,
    val version: String,
    val personality: String,
    val autonomy_level: String,
    val language: String,
    val capabilities: List<String>
)

/**
 * API Client Singleton
 */
object AurizaApiClient {
    
    private const val BASE_URL = \"http://localhost:8000/\"
    
    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .client(okHttpClient)
        .build()
    
    val apiService: AurizaApiService = retrofit.create(AurizaApiService::class.java)
}
