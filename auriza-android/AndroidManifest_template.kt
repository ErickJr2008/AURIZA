package com.auriza

/**
 * Android Manifest configuration template
 * 
 * Add this to your actual AndroidManifest.xml
 */

/*
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\"
    package=\"com.auriza.assistant\">

    <!-- Network -->
    <uses-permission android:name=\"android.permission.INTERNET\" />
    <uses-permission android:name=\"android.permission.CHANGE_NETWORK_STATE\" />
    
    <!-- Audio -->
    <uses-permission android:name=\"android.permission.RECORD_AUDIO\" />
    
    <!-- System -->
    <uses-permission android:name=\"android.permission.QUERY_ALL_PACKAGES\" />
    <uses-permission android:name=\"android.permission.ACCESS_NOTIFICATION_POLICY\" />
    
    <!-- Activities / Services -->
    <application
        android:allowBackup=\"true\"
        android:icon=\"@mipmap/ic_launcher\"
        android:label=\"@string/app_name\"
        android:supportsRtl=\"true\"
        android:theme=\"@style/Theme.AURIZA\">
        
        <!-- Main Activity -->
        <activity
            android:name=\".MainActivity\"
            android:exported=\"true\"
            android:theme=\"@style/Theme.AURIZA\">
            <intent-filter>
                <action android:name=\"android.intent.action.MAIN\" />
                <category android:name=\"android.intent.category.LAUNCHER\" />
            </intent-filter>
        </activity>
        
        <!-- Voice Recognition Service -->
        <service
            android:name=\".services.VoiceRecognitionService\"
            android:enabled=\"true\"
            android:exported=\"true\" />
        
        <!-- Audio Capture Service -->
        <service
            android:name=\".services.AudioCaptureService\"
            android:enabled=\"true\"
            android:exported=\"true\" />
        
        <!-- Accessibility Service (IMPORTANTE) -->
        <service
            android:name=\".services.AurizaAccessibilityService\"
            android:permission=\"android.permission.BIND_ACCESSIBILITY_SERVICE\"
            android:enabled=\"true\"
            android:exported=\"true\">
            <intent-filter>
                <action android:name=\"android.accessibilityservice.AccessibilityService\" />
            </intent-filter>
            <meta-data
                android:name=\"android.accessibilityservice\"
                android:resource=\"@xml/accessibility_service_config\" />
        </service>
        
    </application>

</manifest>
*/
