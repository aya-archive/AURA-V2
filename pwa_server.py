#!/usr/bin/env python3
"""
A.U.R.A PWA Server
Serves the Progressive Web App with proper headers and static files
"""

import http.server
import socketserver
import os
import mimetypes
from urllib.parse import urlparse

class PWAServer(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP server for PWA with proper headers"""
    
    def end_headers(self):
        # Add PWA-specific headers
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        
        # CORS headers for PWA
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests with PWA support"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Serve manifest.json with correct MIME type
        if path == '/manifest.json':
            self.send_response(200)
            self.send_header('Content-Type', 'application/manifest+json')
            self.end_headers()
            with open('manifest.json', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # Serve service worker with correct MIME type
        if path == '/sw.js':
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.end_headers()
            with open('sw.js', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # Serve icons
        if path.startswith('/icons/'):
            icon_path = path[1:]  # Remove leading slash
            if os.path.exists(icon_path):
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.end_headers()
                with open(icon_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
        
        # Default to parent class behavior
        super().do_GET()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    """Start the PWA server"""
    PORT = 8080
    
    print("🚀 Starting A.U.R.A PWA Server...")
    print(f"📱 PWA will be available at: http://localhost:{PORT}")
    print("🔧 PWA Features:")
    print("   • Installable on mobile devices")
    print("   • Offline functionality")
    print("   • Native app-like experience")
    print("   • Push notifications support")
    print("   • Background sync")
    print("\n📋 To install A.U.R.A PWA:")
    print("   1. Open http://localhost:8080 in your browser")
    print("   2. Look for 'Install' or 'Add to Home Screen' option")
    print("   3. Follow the installation prompts")
    print("\n🛑 Press Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), PWAServer) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 A.U.R.A PWA Server stopped")

if __name__ == "__main__":
    main()
