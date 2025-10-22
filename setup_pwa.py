#!/usr/bin/env python3
"""
A.U.R.A PWA Setup Script
Sets up the Progressive Web App with all necessary files and configurations
"""

import os
import json
import subprocess
import sys

def setup_pwa():
    """Set up A.U.R.A as a Progressive Web App"""
    print("🚀 Setting up A.U.R.A as a Progressive Web App...")
    
    # Check if required files exist
    required_files = [
        'manifest.json',
        'sw.js',
        'aura_gradio_app.py'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    # Check if icons directory exists
    if not os.path.exists('icons'):
        print("📁 Creating icons directory...")
        os.makedirs('icons')
    
    # Generate icons if they don't exist
    if not os.path.exists('icons/icon-192x192.png'):
        print("🎨 Generating PWA icons...")
        try:
            subprocess.run([sys.executable, 'generate_icons.py'], check=True)
        except subprocess.CalledProcessError:
            print("⚠️  Icon generation failed, but continuing...")
    
    # Create a simple index.html for PWA
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A.U.R.A - Adaptive User Retention Assistant</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#E85002">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="A.U.R.A">
    <link rel="apple-touch-icon" href="/icons/icon-192x192.png">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #F9F9F9 0%, #A7A7A7 30%, #646464 70%, #333333 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .loading-container {
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #E85002;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        h1 { color: #E85002; margin-bottom: 10px; }
        p { color: #333333; margin-bottom: 20px; }
        .launch-btn {
            background: linear-gradient(135deg, #E85002 0%, #C10801 100%);
            color: #F9F9F9;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .launch-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(232, 80, 2, 0.3);
        }
    </style>
</head>
<body>
    <div class="loading-container">
        <div class="spinner"></div>
        <h1>🤖 A.U.R.A</h1>
        <p>Adaptive User Retention Assistant</p>
        <p>Loading your PWA experience...</p>
        <a href="http://localhost:7860" class="launch-btn">Launch A.U.R.A</a>
    </div>
    
    <script>
        // Register service worker
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => console.log('A.U.R.A Service Worker registered'))
                .catch(error => console.log('Service Worker registration failed'));
        }
        
        // Auto-redirect to Gradio app
        setTimeout(() => {
            window.location.href = 'http://localhost:7860';
        }, 2000);
    </script>
</body>
</html>"""
    
    with open('index.html', 'w') as f:
        f.write(index_html)
    
    print("✅ A.U.R.A PWA setup completed!")
    print("\n📱 PWA Features Enabled:")
    print("   • Installable on mobile devices")
    print("   • Offline functionality with service worker")
    print("   • Native app-like experience")
    print("   • Push notifications support")
    print("   • Background sync capabilities")
    print("   • App shortcuts for quick access")
    print("   • Responsive design for all devices")
    
    print("\n🚀 To use A.U.R.A PWA:")
    print("   1. Start the Gradio app: python3 aura_gradio_app.py")
    print("   2. Open http://localhost:7860 in your browser")
    print("   3. Look for 'Install' or 'Add to Home Screen' option")
    print("   4. Follow the installation prompts")
    
    print("\n📋 PWA Installation Instructions:")
    print("   • Chrome/Edge: Look for install icon in address bar")
    print("   • Safari: Tap Share > Add to Home Screen")
    print("   • Firefox: Look for install option in menu")
    print("   • Mobile: Browser will show 'Add to Home Screen' option")
    
    return True

if __name__ == "__main__":
    setup_pwa()
