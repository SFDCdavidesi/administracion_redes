#!/usr/bin/env python3
"""
Servidor local simple para servir la aplicación web
con soporte para lectura dinámica del directorio datasets/
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
import os

class DatasetHandler(SimpleHTTPRequestHandler):
    """Maneja requests incluyendo endpoint dinámico para datasets."""
    
    def do_GET(self):
        # Endpoint dinámico para listar datasets
        if self.path == '/api/datasets':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            datasets_dir = Path(__file__).parent / 'datasets'
            files = sorted([
                f.name for f in datasets_dir.glob('*.json')
                if f.name != 'index.json'
            ])
            
            response = {'files': files}
            self.wfile.write(json.dumps(response).encode())
            return
        
        # CORS headers para todos los requests
        if self.path.startswith('/api/') or self.path.endswith('.json'):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
        
        # Default: servir archivos estáticos
        super().do_GET()
    
    def end_headers(self):
        """Añade headers CORS a todas las respuestas."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        super().end_headers()

def run_server(port=8000):
    """Inicia el servidor en el puerto especificado."""
    os.chdir(Path(__file__).parent)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, DatasetHandler)
    
    print(f"🚀 Servidor iniciado en http://localhost:{port}")
    print(f"   Abre http://localhost:{port} en tu navegador")
    print(f"\n📡 Endpoint dinámico:")
    print(f"   GET http://localhost:{port}/api/datasets")
    print(f"\n⚙️  Presiona Ctrl+C para detener\n")
    
    httpd.serve_forever()

if __name__ == '__main__':
    run_server(8000)
